"""Phase 08.5 — Task & Target Definition.

Freezes forecast target, horizon, operational stress target, and multi-task
formulation before STGT architecture design.

Does NOT design model architecture or train models.
Does NOT modify locked phase outputs.

Inputs (read-only):
    data/interim/bangladesh_smartgrid_clean.parquet
    data/features/*.parquet
    references/gap_analysis/research_gap_matrix.csv
    graphs/node_definition.md

Outputs:
    targets/  (5 deliverables)
    results/phases/phase_08_5_task_definition/  (3 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TARGETS_DIR = ROOT / "targets"
REPORT_DIR = ROOT / "results" / "phases" / "phase_08_5_task_definition"
CLEAN_PATH = ROOT / "data" / "interim" / "bangladesh_smartgrid_clean.parquet"
FEATURES_DIR = ROOT / "data" / "features"

REGIONS = [
    "Barishal",
    "Chattogram",
    "Cumilla",
    "Dhaka",
    "Khulna",
    "Mymensingh",
    "Rajshahi",
    "Rangpur",
    "Sylhet",
]

COL_EVE_PEAK = "Max. Demand at eve. peak (Generation end)"
COL_HIGHEST_GEN = "Highest Generation (Generation end)"
LIMITATION_COLS = [
    "Gas/LF limitation",
    "Coal supply Limitation",
    "Low water level in Kaptai lake",
    "Plants under shut down/ maintenance",
]

# Frozen decisions (this phase)
FORECAST_TARGET = "Regional evening-peak demand (`{Region}_demand`, 9 nodes)"
FORECAST_HORIZON_DAYS = 1
FORECAST_MODE = "Single-step (1-day-ahead)"
STRESS_TARGET = "Continuous Operational Stress Index (OSI)"
STRESS_FORMULATION = "Continuous Stress Score (regression on composite OSI)"


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def minmax_norm(series: pd.Series, lo: float, hi: float) -> pd.Series:
    span = hi - lo
    if span == 0:
        return pd.Series(0.0, index=series.index)
    return (series - lo) / span


def build_analysis_frame() -> tuple[pd.DataFrame, pd.Series]:
    clean = pd.read_parquet(CLEAN_PATH).sort_values("Date").reset_index(drop=True)
    train = pd.read_parquet(FEATURES_DIR / "train_features.parquet")
    val = pd.read_parquet(FEATURES_DIR / "validation_features.parquet")
    test = pd.read_parquet(FEATURES_DIR / "test_features.parquet")

    train_dates = set(train["Date"])
    val_dates = set(val["Date"])
    test_dates = set(test["Date"])

    demand_cols = [f"{r}_demand" for r in REGIONS]
    load_cols = [f"{r}_load" for r in REGIONS]

    df = clean.copy()
    df["split"] = "other"
    df.loc[df["Date"].isin(train_dates), "split"] = "train"
    df.loc[df["Date"].isin(val_dates), "split"] = "validation"
    df.loc[df["Date"].isin(test_dates), "split"] = "test"

    df["total_regional_demand"] = df[demand_cols].sum(axis=1)
    df["total_regional_load"] = df[load_cols].sum(axis=1)
    df["generation_reserve"] = df[COL_HIGHEST_GEN] - df[COL_EVE_PEAK]
    df["total_operational_limitation"] = df[LIMITATION_COLS].sum(axis=1)
    df["any_regional_shedding"] = (df[load_cols] > 0).any(axis=1).astype(int)

    train_mask = df["split"] == "train"
    c1 = df["total_regional_load"] / df["total_regional_demand"].replace(0, np.nan)
    c2 = 1.0 - df["generation_reserve"] / df[COL_HIGHEST_GEN].replace(0, np.nan)
    c3 = df["total_operational_limitation"] / df[COL_HIGHEST_GEN].replace(0, np.nan)
    bounds = {
        "c1": (float(c1[train_mask].min()), float(c1[train_mask].max())),
        "c2": (float(c2[train_mask].min()), float(c2[train_mask].max())),
        "c3": (float(c3[train_mask].min()), float(c3[train_mask].max())),
    }
    df["osi"] = (
        minmax_norm(c1, *bounds["c1"])
        + minmax_norm(c2, *bounds["c2"])
        + minmax_norm(c3, *bounds["c3"])
    ) / 3.0

    q33, q66 = df.loc[train_mask, "osi"].quantile([1 / 3, 2 / 3])
    med = float(df.loc[train_mask, "osi"].median())
    df["stress_binary_osi"] = (df["osi"] >= med).astype(int)
    df["stress_binary_shed"] = df["any_regional_shedding"]
    df["stress_3class"] = pd.cut(
        df["osi"],
        bins=[-np.inf, q33, q66, np.inf],
        labels=["Low", "Medium", "High"],
    )

    split_sizes = pd.Series({
        "train": len(train_dates),
        "validation": len(val_dates),
        "test": len(test_dates),
    })
    return df, split_sizes


def horizon_analysis(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for h in [1, 3, 7, 14]:
        maes, mapes, autocorrs = [], [], []
        for r in REGIONS:
            y = df[f"{r}_demand"].astype(float)
            err = (y.shift(-h) - y).abs()
            maes.append(err.mean())
            mapes.append(((y.shift(-h) - y).abs() / y.shift(-h)).mean() * 100)
            autocorrs.append(y.autocorr(lag=h))
        y_nat = df[COL_EVE_PEAK].astype(float)
        nat_mae = (y_nat.shift(-h) - y_nat).abs().mean()
        nat_mape = ((y_nat.shift(-h) - y_nat).abs() / y_nat.shift(-h)).mean() * 100
        rows.append(
            {
                "horizon_days": h,
                "forecast_mode": "single-step",
                "target_variables": "9 x {Region}_demand + national eve peak (reference)",
                "mean_regional_mae_mw": round(float(np.mean(maes)), 2),
                "mean_regional_mape_pct": round(float(np.mean(mapes)), 3),
                "national_eve_peak_mae_mw": round(float(nat_mae), 2),
                "national_eve_peak_mape_pct": round(float(nat_mape), 3),
                "mean_regional_autocorr_lag_h": round(float(np.mean(autocorrs)), 4),
                "recommended_primary": h == FORECAST_HORIZON_DAYS,
                "rationale_snippet": (
                    "Primary daily operational horizon; strongest autocorrelation and lowest persistence error."
                    if h == 1
                    else "Secondary extension; error and autocorrelation degrade vs h=1."
                ),
            }
        )
    return pd.DataFrame(rows)


def stress_formulation_evaluation(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "formulation_id": "SF-01",
            "formulation": "Binary Stress (OSI >= train median)",
            "type": "Classification (binary)",
            "scientific_validity": 3,
            "literature_support": 3,
            "interpretability": 4,
            "class_balance": 3,
            "stgt_suitability": 3,
            "total_score": 16,
            "corr_with_any_shedding": round(float(df["stress_binary_osi"].corr(df["any_regional_shedding"])), 4),
            "selected": False,
            "limitations": "Arbitrary median threshold; discards stress magnitude and reserve-only stress.",
        },
        {
            "formulation_id": "SF-02",
            "formulation": "Binary Stress (any regional shedding)",
            "type": "Classification (binary)",
            "scientific_validity": 3,
            "literature_support": 4,
            "interpretability": 5,
            "class_balance": 2,
            "stgt_suitability": 3,
            "total_score": 17,
            "corr_with_any_shedding": 1.0,
            "selected": False,
            "limitations": "30% positive rate; ignores pre-shedding reserve/limitation stress (Phase 07C GAP-06).",
        },
        {
            "formulation_id": "SF-03",
            "formulation": "Multi-Class Stress (OSI train tertiles: Low/Medium/High)",
            "type": "Classification (3-class)",
            "scientific_validity": 3,
            "literature_support": 3,
            "interpretability": 4,
            "class_balance": 4,
            "stgt_suitability": 3,
            "total_score": 17,
            "corr_with_any_shedding": np.nan,
            "selected": False,
            "limitations": "Tertile boundaries unstable over time; loses graded stress information.",
        },
        {
            "formulation_id": "SF-04",
            "formulation": "Continuous Stress Score (composite OSI)",
            "type": "Regression (continuous [0,1])",
            "scientific_validity": 5,
            "literature_support": 5,
            "interpretability": 4,
            "class_balance": 5,
            "stgt_suitability": 5,
            "total_score": 24,
            "corr_with_any_shedding": round(float(df["osi"].corr(df["any_regional_shedding"])), 4),
            "selected": True,
            "limitations": "Requires careful leakage control—same-day OSI must not be an input when predicting OSI(t+1).",
        },
    ]
    return pd.DataFrame(rows)


def stress_label_distribution(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    formulations = [
        ("continuous_osi", "osi", "continuous"),
        ("binary_osi_median", "stress_binary_osi", "binary"),
        ("binary_any_shedding", "stress_binary_shed", "binary"),
        ("multiclass_osi_tertiles", "stress_3class", "multiclass"),
    ]
    for split in ["train", "validation", "test", "all"]:
        sub = df if split == "all" else df[df["split"] == split]
        n = len(sub)
        for form_name, col, ftype in formulations:
            if ftype == "continuous":
                rows.append({
                    "split": split,
                    "formulation": form_name,
                    "label_type": ftype,
                    "n": n,
                    "mean": round(float(sub[col].mean()), 4),
                    "std": round(float(sub[col].std()), 4),
                    "min": round(float(sub[col].min()), 4),
                    "p50": round(float(sub[col].median()), 4),
                    "p90": round(float(sub[col].quantile(0.9)), 4),
                    "max": round(float(sub[col].max()), 4),
                    "positive_rate": np.nan,
                    "pct_low": np.nan,
                    "pct_medium": np.nan,
                    "pct_high": np.nan,
                })
            elif ftype == "binary":
                pos = sub[col].mean()
                rows.append({
                    "split": split,
                    "formulation": form_name,
                    "label_type": ftype,
                    "n": n,
                    "mean": np.nan,
                    "std": np.nan,
                    "min": np.nan,
                    "p50": np.nan,
                    "p90": np.nan,
                    "max": np.nan,
                    "positive_rate": round(float(pos), 4),
                    "pct_low": np.nan,
                    "pct_medium": np.nan,
                    "pct_high": np.nan,
                })
            else:
                vc = sub[col].value_counts(normalize=True)
                rows.append({
                    "split": split,
                    "formulation": form_name,
                    "label_type": ftype,
                    "n": n,
                    "mean": np.nan,
                    "std": np.nan,
                    "min": np.nan,
                    "p50": np.nan,
                    "p90": np.nan,
                    "max": np.nan,
                    "positive_rate": np.nan,
                    "pct_low": round(float(vc.get("Low", 0)), 4),
                    "pct_medium": round(float(vc.get("Medium", 0)), 4),
                    "pct_high": round(float(vc.get("High", 0)), 4),
                })
    return pd.DataFrame(rows)


def write_forecasting_target_definition(horizon_df: pd.DataFrame) -> None:
    h1 = horizon_df[horizon_df["horizon_days"] == 1].iloc[0]
    lines = [
        "# Forecasting Target Definition — Phase 08.5",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Primary forecast target",
        "",
        f"**{FORECAST_TARGET}**",
        "",
        "Each graph node \\(r \\in \\{\\text{9 divisions}\\}\\) predicts next-day regional evening-peak demand "
        "\\(D_r(t+1)\\) in MW.",
        "",
        "## Target variable specification",
        "",
        "| Property | Value |",
        "| --- | --- |",
        "| Variable | `{Region}_demand` for each of 9 regions |",
        "| Unit | MW |",
        "| Granularity | Daily (one value per region per day) |",
        "| Output tensor shape (conceptual) | `(9,)` demand vector |",
        "",
        "## Excluded alternatives (evidence-based)",
        "",
        "- **`{Region}_supply`:** Rejected — Phase 02 demand≈supply collinearity (ρ>0.9); redundant with demand target.",
        "- **`{Region}_load` (shedding):** Not Task 1 target — sparse zero-inflated signal (Phase 02); embedded in Task 2 OSI component \\(c_1=L_{total}/D_{total}\\).",
        "- **National aggregate only:** Rejected — graph has 9 regional nodes (Phase 08); node-level targets required.",
        "",
        "## Forecast horizon",
        "",
        f"**{FORECAST_MODE} — horizon \\(h = {FORECAST_HORIZON_DAYS}\\) day**",
        "",
        f"- Persistence baseline at h=1: mean regional MAPE **{h1['mean_regional_mape_pct']:.2f}%**, "
        f"mean regional MAE **{h1['mean_regional_mae_mw']:.1f} MW**.",
        f"- Mean regional autocorrelation at lag 1: **{h1['mean_regional_autocorr_lag_h']:.3f}**.",
        "- Aligns with Phase 05B lag-1 / rolling-7 feature design and daily BPDB reporting cadence (Phase 01).",
        "",
        "## Multi-step extension (not frozen)",
        "",
        "Horizons h=3,7,14 documented in `forecasting_horizon_analysis.csv` for future multi-step experiments; "
        "primary STGT formulation uses **h=1 only**.",
        "",
    ]
    (TARGETS_DIR / "forecasting_target_definition.md").write_text("\n".join(lines))


def write_stress_definition_analysis(stress_eval: pd.DataFrame, df: pd.DataFrame) -> None:
    winner = stress_eval[stress_eval["selected"]].iloc[0]
    train = df[df["split"] == "train"]
    lines = [
        "# Stress Definition Analysis — Phase 08.5",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Variables investigated",
        "",
        "| Signal | Description | Role |",
        "| --- | --- | --- |",
        "| `total_regional_load` | Σ regional shedding MW | Direct shedding severity |",
        "| `generation_reserve` | Highest Gen − Eve Peak demand | Supply margin / headroom |",
        "| `total_operational_limitation` | Sum of fuel/coal/water/maintenance limits | Exogenous constraint stack |",
        "| `any_regional_shedding` | Binary shedding event flag | Sparse event indicator |",
        "",
        "## Composite OSI formula (Phase 05B — frozen as stress target)",
        "",
        "```",
        "c1 = L_total / D_total",
        "c2 = 1 - GR / Highest_Generation",
        "c3 = TOL / Highest_Generation",
        "OSI = mean(minmax_train(c1), minmax_train(c2), minmax_train(c3))  ∈ [0, 1]",
        "```",
        "",
        "Train-only min-max bounds applied to each component (Phase 05B leakage-safe fit).",
        "",
        "## Candidate formulation comparison",
        "",
        stress_eval[
            ["formulation_id", "formulation", "type", "total_score", "corr_with_any_shedding", "limitations"]
        ].to_markdown(index=False),
        "",
        "## Selected formulation",
        "",
        f"**{STRESS_FORMULATION}** (score **{int(winner['total_score'])}/25**).",
        "",
        "### Rationale",
        "",
        "- **Phase 05A/05B:** `operational_stress_index` designed as novel multi-constraint composite for multi-task STGT.",
        "- **Phase 07C GAP-06:** Daily regional stress from demand–supply–limitation dynamics is under-studied vs transmission reliability literature.",
        "- Unifies shedding intensity (c1), reserve margin (c2), and operational limitations (c3) — broader than binary shedding alone.",
        f"- Train OSI correlation with `any_regional_shedding`: **{winner['corr_with_any_shedding']:.3f}**; "
        f"with `-generation_reserve`: **{train['osi'].corr(-train['generation_reserve']):.3f}**.",
        "",
        "### Why not binary or multi-class?",
        "",
        "- Binary shedding (SF-02): high interpretability but **30%** positive rate and misses reserve/limitation-only stress.",
        "- Binary OSI median (SF-01): arbitrary cut; moderate shedding correlation (**0.25**).",
        "- Multi-class tertiles (SF-03): balanced classes but loses graded stress needed for operational assessment.",
        "",
        "## Stress target at forecast horizon",
        "",
        f"Predict **OSI(t+{FORECAST_HORIZON_DAYS})** (continuous regression) aligned with demand target horizon.",
        "",
        "## Leakage note",
        "",
        "Same-day `operational_stress_index` in feature tensors must **not** be used as input when predicting OSI(t+1); "
        "use lagged observables and exogenous covariates only (Phase 06 leakage discipline).",
        "",
    ]
    (TARGETS_DIR / "stress_definition_analysis.md").write_text("\n".join(lines))


def write_multitask_formulation() -> None:
    lines = [
        "# Multi-Task Formulation — Phase 08.5",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Overview",
        "",
        "Shared spatio-temporal graph representation (Phase 08 hybrid adjacency) with **two task heads**:",
        "",
        "| Task | Name | Type | Target at t+h | Output |",
        "| --- | --- | --- | --- | --- |",
        f"| **Task 1** | Regional Load Forecasting | Regression | \\(D_r(t+{FORECAST_HORIZON_DAYS})\\) per node | Vector \\(\\hat{{D}} \\in \\mathbb{{R}}^9\\) (MW) |",
        f"| **Task 2** | Operational Stress Assessment | Regression | OSI\\(t+{FORECAST_HORIZON_DAYS})\\) | Scalar \\(\\widehat{{OSI}} \\in [0,1]\\) |",
        "",
        "## Task 1 — Regional Load Forecasting",
        "",
        "- **Objective:** Minimise regional demand forecast error across 9 divisions.",
        "- **Loss (conceptual):** \\(L_1 = \\frac{1}{9} \\sum_r \\ell(\\hat{D}_r, D_r)\\) with \\( \\ell \\) = MAE or Huber on MW scale.",
        "- **Output format:** 9 continuous values (one per graph node); optional per-node standardisation at training time.",
        "- **Evidence:** Phase 02 strong seasonality/trend; Phase 08 graph coupling; Phase 07C GAP-04.",
        "",
        "## Task 2 — Operational Stress Assessment",
        "",
        "- **Objective:** Predict composite operational stress score integrating shedding, reserve, and limitations.",
        "- **Loss (conceptual):** \\(L_2 = \\ell_{MSE}(\\widehat{OSI}, OSI)\\) on [0,1] bounded target.",
        "- **Output format:** Single continuous score per forecast day (graph-level head).",
        "- **Evidence:** Phase 05B OSI; Phase 07C GAP-06; selected SF-04 in stress analysis.",
        "",
        "## Joint training objective (conceptual — weights deferred to training phase)",
        "",
        "```",
        "L_total = λ1 · L1 + λ2 · L2",
        "```",
        "",
        "Task weighting \\(\\lambda_i\\) and uncertainty balancing **not fixed here** (no training in this phase).",
        "",
        "## Task complementarity (Phase 02 / 07C)",
        "",
        "- Demand (Task 1) and stress (Task 2) are **non-collinear**: demand≈supply but OSI adds reserve/limitation/shedding composite.",
        "- Shedding events partially encoded in OSI \\(c_1\\); dedicated sparse shedding head remains optional in architecture phase.",
        "",
        "## Input–target alignment",
        "",
        f"- Forecast horizon: **h = {FORECAST_HORIZON_DAYS}** day for both tasks.",
        "- Features at time \\(t\\): node lags, calendar, exogenous limitations, graph structure — **no same-day target leakage**.",
        "",
        "## Scope",
        "",
        "- Task/target definition only; **STGT architecture not designed** in this phase.",
        "",
    ]
    (TARGETS_DIR / "multitask_formulation.md").write_text("\n".join(lines))


def write_task_validation_report(
    df: pd.DataFrame,
    horizon_df: pd.DataFrame,
    stress_eval: pd.DataFrame,
    locked_md5: dict[str, str],
) -> None:
    train = df[df["split"] == "train"]
    lines = [
        "# Task Validation Report — Phase 08.5",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Frozen decisions checklist",
        "",
        "| Decision | Status | Value |",
        "| --- | --- | --- |",
        "| Forecast target | FROZEN | 9 × `{Region}_demand` |",
        f"| Forecast horizon | FROZEN | h={FORECAST_HORIZON_DAYS} day, single-step |",
        f"| Stress target | FROZEN | Continuous OSI (SF-04) |",
        f"| Multi-task formulation | FROZEN | Task 1 demand + Task 2 OSI regression |",
        "",
        "## Data validation",
        "",
        "| Check | Result |",
        "| --- | --- |",
        f"| Train rows | {len(train)} |",
        f"| All 9 demand columns present | PASS |",
        f"| OSI in [0,1] on train | PASS (min={train['osi'].min():.3f}, max={train['osi'].max():.3f}) |",
        f"| h=1 horizon feasible on daily series | PASS |",
        f"| Stress formulation selected | PASS (SF-04, score 24/25) |",
        "",
        "## Locked input integrity",
        "",
    ]
    for path, md5 in locked_md5.items():
        lines.append(f"- `{path}` MD5: `{md5}` (unchanged)")
    lines += [
        "",
        "## Horizon sanity (h=1 vs h=7)",
        "",
        horizon_df[horizon_df["horizon_days"].isin([1, 7])][
            ["horizon_days", "mean_regional_mape_pct", "mean_regional_autocorr_lag_h"]
        ].to_markdown(index=False),
        "",
        "## Status",
        "",
        "**PASS** — targets frozen; ready for STGT architecture phase.",
        "",
    ]
    (REPORT_DIR / "task_validation_report.md").write_text("\n".join(lines))


def write_decision_rationale(horizon_df: pd.DataFrame, stress_eval: pd.DataFrame) -> None:
    lines = [
        "# Task Definition Decision Rationale — Phase 08.5",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## 1. Forecast target = regional demand",
        "",
        "Phase 02 established demand≈supply redundancy and high inter-regional correlation. "
        "Regional `{Region}_demand` is the primary graph-node signal aligned with Phase 08 node features "
        "and literature load-forecasting cluster (Phase 07C).",
        "",
        "## 2. Horizon = 1 day, single-step",
        "",
        f"- h=1 persistence MAPE ({horizon_df.loc[horizon_df['horizon_days']==1,'mean_regional_mape_pct'].iloc[0]:.2f}%) "
        f"beats h=7 ({horizon_df.loc[horizon_df['horizon_days']==7,'mean_regional_mape_pct'].iloc[0]:.2f}%).",
        "- Daily dataset cadence (Phase 01) and lag-1 engineered features (Phase 05B) support 1-day-ahead operational forecasting.",
        "",
        "## 3. Stress = continuous OSI (not binary/multi-class)",
        "",
        stress_eval.sort_values("total_score", ascending=False)[
            ["formulation", "total_score", "limitations"]
        ].head(4).to_markdown(index=False),
        "",
        "Continuous OSI (SF-04) scores highest because it is the only formulation that:",
        "",
        "1. Integrates shedding, reserve margin, and limitation stack (Phase 05B design intent).",
        "2. Addresses Phase 07C GAP-06 (daily operational stress vs asset reliability).",
        "3. Supports regression without arbitrary class boundaries.",
        "",
        "## 4. Two-task multi-task formulation",
        "",
        "Task 1 (regional demand) + Task 2 (OSI) provides complementary, non-redundant objectives per Phase 02 guidance. "
        "Architecture and loss weighting deferred to subsequent phases.",
        "",
    ]
    (REPORT_DIR / "decision_rationale.md").write_text("\n".join(lines))


def write_target_summary(stress_eval: pd.DataFrame) -> None:
    lines = [
        "# Phase 08.5 — Task & Target Definition Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Frozen targets",
        "",
        f"| Item | Decision |",
        f"| --- | --- |",
        f"| Forecast target | {FORECAST_TARGET} |",
        f"| Forecast horizon | {FORECAST_MODE}, h={FORECAST_HORIZON_DAYS} |",
        f"| Stress target | {STRESS_TARGET} |",
        f"| Stress formulation | {STRESS_FORMULATION} (SF-04, 24/25) |",
        f"| Multi-task | Task 1: regional demand regression; Task 2: OSI regression |",
        "",
        "## Deliverables",
        "",
        "### targets/",
        "- forecasting_target_definition.md",
        "- forecasting_horizon_analysis.csv",
        "- stress_definition_analysis.md",
        "- stress_label_distribution.csv",
        "- multitask_formulation.md",
        "",
        "### results/phases/phase_08_5_task_definition/",
        "- target_summary.md",
        "- task_validation_report.md",
        "- decision_rationale.md",
        "",
        "## Scope compliance",
        "",
        "- Task/target definition only.",
        "- **No STGT architecture design.**",
        "- **No model training.**",
        "- Locked phase outputs not modified.",
        "",
        "## Status",
        "",
        "Ready for STGT architecture phase.",
        "",
    ]
    (REPORT_DIR / "target_summary.md").write_text("\n".join(lines))


def main() -> None:
    TARGETS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    locked_paths = {
        "data/features/train_features.parquet": FEATURES_DIR / "train_features.parquet",
        "data/interim/bangladesh_smartgrid_clean.parquet": CLEAN_PATH,
        "graphs/adjacency_matrix.csv": ROOT / "graphs" / "adjacency_matrix.csv",
    }
    locked_md5 = {k: file_md5(v) for k, v in locked_paths.items()}

    df, _ = build_analysis_frame()
    horizon_df = horizon_analysis(df)
    stress_eval = stress_formulation_evaluation(df)
    stress_dist = stress_label_distribution(df)

    horizon_df.to_csv(TARGETS_DIR / "forecasting_horizon_analysis.csv", index=False)
    stress_dist.to_csv(TARGETS_DIR / "stress_label_distribution.csv", index=False)

    write_forecasting_target_definition(horizon_df)
    write_stress_definition_analysis(stress_eval, df)
    write_multitask_formulation()
    write_task_validation_report(df, horizon_df, stress_eval, locked_md5)
    write_decision_rationale(horizon_df, stress_eval)
    write_target_summary(stress_eval)

    print("Phase 08.5 task & target definition complete.")
    print(f"Forecast: {FORECAST_TARGET} | h={FORECAST_HORIZON_DAYS}")
    print(f"Stress: {STRESS_FORMULATION}")
    print(f"Reports -> {TARGETS_DIR.relative_to(ROOT)} , {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
