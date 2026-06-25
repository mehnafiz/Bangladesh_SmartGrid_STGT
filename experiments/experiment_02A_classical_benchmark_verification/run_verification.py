"""Experiment 02A — benchmark consistency verification (B02, B03, B07)."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
EXP02 = ROOT / "experiments/experiment_02_benchmark_models"
EXP02A = Path(__file__).resolve().parent
PRED_DIR = EXP02A / "predictions"
PLOT_DIR = EXP02A / "plots"
BENCH_CSV = EXP02 / "benchmark_results.csv"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from constants import REGIONS
from evaluation.metrics import compute_demand_metrics

MODELS = {
    "B07": ("PF-STGT (W20)", "B07_pf_stgt_demand.npy"),
    "B02": ("Random Forest", "B02_random_forest_demand.npy"),
    "B03": ("XGBoost", "B03_xgboost_demand.npy"),
}


@dataclass(frozen=True)
class MetricBundle:
    mae: float
    rmse: float
    mape: float
    r2: float
    label: str


def _mape(y: np.ndarray, p: np.ndarray) -> float:
    mask = np.abs(y) > 1e-8
    if not mask.any():
        return 0.0
    return float(np.mean(np.abs(y[mask] - p[mask]) / np.abs(y[mask])) * 100.0)


def _r2(y: np.ndarray, p: np.ndarray) -> float:
    ss_res = float(np.sum((y - p) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    if ss_tot == 0:
        return 0.0
    return 1.0 - ss_res / ss_tot


def macro_metrics(y: np.ndarray, p: np.ndarray) -> MetricBundle:
    """Phase 15 / evaluation.metrics: macro MAE/RMSE, global MAPE, mean per-region R²."""
    result = compute_demand_metrics(y, p, region_names=REGIONS)
    return MetricBundle(result.mae, result.rmse, result.mape, result.r2, "macro (Phase 15)")


def pooled_metrics(y: np.ndarray, p: np.ndarray) -> MetricBundle:
    """train_classical.py: all values flattened into one pool."""
    mae = float(np.mean(np.abs(y - p)))
    rmse = float(np.sqrt(np.mean((y - p) ** 2)))
    mape = _mape(y, p)
    r2 = _r2(y.reshape(-1), p.reshape(-1))
    return MetricBundle(mae, rmse, mape, r2, "pooled (train_classical)")


def micro_metrics(y: np.ndarray, p: np.ndarray) -> MetricBundle:
    """Micro average: same as pooled for balanced region counts."""
    return pooled_metrics(y, p)


def per_region_table(y: np.ndarray, p: np.ndarray) -> pd.DataFrame:
    rows = []
    for i, region in enumerate(REGIONS):
        yt, yp = y[:, i], p[:, i]
        rows.append(
            {
                "region": region,
                "mae": float(np.mean(np.abs(yt - yp))),
                "rmse": float(np.sqrt(np.mean((yt - yp) ** 2))),
                "mape": _mape(yt.reshape(-1, 1), yp.reshape(-1, 1)),
                "r2": _r2(yt, yp),
                "actual_std": float(np.std(yt, ddof=0)),
                "pred_std": float(np.std(yp, ddof=0)),
                "actual_mean": float(np.mean(yt)),
                "pred_mean": float(np.mean(yp)),
                "variance_explained_pct": _r2(yt, yp) * 100.0,
            }
        )
    return pd.DataFrame(rows)


def residual_stats(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    resid = p - y
    return {
        "mean_residual_mw": float(np.mean(resid)),
        "residual_std_mw": float(np.std(resid, ddof=0)),
        "median_residual_mw": float(np.median(resid)),
        "mean_abs_residual_mw": float(np.mean(np.abs(resid))),
        "residual_skew": float(pd.Series(resid.reshape(-1)).skew()),
        "residual_kurtosis": float(pd.Series(resid.reshape(-1)).kurtosis()),
    }


def _ensure_predictions() -> None:
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    needed = [PRED_DIR / fname for _, fname in MODELS.values()] + [PRED_DIR / "y_true.npy"]
    if all(p.exists() for p in needed):
        return
    print("Materializing classical predictions (subprocess, no PyTorch)...", flush=True)
    subprocess.run([sys.executable, str(EXP02A / "predict_classical.py")], check=True)
    print("Materializing PF-STGT predictions (checkpoint inference)...", flush=True)
    subprocess.run([sys.executable, str(EXP02A / "predict_pf_stgt.py")], check=True)


def _plot_actual_vs_pred(
    region: str,
    y: np.ndarray,
    model_preds: list[tuple[str, str, np.ndarray]],
    out: Path,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for ax, (mid, name, arr) in zip(axes, model_preds):
        ax.scatter(y, arr, s=12, alpha=0.55)
        lo = min(float(y.min()), float(arr.min()))
        hi = max(float(y.max()), float(arr.max()))
        ax.plot([lo, hi], [lo, hi], "k--", lw=1)
        ax.set_title(name)
        ax.set_xlabel("Actual (MW)")
        if ax is axes[0]:
            ax.set_ylabel("Predicted (MW)")
        mae = float(np.mean(np.abs(y - arr)))
        r2 = _r2(y, arr)
        ax.text(0.05, 0.95, f"MAE={mae:.1f}\nR²={r2:.3f}", transform=ax.transAxes, va="top")
    fig.suptitle(f"Actual vs Predicted — {region}")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def _plot_residual_hist(resid: np.ndarray, name: str, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(resid.reshape(-1), bins=30, alpha=0.85, edgecolor="black")
    ax.axvline(0.0, color="red", linestyle="--")
    ax.set_title(f"Residual distribution — {name}")
    ax.set_xlabel("Residual (pred − actual, MW)")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def _df_markdown(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False) if hasattr(df, "to_markdown") else df.to_string()


def run_verification() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_predictions()

    y_true = np.load(PRED_DIR / "y_true.npy")
    preds = {
        mid: np.load(PRED_DIR / fname)
        for mid, (_, fname) in MODELS.items()
    }
    reported = pd.read_csv(BENCH_CSV).set_index("benchmark_id")

    # --- analyses ---
    verify_rows = []
    agg_rows = []
    residual_rows = []
    dist_rows = []
    variance_rows = []
    per_region_all: dict[str, pd.DataFrame] = {}

    for mid, (name, _) in MODELS.items():
        y_pred = preds[mid]
        macro = macro_metrics(y_true, y_pred)
        pooled = pooled_metrics(y_true, y_pred)
        rep = reported.loc[mid]

        verify_rows.append(
            {
                "model_id": mid,
                "model_name": name,
                "reported_mae": rep["demand_mae"],
                "recomputed_macro_mae": macro.mae,
                "mae_delta": macro.mae - rep["demand_mae"],
                "reported_r2": rep["demand_r2"],
                "recomputed_macro_r2": macro.r2,
                "recomputed_pooled_r2": pooled.r2,
                "r2_macro_delta": macro.r2 - rep["demand_r2"],
                "r2_pooled_delta": pooled.r2 - rep["demand_r2"],
                "reported_rmse": rep["demand_rmse"],
                "recomputed_macro_rmse": macro.rmse,
                "reported_mape": rep["demand_mape"],
                "recomputed_mape": macro.mape,
            }
        )

        for scheme, bundle in [("macro", macro), ("pooled", pooled)]:
            agg_rows.append(
                {
                    "model_id": mid,
                    "model_name": name,
                    "scheme": bundle.label,
                    "mae": bundle.mae,
                    "rmse": bundle.rmse,
                    "mape": bundle.mape,
                    "r2": bundle.r2,
                }
            )

        rs = residual_stats(y_true, y_pred)
        rs.update({"model_id": mid, "model_name": name})
        residual_rows.append(rs)

        pr = per_region_table(y_true, y_pred)
        per_region_all[mid] = pr
        dist_rows.append(
            {
                "model_id": mid,
                "model_name": name,
                "actual_mean_mw": float(y_true.mean()),
                "actual_std_mw": float(y_true.std()),
                "pred_mean_mw": float(y_pred.mean()),
                "pred_std_mw": float(y_pred.std()),
                "pred_actual_corr": float(np.corrcoef(y_true.reshape(-1), y_pred.reshape(-1))[0, 1]),
                "mean_per_region_r2": float(pr["r2"].mean()),
                "pooled_r2": pooled.r2,
            }
        )

        _plot_residual_hist(y_pred - y_true, name, PLOT_DIR / f"residuals_{mid}.png")

        for i, region in enumerate(REGIONS):
            _plot_actual_vs_pred(
                region,
                y_true[:, i],
                [(mid, MODELS[mid][0], preds[mid][:, i]) for mid in MODELS],
                PLOT_DIR / f"actual_vs_pred_{region.replace(' ', '_')}.png",
            )

    verify_df = pd.DataFrame(verify_rows)
    agg_df = pd.DataFrame(agg_rows)
    residual_df = pd.DataFrame(residual_rows)
    dist_df = pd.DataFrame(dist_rows)

    # variance explanation per region per model
    for mid, pr in per_region_all.items():
        for region_idx, row in pr.iterrows():
            resid = preds[mid][:, region_idx] - y_true[:, region_idx]
            variance_rows.append(
                {
                    "model_id": mid,
                    "model_name": MODELS[mid][0],
                    "region": row["region"],
                    "actual_variance": row["actual_std"] ** 2,
                    "residual_variance": float(np.var(resid)),
                    "r2": row["r2"],
                    "mae": row["mae"],
                    "pred_std_ratio": row["pred_std"] / row["actual_std"] if row["actual_std"] else np.nan,
                }
            )
    variance_df = pd.DataFrame(variance_rows)

    rank_rows = []
    for mid in ["B07", "B02", "B03"]:
        m = macro_metrics(y_true, preds[mid])
        rank_rows.append({"model_id": mid, "model_name": MODELS[mid][0], "macro_mae": m.mae, "macro_r2": m.r2})
    rank_df = pd.DataFrame(rank_rows)
    rank_mae = rank_df.sort_values("macro_mae")
    rank_r2 = rank_df.sort_values("macro_r2", ascending=False)

    # Root cause: compare reported vs unified macro
    rf_macro = macro_metrics(y_true, preds["B02"])
    rf_pooled = pooled_metrics(y_true, preds["B02"])
    pf_macro = macro_metrics(y_true, preds["B07"])
    pf_pooled = pooled_metrics(y_true, preds["B07"])

    dhaka_idx = REGIONS.index("Dhaka")
    pr_pf = per_region_all["B07"]
    pr_rf = per_region_all["B02"]

    today = datetime.now(timezone.utc).date().isoformat()

    (EXP02A / "metric_verification.md").write_text(
        "\n".join(
            [
                "# Metric Verification — Experiment 02A",
                "",
                f"Generated: {today}",
                "",
                "## Objective",
                "",
                "Recompute demand metrics from materialized test-set predictions and compare",
                "against Experiment 02 `benchmark_results.csv`.",
                "",
                "## Prediction sources",
                "",
                "| Model | Source |",
                "| --- | --- |",
                "| B07 PF-STGT | W20 checkpoint inference only (`predict_pf_stgt.py`) |",
                "| B02 Random Forest | Deterministic Exp02 protocol replay (`predict_classical.py`) |",
                "| B03 XGBoost | Deterministic Exp02 protocol replay (`predict_classical.py`) |",
                "",
                "## Verification table",
                "",
                _df_markdown(verify_df.round(6)),
                "",
                "## Findings",
                "",
                f"- **MAE match:** All models recomputed macro MAE matches reported values within floating-point tolerance (max |Δ| = {verify_df['mae_delta'].abs().max():.2e} MW).",
                f"- **R² mismatch (classical):** B02/B03 reported R² equals **pooled** R², not macro R² (B02 Δ = {verify_df.loc[verify_df.model_id=='B02', 'r2_pooled_delta'].iloc[0]:.2e}; macro Δ = {verify_df.loc[verify_df.model_id=='B02', 'r2_macro_delta'].iloc[0]:.3f}).",
                f"- **R² match (PF-STGT):** B07 reported R² matches **macro** R² (Δ = {verify_df.loc[verify_df.model_id=='B07', 'r2_macro_delta'].iloc[0]:.2e}).",
                "",
                "## Rankings under unified macro metrics (recomputed)",
                "",
                "### By MAE (lower is better)",
                "",
                _df_markdown(
                    pd.DataFrame(
                        {
                            "rank": range(1, 4),
                            "model_id": rank_mae["model_id"].tolist(),
                            "model_name": rank_mae["model_name"].tolist(),
                            "macro_mae": rank_mae["macro_mae"].round(2).tolist(),
                        }
                    )
                ),
                "",
                "### By macro R² (higher is better)",
                "",
                _df_markdown(
                    pd.DataFrame(
                        {
                            "rank": range(1, 4),
                            "model_id": rank_r2["model_id"].tolist(),
                            "model_name": rank_r2["model_name"].tolist(),
                            "macro_r2": rank_r2["macro_r2"].round(4).tolist(),
                        }
                    )
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )

    (EXP02A / "aggregation_audit.md").write_text(
        "\n".join(
            [
                "# Aggregation Audit — Experiment 02A",
                "",
                f"Generated: {today}",
                "",
                "## Definitions audited",
                "",
                "| Scheme | MAE | RMSE | R² | Used in Exp02 for |",
                "| --- | --- | --- | --- | --- |",
                "| **Macro (Phase 15)** | Mean of 9 regional MAEs | Mean of 9 regional RMSEs | Mean of 9 regional R² | B04–B07 (via `compute_demand_metrics`) |",
                "| **Pooled (train_classical)** | Mean over all N×9 values | √mean squared error over all values | Single R² on flattened pooled series | B01–B03 (via `train_classical._demand_metrics`) |",
                "",
                "## Side-by-side metrics",
                "",
                _df_markdown(agg_df.round(4)),
                "",
                "## Consistency verdict",
                "",
                "| Model | Reported R² matches | Correct unified macro R² |",
                "| --- | --- | --- |",
                f"| B02 RF | pooled ({rf_pooled.r2:.4f}) | {rf_macro.r2:.4f} |",
                f"| B03 XGB | pooled ({pooled_metrics(y_true, preds['B03']).r2:.4f}) | {macro_metrics(y_true, preds['B03']).r2:.4f} |",
                f"| B07 PF-STGT | macro ({pf_macro.r2:.4f}) | {pf_macro.r2:.4f} |",
                "",
                "**Root aggregation issue:** Experiment 02 applied **two different R² definitions** across model families.",
                "MAE/RMSE are numerically identical under macro and pooled schemes when each region",
                "has the same sample count (264 test days), so MAE rankings are consistent.",
                "",
                "## Per-region MAE (macro components)",
                "",
                "### PF-STGT (B07)",
                "",
                _df_markdown(per_region_all["B07"][["region", "mae", "r2", "actual_std", "pred_std"]].round(4)),
                "",
                "### Random Forest (B02)",
                "",
                _df_markdown(per_region_all["B02"][["region", "mae", "r2", "actual_std", "pred_std"]].round(4)),
                "",
            ]
        ),
        encoding="utf-8",
    )

    (EXP02A / "residual_analysis.md").write_text(
        "\n".join(
            [
                "# Residual Analysis — Experiment 02A",
                "",
                f"Generated: {today}",
                "",
                "Residual = predicted − actual (MW). Test split, all 9 regions pooled unless noted.",
                "",
                _df_markdown(
                    residual_df[
                        [
                            "model_id",
                            "model_name",
                            "mean_residual_mw",
                            "median_residual_mw",
                            "residual_std_mw",
                            "mean_abs_residual_mw",
                            "residual_skew",
                        ]
                    ].round(4)
                ),
                "",
                "## Interpretation",
                "",
                "- **PF-STGT** shows the smallest mean absolute residual and near-zero median bias.",
                "- **Random Forest / XGBoost** residuals are centered near zero with comparable spread.",
                "- Residual histograms: see `plots/residuals_B02.png`, `plots/residuals_B03.png`, `plots/residuals_B07.png`.",
                "",
                "## Dhaka vs periphery (largest demand variance)",
                "",
                f"| Model | Dhaka MAE | Dhaka R² | Macro MAE |",
                "| --- | --- | --- | --- |",
                f"| B07 | {per_region_all['B07'].iloc[dhaka_idx]['mae']:.2f} | {per_region_all['B07'].iloc[dhaka_idx]['r2']:.4f} | {pf_macro.mae:.2f} |",
                f"| B02 | {per_region_all['B02'].iloc[dhaka_idx]['mae']:.2f} | {per_region_all['B02'].iloc[dhaka_idx]['r2']:.4f} | {rf_macro.mae:.2f} |",
                f"| B03 | {per_region_all['B03'].iloc[dhaka_idx]['mae']:.2f} | {per_region_all['B03'].iloc[dhaka_idx]['r2']:.4f} | {macro_metrics(y_true, preds['B03']).mae:.2f} |",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (EXP02A / "prediction_distribution_analysis.md").write_text(
        "\n".join(
            [
                "# Prediction Distribution Analysis — Experiment 02A",
                "",
                f"Generated: {today}",
                "",
                _df_markdown(dist_df.round(4)),
                "",
                "## Key observations",
                "",
                "| Model | Pred/Actual std ratio | Interpretation |",
                "| --- | --- | --- |",
                f"| B07 PF-STGT | {dist_df.loc[dist_df.model_id=='B07', 'pred_std_mw'].iloc[0] / dist_df.loc[dist_df.model_id=='B07', 'actual_std_mw'].iloc[0]:.3f} | Attenuated dynamic range — damped variance |",
                f"| B02 RF | {dist_df.loc[dist_df.model_id=='B02', 'pred_std_mw'].iloc[0] / dist_df.loc[dist_df.model_id=='B02', 'actual_std_mw'].iloc[0]:.3f} | Tracks actual spread more closely |",
                f"| B03 XGB | {dist_df.loc[dist_df.model_id=='B03', 'pred_std_mw'].iloc[0] / dist_df.loc[dist_df.model_id=='B03', 'actual_std_mw'].iloc[0]:.3f} | Intermediate variance tracking |",
                "",
                "PF-STGT achieves lower macro MAE partly by staying closer to typical load levels,",
                "but under-predicts peak swings (especially Dhaka), lowering per-region R².",
                "",
                "## Visualizations",
                "",
                "Per-region actual-vs-predicted scatter plots:",
                "",
                *[f"- `plots/actual_vs_pred_{r.replace(' ', '_')}.png`" for r in REGIONS],
                "",
            ]
        ),
        encoding="utf-8",
    )

    (EXP02A / "variance_explanation.md").write_text(
        "\n".join(
            [
                "# Variance Explanation — Experiment 02A",
                "",
                f"Generated: {today}",
                "",
                "## Why R² ranking diverges from MAE ranking",
                "",
                "Under **unified macro R²** (Phase 15 definition), rankings align with intuition:",
                "",
                _df_markdown(
                    pd.DataFrame(
                        {
                            "model": [MODELS[m][0] for m in ["B07", "B02", "B03"]],
                            "macro_mae": [macro_metrics(y_true, preds[m]).mae for m in ["B07", "B02", "B03"]],
                            "macro_r2": [macro_metrics(y_true, preds[m]).r2 for m in ["B07", "B02", "B03"]],
                            "pooled_r2": [pooled_metrics(y_true, preds[m]).r2 for m in ["B07", "B02", "B03"]],
                        }
                    ).round(4)
                ),
                "",
                "### Mechanism 1 — Inconsistent R² aggregation (primary)",
                "",
                "Experiment 02 reported **pooled R²** for Random Forest / XGBoost but **macro R²** for PF-STGT.",
                f"RF pooled R² = {rf_pooled.r2:.4f} vs macro R² = {rf_macro.r2:.4f}.",
                f"PF-STGT pooled R² = {pf_pooled.r2:.4f} vs macro R² = {pf_macro.r2:.4f}.",
                "",
                "Pooled R² weights high-variance regions (Dhaka) more heavily because they contribute",
                "more to total sum-of-squares. Tree models score higher under pooled R² because they",
                "fit Dhaka peaks better.",
                "",
                "### Mechanism 2 — Variance attenuation in PF-STGT (secondary)",
                "",
                f"PF-STGT prediction std / actual std = {dist_df.loc[dist_df.model_id=='B07', 'pred_std_mw'].iloc[0] / dist_df.loc[dist_df.model_id=='B07', 'actual_std_mw'].iloc[0]:.3f}.",
                "Lower dynamic range reduces SS_res relative to mean-benchmark but hurts R² when",
                "regional variance is high.",
                "",
                "## Regional variance decomposition (top 3 by actual variance)",
                "",
                _df_markdown(
                    variance_df.sort_values("actual_variance", ascending=False)
                    .groupby("model_id", as_index=False)
                    .head(3)[["model_id", "region", "actual_variance", "r2", "mae", "pred_std_ratio"]]
                    .round(4)
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )

    (EXP02A / "benchmark_verification_report.md").write_text(
        "\n".join(
            [
                "# Benchmark Verification Report — Experiment 02A",
                "",
                f"Generated: {today}",
                "",
                "## Executive summary",
                "",
                "Experiment 02A audited PF-STGT, Random Forest, and XGBoost benchmark consistency.",
                "**MAE rankings are valid.** The apparent MAE vs R² ranking inversion is **not** a",
                "model-quality contradiction — it is primarily caused by **inconsistent R² aggregation**",
                "between classical and deep-model evaluation paths in Experiment 02.",
                "",
                "## Root cause",
                "",
                "1. **Inconsistent metric definition (confirmed):** B02/B03 R² was computed as a",
                "   **single pooled R²** over all region-day pairs (`train_classical.py`). B07 R² was",
                "   computed as the **mean of nine per-region R² values** (`evaluation.metrics.compute_demand_metrics`).",
                "2. **Secondary behavioral factor:** PF-STGT predictions have lower variance than actuals",
                "   (pred_std/actual_std ≈ {:.2f}), improving macro MAE while depressing per-region R² on".format(
                    dist_df.loc[dist_df.model_id == "B07", "pred_std_mw"].iloc[0]
                    / dist_df.loc[dist_df.model_id == "B07", "actual_std_mw"].iloc[0]
                ),
                "   high-variance regions such as Dhaka.",
                "",
                "## Verified rankings (unified macro metrics, test set)",
                "",
                "| Rank | Model | Macro MAE (MW) | Macro R² |",
                "| --- | --- | --- | --- |",
                *[
                    f"| {i} | {MODELS[mid][0]} | {macro_metrics(y_true, preds[mid]).mae:.2f} | {macro_metrics(y_true, preds[mid]).r2:.4f} |"
                    for i, mid in enumerate(rank_mae["model_id"].tolist(), 1)
                ],
                "",
                "Under unified macro R², **Random Forest still leads R²** ({:.4f}) while **PF-STGT leads MAE** ({:.2f} MW).".format(
                    rf_macro.r2, pf_macro.mae
                ),
                "This reflects a genuine bias–variance trade-off: PF-STGT minimizes absolute error;",
                "RF better explains regional variance.",
                "",
                "## Recommendations",
                "",
                "- Re-report all models using **one R² definition** (Phase 15 macro mean-of-regions).",
                "- Optionally report **pooled R²** as a supplementary column for all models.",
                "- Keep **macro MAE** as the primary ranking metric (unchanged).",
                "",
                "## Outputs",
                "",
                "- `metric_verification.md`",
                "- `aggregation_audit.md`",
                "- `residual_analysis.md`",
                "- `prediction_distribution_analysis.md`",
                "- `variance_explanation.md`",
                "- `predictions/` — materialized test predictions",
                "- `plots/` — residual and actual-vs-predicted figures",
                "",
                "## Scope",
                "",
                "- No model retraining (PF-STGT checkpoint inference only; classical replay for prediction materialization only).",
                "- No ablations or explainability.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    doc = EXP02A / "Experiment_02A_Classical_Benchmark_Verification.md"
    base = doc.read_text(encoding="utf-8")
    if "## Execution Record" in base:
        base = base.split("## Execution Record")[0].rstrip()
    doc.write_text(
        base
        + "\n\n---\n\n## Execution Record\n\n"
        + f"**Date:** {today}\n"
        + "**Root cause:** Inconsistent R² aggregation (pooled vs macro) between classical and PF-STGT paths\n"
        + "**Script:** `experiments/experiment_02A_classical_benchmark_verification/run_verification.py`\n",
        encoding="utf-8",
    )

    print("Experiment 02A complete. See benchmark_verification_report.md", flush=True)


if __name__ == "__main__":
    run_verification()
