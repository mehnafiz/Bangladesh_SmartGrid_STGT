"""Experiment 03 — PF-STGT ablation studies (A1–A6)."""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from scipy import stats
from torch import Tensor
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
EXP_DIR = Path(__file__).resolve().parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
sys.path.insert(0, str(EXP_DIR))

from ablation_models import AblationPFSTGT
from constants import PROJECT_ROOT, REGIONS
from evaluation.metrics import compute_demand_metrics, compute_stress_metrics
from foundation import FoundationCoordinator
from graph.registry import GraphVariant
from models.pf_stgt import PFSTGT
from training.checkpoint import CheckpointManager
from training.config import TrainingConfig
from training.dataloader import build_dataloaders
from training.dataset import SmartGridTorchDataset, collate_smartgrid_batch
from training.early_stopping import EarlyStopping
from training.losses import DemandHuberLoss, LossBreakdown, StressMSELoss
from training.seed import set_seed
from training.trainer import Trainer
from training.validator import Validator
from utils.logging import setup_logging

OUTPUT_DIR = EXP_DIR
CKPT_ROOT = EXP_DIR / "checkpoints"
W20_CKPT = (
    PROJECT_ROOT
    / "experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt"
)
BENCH_CSV = PROJECT_ROOT / "experiments/experiment_02_benchmark_models/benchmark_results.csv"
SEED = 42
DEMAND_NORM = 100.0
W20 = dict(lambda_stress=20.0, normalize_demand=True, balanced_early_stop=True)
BONFERRONI_ALPHA = 0.01  # 5 comparisons vs A1


@dataclass(frozen=True)
class AblationSpec:
    ablation_id: str
    name: str
    graph_variant: GraphVariant
    structural: str  # A1, A2, A3, A4, or full
    multi_task: bool
    use_w20_checkpoint: bool = False


ABLATIONS: tuple[AblationSpec, ...] = (
    AblationSpec("A1", "PF-STGT (W20)", GraphVariant.HYBRID, "A1", True, use_w20_checkpoint=True),
    AblationSpec("A2", "No Graph", GraphVariant.HYBRID, "A2", True),
    AblationSpec("A3", "No Transformer", GraphVariant.HYBRID, "A3", True),
    AblationSpec("A4", "Single-Task", GraphVariant.HYBRID, "A4", False),
    AblationSpec("A5", "Geographical Graph Only", GraphVariant.GEO, "A1", True),
    AblationSpec("A6", "Correlation Graph Only", GraphVariant.CORR, "A1", True),
)


class W20MultiTaskLoss(nn.Module):
    def __init__(self, lambda_stress: float, *, multi_task: bool = True) -> None:
        super().__init__()
        self.lambda_stress = lambda_stress if multi_task else 0.0
        self.multi_task = multi_task
        self.demand = DemandHuberLoss()
        self.stress = StressMSELoss()

    def forward(self, demand_pred, osi_pred, demand_true, osi_true):
        d_raw = self.demand(demand_pred, demand_true)
        d = d_raw / DEMAND_NORM
        if not self.multi_task:
            total = d
            return total, LossBreakdown(total=float(total.detach()), demand=float(d_raw.detach()), stress=0.0)
        s = self.stress(osi_pred, osi_true)
        total = d + self.lambda_stress * s
        return total, LossBreakdown(
            total=float(total.detach()),
            demand=float(d_raw.detach()),
            stress=float(s.detach()),
        )


def _select_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _early_stop_score(demand_mae: float, stress_mae: float, *, spec: AblationSpec) -> float:
    if not W20["balanced_early_stop"] or not spec.multi_task:
        return demand_mae
    return 0.7 * (demand_mae / DEMAND_NORM) + 0.3 * stress_mae


def _build_model(spec: AblationSpec) -> nn.Module:
    if spec.structural in {"A2", "A3", "A4"}:
        return AblationPFSTGT(spec.structural)
    return PFSTGT()


def _collect_predictions(
    model: nn.Module,
    loader: DataLoader,
    device: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    model.eval()
    d_true, d_pred, s_true, s_pred = [], [], [], []
    with torch.no_grad():
        for batch in loader:
            batch = {k: v.to(device) if torch.is_tensor(v) else v for k, v in batch.items()}
            out = model(
                batch["node_features"],
                batch["global_features"],
                batch["adjacency"],
                attention_bias=batch["attention_bias"],
            )
            d_true.append(batch["demand_target"].cpu().numpy())
            d_pred.append(out.demand_pred.cpu().numpy())
            s_true.append(batch["osi_target"].cpu().numpy())
            s_pred.append(out.osi_pred.cpu().numpy())
    return (
        np.concatenate(d_true),
        np.concatenate(d_pred),
        np.concatenate(s_true),
        np.concatenate(s_pred),
    )


def _evaluate_test(
    model: nn.Module,
    coordinator: FoundationCoordinator,
    device: str,
    *,
    multi_task: bool = True,
) -> dict[str, Any]:
    loader = DataLoader(
        SmartGridTorchDataset("test", coordinator),
        batch_size=32,
        collate_fn=collate_smartgrid_batch,
    )
    y_d, p_d, y_s, p_s = _collect_predictions(model, loader, device)
    dm = compute_demand_metrics(y_d, p_d, region_names=REGIONS)
    if multi_task:
        sm = compute_stress_metrics(y_s, p_s)
        stress = {"stress_mae": sm.mae, "stress_rmse": sm.rmse, "stress_r2": sm.r2}
    else:
        stress = {"stress_mae": float("nan"), "stress_rmse": float("nan"), "stress_r2": float("nan")}
    per_sample = np.abs(y_d - p_d).mean(axis=1)
    return {
        "demand_mae": dm.mae,
        "demand_rmse": dm.rmse,
        "demand_mape": dm.mape,
        "demand_r2": dm.r2,
        **stress,
        "per_sample_demand_mae": per_sample,
        "per_region_mae": dm.per_region_mae,
    }


def _train_ablation(spec: AblationSpec, device: str) -> dict[str, Any]:
    coordinator = FoundationCoordinator(verify_md5=True, graph_variant=spec.graph_variant)
    config = TrainingConfig(
        seed=SEED,
        device=device,
        lambda_stress=W20["lambda_stress"],
        checkpoint_root=CKPT_ROOT,
        benchmark_id=spec.ablation_id,
        max_epochs=200,
    )
    set_seed(SEED)
    model = _build_model(spec).to(device)
    loss_fn = W20MultiTaskLoss(W20["lambda_stress"], multi_task=spec.multi_task)
    trainer = Trainer(model, config, loss_fn)
    validator = Validator(model, config, loss_fn)
    early = EarlyStopping(patience=config.early_stop_patience, min_delta=0.001)
    ckpt = CheckpointManager(config)
    loaders = build_dataloaders(coordinator, config)

    start = time.perf_counter()
    best_score = float("inf")
    stopped_early = False
    epochs_run = 0

    for epoch in range(1, config.max_epochs + 1):
        trainer.train_epoch(loaders["train"])
        val_metrics = validator.validate(loaders["validation"])
        trainer.step_scheduler(val_metrics.demand.mae)
        score = _early_stop_score(val_metrics.demand.mae, val_metrics.stress.mae, spec=spec)
        stop = early.step(score)
        if stop.improved:
            ckpt.save_best(
                model,
                trainer.optimizer,
                epoch,
                {
                    "demand_mae": val_metrics.demand.mae,
                    "stress_mae": val_metrics.stress.mae,
                    "stress_r2": val_metrics.stress.r2,
                },
            )
        epochs_run = epoch
        if stop.should_stop:
            stopped_early = True
            break

    if ckpt.has_checkpoint():
        ckpt.load(model, trainer.optimizer)

    test = _evaluate_test(model, coordinator, device, multi_task=spec.multi_task)
    elapsed = time.perf_counter() - start

    return {
        "ablation_id": spec.ablation_id,
        "model_name": spec.name,
        "graph_variant": spec.graph_variant.value,
        "multi_task": spec.multi_task,
        "epochs_run": epochs_run,
        "stopped_early": stopped_early,
        "training_seconds": elapsed,
        "checkpoint": str(config.best_checkpoint_path()),
        **{k: v for k, v in test.items() if k != "per_region_mae"},
        "per_region_mae": test["per_region_mae"],
    }


def _load_a1_reference(device: str) -> dict[str, Any]:
    spec = ABLATIONS[0]
    coordinator = FoundationCoordinator(verify_md5=True, graph_variant=GraphVariant.HYBRID)
    model = PFSTGT().to(device)
    payload = torch.load(W20_CKPT, map_location=device, weights_only=False)
    model.load_state_dict(payload["model_state_dict"])
    test = _evaluate_test(model, coordinator, device)
    return {
        "ablation_id": "A1",
        "model_name": spec.name,
        "graph_variant": "hybrid",
        "multi_task": True,
        "epochs_run": 0,
        "stopped_early": False,
        "training_seconds": 0.0,
        "checkpoint": str(W20_CKPT),
        "from_checkpoint": True,
        **{k: v for k, v in test.items() if k != "per_region_mae"},
        "per_region_mae": test["per_region_mae"],
    }


def _wilcoxon_rows(
    a1_mae: np.ndarray,
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for row in results:
        if row["ablation_id"] == "A1":
            continue
        other = row["per_sample_demand_mae"]
        diff = other - a1_mae  # positive => ablation worse than A1
        stat, p_two = stats.wilcoxon(diff, alternative="two-sided", zero_method="wilcox")
        p_worse = stats.wilcoxon(diff, alternative="greater", zero_method="wilcox").pvalue
        rng = np.random.default_rng(SEED)
        boots = []
        n = len(diff)
        for _ in range(2000):
            idx = rng.integers(0, n, n)
            boots.append(float(np.mean(diff[idx])))
        lo, hi = np.percentile(boots, [2.5, 97.5])
        rows.append(
            {
                "comparison": f"A1 vs {row['ablation_id']}",
                "ablation_name": row["model_name"],
                "median_mae_diff_mw": float(np.median(diff)),
                "mean_mae_diff_mw": float(np.mean(diff)),
                "wilcoxon_stat": float(stat),
                "p_value_two_sided": float(p_two),
                "p_value_ablation_worse": float(p_worse),
                "bonferroni_significant_0.01": float(p_worse) < BONFERRONI_ALPHA and np.median(diff) > 0,
                "bootstrap_95ci_mae_diff": f"[{lo:.2f}, {hi:.2f}]",
            }
        )
    return rows


def _contribution_rows(a1: dict[str, Any], results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ref_mae = a1["demand_mae"]
    ref_r2 = a1["demand_r2"]
    mapping = {
        "Graph module": "A2",
        "Transformer module": "A3",
        "Multi-task learning": "A4",
        "Hybrid graph (vs geo-only)": "A5",
        "Hybrid graph (vs corr-only)": "A6",
    }
    rows = []
    by_id = {r["ablation_id"]: r for r in results}
    for component, aid in mapping.items():
        v = by_id[aid]
        delta_mae = v["demand_mae"] - ref_mae
        delta_r2 = ref_r2 - v["demand_r2"]
        rows.append(
            {
                "component": component,
                "ablation_id": aid,
                "delta_mae_mw": delta_mae,
                "relative_degradation_pct": delta_mae / ref_mae * 100.0,
                "delta_r2": delta_r2,
                "stress_delta_mae": v["stress_mae"] - a1["stress_mae"] if aid != "A4" else float("nan"),
                "verdict": "Supports component" if delta_mae > 0 else "No measurable benefit",
            }
        )
    return rows


def _write_reports(
    results: list[dict[str, Any]],
    stats_rows: list[dict[str, Any]],
    contrib_rows: list[dict[str, Any]],
) -> None:
    today = datetime.now(timezone.utc).date().isoformat()
    a1 = next(r for r in results if r["ablation_id"] == "A1")

    df = pd.DataFrame(
        [
            {
                "ablation_id": r["ablation_id"],
                "model_name": r["model_name"],
                "graph_variant": r["graph_variant"],
                "multi_task": r["multi_task"],
                "demand_mae": r["demand_mae"],
                "demand_rmse": r["demand_rmse"],
                "demand_mape": r["demand_mape"],
                "demand_r2": r["demand_r2"],
                "stress_mae": r["stress_mae"],
                "stress_rmse": r["stress_rmse"],
                "stress_r2": r["stress_r2"],
            }
            for r in results
        ]
    )
    df.to_csv(OUTPUT_DIR / "ablation_results.csv", index=False)

    ranked = df.sort_values("demand_mae").reset_index(drop=True)
    ranked["demand_rank"] = ranked["demand_mae"].rank(method="min").astype(int)
    stress_ranked = ranked[ranked["ablation_id"] != "A4"].copy()
    stress_ranked["stress_rank"] = stress_ranked["stress_mae"].rank(method="min").astype(int)

    stats_df = pd.DataFrame(stats_rows)
    contrib_df = pd.DataFrame(contrib_rows)

    def md(df_in: pd.DataFrame) -> str:
        return df_in.to_markdown(index=False) if hasattr(df_in, "to_markdown") else df_in.to_string()

    (OUTPUT_DIR / "ablation_rankings.md").write_text(
        "\n".join(
            [
                "# Ablation Rankings — Experiment 03",
                "",
                f"Generated: {today}",
                "",
                "## Demand (test, rank by MAE)",
                "",
                "| Rank | ID | Model | MAE | RMSE | MAPE | R² |",
                "| --- | --- | --- | --- | --- | --- | --- |",
                *[
                    f"| {int(row.demand_rank)} | {row.ablation_id} | {row.model_name} | "
                    f"{row.demand_mae:.2f} | {row.demand_rmse:.2f} | {row.demand_mape:.2f} | {row.demand_r2:.4f} |"
                    for _, row in ranked.iterrows()
                ],
                "",
                "## Stress (test, rank by MAE; A4 N/A)",
                "",
                "| Rank | ID | Model | MAE | RMSE | R² |",
                "| --- | --- | --- | --- | --- | --- |",
                *[
                    f"| {int(row.stress_rank)} | {row.ablation_id} | {row.model_name} | "
                    f"{row.stress_mae:.4f} | {row.stress_rmse:.4f} | {row.stress_r2:.4f} |"
                    for _, row in stress_ranked.sort_values("stress_mae").iterrows()
                ],
                "",
                f"**Reference (A1):** {a1['model_name']} — demand MAE {a1['demand_mae']:.2f} MW",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (OUTPUT_DIR / "component_contribution.md").write_text(
        "\n".join(
            [
                "# Component Contribution — Experiment 03",
                "",
                f"Generated: {today}",
                "",
                "ΔMAE = ablation MAE − A1 MAE (positive ⇒ removing/changing component hurts).",
                "ΔR² = A1 R² − ablation R² (positive ⇒ component helps variance explanation).",
                "",
                md(contrib_df.round(4)),
                "",
                "## Summary",
                "",
                f"- **Graph module (A2):** ΔMAE = {contrib_df.loc[contrib_df.component.str.contains('Graph module'), 'delta_mae_mw'].iloc[0]:+.2f} MW",
                f"- **Transformer (A3):** ΔMAE = {contrib_df.loc[contrib_df.component.str.contains('Transformer'), 'delta_mae_mw'].iloc[0]:+.2f} MW",
                f"- **Multi-task (A4):** ΔMAE = {contrib_df.loc[contrib_df.component.str.contains('Multi-task'), 'delta_mae_mw'].iloc[0]:+.2f} MW",
                f"- **Hybrid vs geo-only (A5):** ΔMAE = {contrib_df.loc[contrib_df.component.str.contains('geo-only'), 'delta_mae_mw'].iloc[0]:+.2f} MW",
                f"- **Hybrid vs corr-only (A6):** ΔMAE = {contrib_df.loc[contrib_df.component.str.contains('corr-only'), 'delta_mae_mw'].iloc[0]:+.2f} MW",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (OUTPUT_DIR / "statistical_significance.md").write_text(
        "\n".join(
            [
                "# Statistical Significance — Experiment 03",
                "",
                f"Generated: {today}",
                "",
                "Wilcoxon signed-rank on per-sample macro demand MAE (test set).",
                f"Bonferroni-adjusted α = {BONFERRONI_ALPHA} for 5 comparisons vs A1 (Phase 13).",
                "",
                md(stats_df.round(6)),
                "",
            ]
        ),
        encoding="utf-8",
    )

    (OUTPUT_DIR / "ablation_summary.md").write_text(
        "\n".join(
            [
                "# Ablation Summary — Experiment 03",
                "",
                f"Generated: {today}",
                "",
                "## Protocol",
                "",
                "- Reference: **A1 PF-STGT W20** (Experiment 01B checkpoint, not retrained)",
                "- Ablations A2–A6 trained with W20 settings (λ₂=20, demand÷100, balanced ES)",
                "- Seed 42, identical chronological splits, Phase 15 metrics",
                "- A5: geographical graph only; A6: correlation graph only (τ=0.65)",
                "",
                "## Reference performance (A1, test)",
                "",
                f"- Demand MAE: {a1['demand_mae']:.2f} MW | R²: {a1['demand_r2']:.4f}",
                f"- Stress MAE: {a1['stress_mae']:.4f} | R²: {a1['stress_r2']:.4f}",
                "",
                "## Best ablation variant (demand MAE)",
                "",
                f"**{ranked.iloc[0].model_name}** ({ranked.iloc[0].ablation_id}) — {ranked.iloc[0].demand_mae:.2f} MW",
                "",
                "## Component contributions (ΔMAE vs A1)",
                "",
                md(contrib_df[["component", "ablation_id", "delta_mae_mw", "relative_degradation_pct", "verdict"]].round(2)),
                "",
                "## Scope",
                "",
                "- No explainability analyses",
                "",
            ]
        ),
        encoding="utf-8",
    )

    doc = OUTPUT_DIR / "Experiment_03_Ablation_Studies.md"
    base = doc.read_text(encoding="utf-8")
    if "## Execution Record" in base:
        base = base.split("## Execution Record")[0].rstrip()
    doc.write_text(
        base
        + "\n\n---\n\n## Execution Record\n\n"
        + f"**Date:** {today}\n"
        + f"**Reference:** A1 W20 demand MAE {a1['demand_mae']:.2f} MW\n"
        + f"**Script:** `experiments/experiment_03_ablation_studies/run_ablation.py`\n",
        encoding="utf-8",
    )


def regenerate_reports() -> None:
    """Rebuild markdown/csv outputs from saved checkpoints (inference only)."""
    device = _select_device()
    results: list[dict[str, Any]] = []

    for spec in ABLATIONS:
        if spec.use_w20_checkpoint:
            results.append(_load_a1_reference(device))
            continue
        coordinator = FoundationCoordinator(verify_md5=True, graph_variant=spec.graph_variant)
        model = _build_model(spec).to(device)
        ckpt = CKPT_ROOT / spec.ablation_id / f"seed_{SEED}" / "best.pt"
        payload = torch.load(ckpt, map_location=device, weights_only=False)
        model.load_state_dict(payload["model_state_dict"])
        test = _evaluate_test(model, coordinator, device, multi_task=spec.multi_task)
        raw = json.loads((EXP_DIR / "ablation_raw.json").read_text())
        meta = next(r for r in raw if r["ablation_id"] == spec.ablation_id)
        results.append({**meta, **{k: v for k, v in test.items() if k != "per_region_mae"}, "per_region_mae": test["per_region_mae"]})

    a1_mae = results[0]["per_sample_demand_mae"]
    _write_reports(results, _wilcoxon_rows(a1_mae, results), _contribution_rows(results[0], results))
    print("Reports regenerated.", flush=True)


def run_ablation(*, skip_training: bool = False) -> None:
    setup_logging()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CKPT_ROOT.mkdir(parents=True, exist_ok=True)

    if skip_training:
        regenerate_reports()
        return

    device = _select_device()

    results: list[dict[str, Any]] = []

    print("Evaluating A1 (W20 checkpoint)...", flush=True)
    results.append(_load_a1_reference(device))

    for spec in ABLATIONS[1:]:
        print(f"Training {spec.ablation_id} {spec.name}...", flush=True)
        results.append(_train_ablation(spec, device))

    a1_mae = results[0]["per_sample_demand_mae"]
    stats_rows = _wilcoxon_rows(a1_mae, results)
    contrib_rows = _contribution_rows(results[0], results)

    serializable = []
    for r in results:
        row = {k: v for k, v in r.items() if k != "per_sample_demand_mae"}
        serializable.append(row)
    (OUTPUT_DIR / "ablation_raw.json").write_text(json.dumps(serializable, indent=2, default=str))

    _write_reports(results, stats_rows, contrib_rows)
    print("Experiment 03 complete.", flush=True)


if __name__ == "__main__":
    skip = "--reports-only" in sys.argv
    run_ablation(skip_training=skip)
