"""Experiment 02 — benchmark model comparison (B01–B07)."""

from __future__ import annotations

import pickle
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
EXP_DIR = Path(__file__).resolve().parent
CLASSICAL_CACHE = EXP_DIR / "classical_cache.pkl"
CLASSICAL_SCRIPT = EXP_DIR / "train_classical.py"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
sys.path.insert(0, str(EXP_DIR))

from constants import (
    GLOBAL_FEATURES,
    INPUT_WINDOW_T,
    N_NODES,
    NODE_FEATURES_PER_REGION,
    PROJECT_ROOT,
    REGIONS,
)
from foundation import FoundationCoordinator
from utils.logging import setup_logging

OUTPUT_DIR = EXP_DIR
W20_CKPT = (
    PROJECT_ROOT
    / "experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt"
)
DEMAND_NORM = 100.0
SEED = 42


@dataclass
class SplitArrays:
    X_flat: np.ndarray
    node: np.ndarray
    global_: np.ndarray
    y_demand: np.ndarray
    y_osi: np.ndarray


@dataclass
class BenchmarkResult:
    benchmark_id: str
    model_name: str
    split: str
    demand_mae: float
    demand_rmse: float
    demand_mape: float
    demand_r2: float
    stress_mae: float
    stress_rmse: float
    stress_r2: float
    per_sample_demand_mae: np.ndarray | None = None


def _run_classical_subprocess() -> dict[str, Any]:
    if CLASSICAL_CACHE.exists():
        print(f"Loading classical cache from {CLASSICAL_CACHE}", flush=True)
        with CLASSICAL_CACHE.open("rb") as f:
            return pickle.load(f)
    print("Training classical models (B01–B03) in isolated subprocess...", flush=True)
    subprocess.run([sys.executable, str(CLASSICAL_SCRIPT)], check=True)
    with CLASSICAL_CACHE.open("rb") as f:
        return pickle.load(f)


def _classical_to_result(row: dict[str, Any]) -> BenchmarkResult:
    return BenchmarkResult(
        benchmark_id=row["benchmark_id"],
        model_name=row["model_name"],
        split=row["split"],
        demand_mae=row["demand_mae"],
        demand_rmse=row["demand_rmse"],
        demand_mape=row["demand_mape"],
        demand_r2=row["demand_r2"],
        stress_mae=row["stress_mae"],
        stress_rmse=row["stress_rmse"],
        stress_r2=row["stress_r2"],
        per_sample_demand_mae=row.get("per_sample_demand_mae"),
    )


def _build_split_arrays(coordinator: FoundationCoordinator, split: str) -> SplitArrays:
    indices = coordinator.data_result.sample_indices[split]
    flat: list[np.ndarray] = []
    nodes: list[np.ndarray] = []
    globals_: list[np.ndarray] = []
    demands: list[np.ndarray] = []
    osis: list[float] = []
    for sample_idx in indices:
        sample = coordinator.build_sample(split, sample_idx.end_idx)
        node = sample.x_temporal.node_features.astype(np.float32)
        glob = sample.x_temporal.global_features.astype(np.float32)
        flat.append(np.concatenate([node.reshape(-1), glob.reshape(-1)]))
        nodes.append(node)
        globals_.append(glob)
        demands.append(sample.targets.y_demand.values.astype(np.float32))
        osis.append(float(sample.targets.y_osi.value))
    return SplitArrays(
        X_flat=np.stack(flat),
        node=np.stack(nodes),
        global_=np.stack(globals_),
        y_demand=np.stack(demands),
        y_osi=np.asarray(osis, dtype=np.float32).reshape(-1, 1),
    )


def _run_deep_phase(
    coordinator: FoundationCoordinator,
    train: SplitArrays,
    val: SplitArrays,
    test: SplitArrays,
) -> tuple[list[BenchmarkResult], dict[str, np.ndarray]]:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset

    from benchmark_models import SequenceRegressor, TGCN
    from evaluation.metrics import compute_demand_metrics, compute_stress_metrics
    from models.pf_stgt import PFSTGT
    from training.dataset import SmartGridTorchDataset, collate_smartgrid_batch
    from training.early_stopping import EarlyStopping
    from training.losses import DemandHuberLoss, StressMSELoss
    from training.seed import set_seed

    device = "cpu"
    set_seed(SEED)
    adjacency = torch.from_numpy(coordinator.x_graph.adjacency.astype(np.float32))
    adjacency = adjacency / adjacency.sum(dim=-1, keepdim=True).clamp_min(1e-6)
    demand_prior = torch.from_numpy(train.y_demand.mean(axis=0)).float()

    def _init_demand_bias(model: nn.Module) -> None:
        with torch.no_grad():
            model.demand_head.bias.copy_(demand_prior)

    def evaluate_predictions(
        benchmark_id: str,
        model_name: str,
        y_demand: np.ndarray,
        demand_pred: np.ndarray,
        y_osi: np.ndarray,
        osi_pred: np.ndarray,
    ) -> BenchmarkResult:
        demand_metrics = compute_demand_metrics(y_demand, demand_pred, region_names=REGIONS)
        stress_metrics = compute_stress_metrics(y_osi, osi_pred)
        return BenchmarkResult(
            benchmark_id=benchmark_id,
            model_name=model_name,
            split="test",
            demand_mae=demand_metrics.mae,
            demand_rmse=demand_metrics.rmse,
            demand_mape=demand_metrics.mape,
            demand_r2=demand_metrics.r2,
            stress_mae=stress_metrics.mae,
            stress_rmse=stress_metrics.rmse,
            stress_r2=stress_metrics.r2,
            per_sample_demand_mae=np.abs(y_demand - demand_pred).mean(axis=1),
        )

    def make_sequence_tensor(node: np.ndarray, global_: np.ndarray) -> torch.Tensor:
        batch_size = node.shape[0]
        seq = []
        for t in range(INPUT_WINDOW_T):
            step = np.concatenate([node[:, t].reshape(batch_size, -1), global_[:, t]], axis=1)
            seq.append(step)
        return torch.from_numpy(np.stack(seq, axis=1)).float()

    def train_deep_baseline(
        benchmark_id: str,
        model_name: str,
        model: nn.Module,
    ) -> BenchmarkResult:
        _init_demand_bias(model)
        model.to(device)
        demand_loss = DemandHuberLoss()
        stress_loss = StressMSELoss()
        optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", factor=0.5, patience=5
        )
        early = EarlyStopping(patience=15, min_delta=0.01)

        train_seq = make_sequence_tensor(train.node, train.global_)
        val_seq = make_sequence_tensor(val.node, val.global_)
        test_seq = make_sequence_tensor(test.node, test.global_)

        def forward_batch(seq_b, node_b, glob_b):
            if isinstance(model, TGCN):
                return model(node_b, glob_b, adjacency.to(device))
            return model(seq_b)

        def predict_split(seq, node, glob) -> tuple[np.ndarray, np.ndarray]:
            model.eval()
            preds_d, preds_s = [], []
            with torch.no_grad():
                loader = DataLoader(
                    TensorDataset(seq, torch.from_numpy(node), torch.from_numpy(glob)),
                    batch_size=32,
                )
                for seq_b, node_b, glob_b in loader:
                    seq_b = seq_b.to(device)
                    node_b = node_b.to(device)
                    glob_b = glob_b.to(device)
                    od, os_ = forward_batch(seq_b, node_b, glob_b)
                    preds_d.append(od.cpu().numpy())
                    preds_s.append(os_.cpu().numpy())
            return np.concatenate(preds_d, axis=0), np.concatenate(preds_s, axis=0)

        best_state = None
        for _ in range(1, 61):
            model.train()
            loader = DataLoader(
                TensorDataset(
                    train_seq,
                    torch.from_numpy(train.node),
                    torch.from_numpy(train.global_),
                    torch.from_numpy(train.y_demand),
                ),
                batch_size=32,
                shuffle=True,
            )
            for seq_b, node_b, glob_b, yd_b in loader:
                seq_b = seq_b.to(device)
                node_b = node_b.to(device)
                glob_b = glob_b.to(device)
                yd_b = yd_b.to(device)
                optimizer.zero_grad(set_to_none=True)
                out_d, _ = forward_batch(seq_b, node_b, glob_b)
                loss = demand_loss(out_d, yd_b)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()

            d_pred, _ = predict_split(val_seq, val.node, val.global_)
            val_mae = float(compute_demand_metrics(val.y_demand, d_pred).mae)
            scheduler.step(val_mae)
            stop_state = early.step(val_mae)
            if stop_state.improved:
                best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            if stop_state.should_stop:
                break

        if best_state:
            model.load_state_dict(best_state)

        for param in model.parameters():
            param.requires_grad = False
        for param in model.stress_head.parameters():
            param.requires_grad = True
        stress_optimizer = torch.optim.AdamW(model.stress_head.parameters(), lr=1e-3)
        stress_loader = DataLoader(
            TensorDataset(
                train_seq,
                torch.from_numpy(train.node),
                torch.from_numpy(train.global_),
                torch.from_numpy(train.y_osi),
            ),
            batch_size=32,
            shuffle=True,
        )
        for _ in range(30):
            model.train()
            for seq_b, node_b, glob_b, ys_b in stress_loader:
                seq_b = seq_b.to(device)
                node_b = node_b.to(device)
                glob_b = glob_b.to(device)
                ys_b = ys_b.to(device)
                stress_optimizer.zero_grad(set_to_none=True)
                _, out_s = forward_batch(seq_b, node_b, glob_b)
                loss = stress_loss(out_s, ys_b)
                loss.backward()
                stress_optimizer.step()

        d_pred, s_pred = predict_split(test_seq, test.node, test.global_)
        return evaluate_predictions(
            benchmark_id,
            model_name,
            test.y_demand,
            d_pred,
            test.y_osi,
            s_pred,
        )

    def evaluate_pf_stgt_w20() -> BenchmarkResult:
        model = PFSTGT()
        payload = torch.load(W20_CKPT, map_location=device, weights_only=False)
        model.load_state_dict(payload["model_state_dict"])
        model.to(device)
        model.eval()

        loader = DataLoader(
            SmartGridTorchDataset("test", coordinator),
            batch_size=32,
            collate_fn=collate_smartgrid_batch,
        )
        d_preds, s_preds, d_true, s_true = [], [], [], []
        with torch.no_grad():
            for batch in loader:
                batch = {k: v.to(device) if torch.is_tensor(v) else v for k, v in batch.items()}
                out = model(
                    batch["node_features"],
                    batch["global_features"],
                    batch["adjacency"],
                    attention_bias=batch["attention_bias"],
                )
                d_preds.append(out.demand_pred.cpu().numpy())
                s_preds.append(out.osi_pred.cpu().numpy())
                d_true.append(batch["demand_target"].cpu().numpy())
                s_true.append(batch["osi_target"].cpu().numpy())
        return evaluate_predictions(
            "B07",
            "PF-STGT (W20)",
            np.concatenate(d_true),
            np.concatenate(d_preds),
            np.concatenate(s_true),
            np.concatenate(s_preds),
        )

    results: list[BenchmarkResult] = []
    per_sample: dict[str, np.ndarray] = {}
    input_dim = N_NODES * NODE_FEATURES_PER_REGION + GLOBAL_FEATURES

    print("Training B04 LSTM...", flush=True)
    r = train_deep_baseline("B04", "LSTM", SequenceRegressor(input_dim, cell="lstm"))
    results.append(r)
    per_sample["B04"] = r.per_sample_demand_mae

    print("Training B05 GRU...", flush=True)
    r = train_deep_baseline("B05", "GRU", SequenceRegressor(input_dim, cell="gru"))
    results.append(r)
    per_sample["B05"] = r.per_sample_demand_mae

    print("Training B06 T-GCN...", flush=True)
    r = train_deep_baseline("B06", "T-GCN", TGCN(NODE_FEATURES_PER_REGION, GLOBAL_FEATURES))
    results.append(r)
    per_sample["B06"] = r.per_sample_demand_mae

    print("Evaluating B07 PF-STGT (W20)...", flush=True)
    r = evaluate_pf_stgt_w20()
    results.append(r)
    per_sample["B07"] = r.per_sample_demand_mae

    return results, per_sample


def _wilcoxon_tests(b07_mae: np.ndarray, others: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bid, mae in others.items():
        diff = b07_mae - mae
        stat, p_two = stats.wilcoxon(diff, alternative="two-sided", zero_method="wilcox")
        p_b07_better = stats.wilcoxon(diff, alternative="less", zero_method="wilcox").pvalue
        d = float(np.mean(diff) / (np.std(diff, ddof=1) + 1e-12))
        rows.append(
            {
                "comparison": f"B07 vs {bid}",
                "median_mae_diff_mw": float(np.median(diff)),
                "wilcoxon_stat": float(stat),
                "p_value_two_sided": float(p_two),
                "p_value_b07_better_one_sided": float(p_b07_better),
                "cohens_d": d,
                "bonferroni_significant_0.0083": float(p_b07_better) < 0.0083 and np.median(diff) < 0,
            }
        )
    return rows


def _bootstrap_ci(a: np.ndarray, b: np.ndarray, n: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    diffs = []
    n_samples = len(a)
    for _ in range(n):
        idx = rng.integers(0, n_samples, n_samples)
        diffs.append(float(np.mean(a[idx] - b[idx])))
    low, high = np.percentile(diffs, [2.5, 97.5])
    return float(low), float(high)


def _write_reports(results: list[BenchmarkResult], stats_rows: list[dict[str, Any]]) -> dict[str, Any]:
    df = pd.DataFrame(
        [
            {
                "benchmark_id": r.benchmark_id,
                "model_name": r.model_name,
                "split": r.split,
                "demand_mae": r.demand_mae,
                "demand_rmse": r.demand_rmse,
                "demand_mape": r.demand_mape,
                "demand_r2": r.demand_r2,
                "stress_mae": r.stress_mae,
                "stress_rmse": r.stress_rmse,
                "stress_r2": r.stress_r2,
            }
            for r in results
        ]
    )
    df = df.sort_values("benchmark_id").reset_index(drop=True)
    df.to_csv(OUTPUT_DIR / "benchmark_results.csv", index=False)

    ranked = df.sort_values(["demand_mae", "stress_mae"]).reset_index(drop=True)
    ranked["demand_rank"] = ranked["demand_mae"].rank(method="min").astype(int)
    ranked["stress_rank"] = ranked["stress_mae"].rank(method="min").astype(int)
    best = ranked.iloc[0]

    (OUTPUT_DIR / "benchmark_rankings.md").write_text(
        "\n".join(
            [
                "# Benchmark Rankings — Experiment 02",
                "",
                "## Demand forecasting (test, primary rank by MAE)",
                "",
                "| Rank | ID | Model | MAE | RMSE | MAPE | R² |",
                "| --- | --- | --- | --- | --- | --- | --- |",
                *[
                    f"| {int(row.demand_rank)} | {row.benchmark_id} | {row.model_name} | "
                    f"{row.demand_mae:.2f} | {row.demand_rmse:.2f} | {row.demand_mape:.2f} | {row.demand_r2:.4f} |"
                    for _, row in ranked.iterrows()
                ],
                "",
                "## Stress forecasting (test, rank by MAE)",
                "",
                "| Rank | ID | Model | MAE | RMSE | R² |",
                "| --- | --- | --- | --- | --- | --- |",
                *[
                    f"| {int(row.stress_rank)} | {row.benchmark_id} | {row.model_name} | "
                    f"{row.stress_mae:.4f} | {row.stress_rmse:.4f} | {row.stress_r2:.4f} |"
                    for _, row in ranked.sort_values("stress_mae").iterrows()
                ],
                "",
                f"**Best overall (demand MAE):** {best.model_name} ({best.benchmark_id})",
                "",
            ]
        )
    )

    (OUTPUT_DIR / "benchmark_summary.md").write_text(
        "\n".join(
            [
                "# Benchmark Summary — Experiment 02",
                "",
                f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
                "",
                "## Protocol",
                "",
                "- Identical chronological train/validation/test splits (Sprint 01)",
                "- Identical targets and features",
                "- Seed 42 for all models",
                "- Classical models (B01–B03) trained without PyTorch loaded",
                "- PF-STGT uses Experiment 01B W20 checkpoint (not retrained)",
                "",
                f"## Best model (demand MAE): **{best.model_name}** ({best.benchmark_id})",
                "",
                f"- Test demand MAE: {best.demand_mae:.2f} MW",
                f"- Test demand R²: {best.demand_r2:.4f}",
                "",
                "## PF-STGT (B07 W20)",
                "",
            ]
            + [
                line
                for _, row in df[df.benchmark_id == "B07"].iterrows()
                for line in [
                    f"- Demand MAE: {row.demand_mae:.2f} MW, R²: {row.demand_r2:.4f}",
                    f"- Stress MAE: {row.stress_mae:.4f}, R²: {row.stress_r2:.4f}",
                ]
            ]
            + ["", "## Scope", "", "- No ablations or explainability", ""]
        )
    )

    stats_df = pd.DataFrame(stats_rows)
    stats_md = stats_df.to_markdown(index=False) if hasattr(stats_df, "to_markdown") else stats_df.to_string()
    (OUTPUT_DIR / "statistical_significance.md").write_text(
        "\n".join(
            [
                "# Statistical Significance — Experiment 02",
                "",
                "Wilcoxon signed-rank test on per-sample macro demand MAE (test set).",
                "Bonferroni-adjusted α = 0.0083 for 6 comparisons (Phase 15).",
                "",
                stats_md,
                "",
            ]
        )
    )

    perf = ranked[
        [
            "benchmark_id",
            "model_name",
            "demand_mae",
            "demand_rmse",
            "demand_mape",
            "demand_r2",
            "stress_mae",
            "stress_rmse",
            "stress_r2",
        ]
    ]
    perf_md = perf.to_markdown(index=False) if hasattr(perf, "to_markdown") else perf.to_string()
    (OUTPUT_DIR / "performance_tables.md").write_text(
        "\n".join(
            [
                "# Performance Tables — Experiment 02",
                "",
                "## Table 1 — Test-set benchmark results",
                "",
                perf_md,
                "",
            ]
        )
    )

    doc = OUTPUT_DIR / "Experiment_02_Benchmark_Models.md"
    base = doc.read_text(encoding="utf-8")
    if "## Execution Record" in base:
        base = base.split("## Execution Record")[0].rstrip()
    doc.write_text(
        base
        + "\n\n---\n\n## Execution Record\n\n"
        + f"**Date:** {datetime.now(timezone.utc).date().isoformat()}\n"
        + f"**Best model:** {best.model_name} ({best.benchmark_id})\n"
        + f"**Script:** `experiments/experiment_02_benchmark_models/run_benchmark.py`\n",
        encoding="utf-8",
    )

    return {"best_id": best.benchmark_id, "best_name": best.model_name, "ranked": ranked}


def run_benchmark(*, refresh_classical: bool = False) -> None:
    setup_logging()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if refresh_classical and CLASSICAL_CACHE.exists():
        CLASSICAL_CACHE.unlink()

    classical = _run_classical_subprocess()
    classical_results = [_classical_to_result(r) for r in classical["results"]]
    per_sample: dict[str, np.ndarray] = dict(classical["per_sample"])

    coordinator = FoundationCoordinator(verify_md5=True)
    train = _build_split_arrays(coordinator, "train")
    val = _build_split_arrays(coordinator, "validation")
    test = _build_split_arrays(coordinator, "test")

    deep_results, deep_per_sample = _run_deep_phase(coordinator, train, val, test)
    per_sample.update(deep_per_sample)

    results = classical_results + deep_results
    b07_mae = per_sample["B07"]
    others = {k: v for k, v in per_sample.items() if k != "B07"}
    stats_rows = _wilcoxon_tests(b07_mae, others)
    for row in stats_rows:
        bid = row["comparison"].split()[-1]
        if bid in per_sample:
            lo, hi = _bootstrap_ci(b07_mae, per_sample[bid])
            row["bootstrap_95ci_mae_diff"] = f"[{lo:.2f}, {hi:.2f}]"

    meta = _write_reports(results, stats_rows)
    print(f"Experiment 02 complete. Best model: {meta['best_name']} ({meta['best_id']})")


if __name__ == "__main__":
    refresh = "--refresh-classical" in sys.argv
    run_benchmark(refresh_classical=refresh)
