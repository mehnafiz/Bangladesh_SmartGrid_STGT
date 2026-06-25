"""Phase 11 — Hyperparameter Optimization Strategy.

Designs a reproducible, computationally feasible HPO protocol for PF-STGT (B07).
Freezes search space, parameter ranges, optimization methodology, budget, and
model selection protocol.

Does NOT implement models, train models, or modify locked phase outputs.

Inputs (read-only):
    architecture/
    experiments/  (Phase 10 protocol)

Outputs:
    optimization/  (5 deliverables)
    results/phases/phase_11_hyperparameter_optimization/  (2 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OPT_DIR = ROOT / "optimization"
REPORT_DIR = ROOT / "results" / "phases" / "phase_11_hyperparameter_optimization"
EXP_DIR = ROOT / "experiments"
ARCH_DIR = ROOT / "architecture"
FEATURES_PATH = ROOT / "data" / "features" / "train_features.parquet"

# ── Fixed (not searched) ───────────────────────────────────────────────────
FIXED = {
    "lookback_window_T": 7,
    "forecast_horizon_H": 1,
    "num_nodes": 9,
    "num_tasks": 2,
    "graph_strategy": "Hybrid (Phase 08 adjacency)",
    "optimizer": "AdamW",
    "scheduler": "ReduceLROnPlateau(factor=0.5, patience=5)",
    "early_stopping_patience": 15,
    "max_epochs": 200,
    "grad_clip_norm": 1.0,
    "lambda_demand": 1.0,
    "lambda_stress": 0.5,
    "huber_delta_mw": 1.0,
    "primary_seed_hpo": 42,
    "final_seeds": [42, 123, 456],
}

# ── Frozen HPO decisions ───────────────────────────────────────────────────
OPTIMIZATION_METHOD = "Random Search (seeded, validation-only)"
N_STAGE1_TRIALS = 20
N_FINALIST_CONFIGS = 3
N_FINAL_SEEDS = 3
PRIMARY_METRIC = "validation_macro_demand_MAE"
SECONDARY_METRIC = "validation_stress_MAE"


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parameter_ranges_df() -> pd.DataFrame:
    rows = [
        # Graph module
        {"module": "graph", "parameter": "num_graph_layers", "symbol": "L_s",
         "type": "integer", "range_min": 1, "range_max": 3, "candidates": "1, 2, 3",
         "default_phase09": 2, "justification": "9-node graph; depth 1–3 avoids over-smoothing on small N"},
        {"module": "graph", "parameter": "graph_hidden_dim", "symbol": "d_model",
         "type": "integer", "range_min": 64, "range_max": 192, "candidates": "64, 128, 192",
         "default_phase09": 128, "justification": "~1,287 train windows; cap capacity vs overfit"},
        {"module": "graph", "parameter": "graph_dropout", "symbol": "p_g",
         "type": "float", "range_min": 0.1, "range_max": 0.3, "candidates": "0.1, 0.2, 0.3",
         "default_phase09": 0.1, "justification": "Regularise graph attention on 24-edge hybrid graph"},
        # Transformer module
        {"module": "transformer", "parameter": "num_transformer_layers", "symbol": "L_t",
         "type": "integer", "range_min": 1, "range_max": 3, "candidates": "1, 2, 3",
         "default_phase09": 2, "justification": "T=7 window; 1–3 layers cover weekly pattern depth"},
        {"module": "transformer", "parameter": "num_attention_heads", "symbol": "H",
         "type": "integer", "range_min": 2, "range_max": 8, "candidates": "2, 4, 8",
         "default_phase09": 4, "justification": "Must divide d_model; constrained sampling in HPO"},
        {"module": "transformer", "parameter": "transformer_dropout", "symbol": "p_t",
         "type": "float", "range_min": 0.1, "range_max": 0.3, "candidates": "0.1, 0.2, 0.3",
         "default_phase09": 0.1, "justification": "Match graph dropout band for balanced regularisation"},
        # Training
        {"module": "training", "parameter": "learning_rate", "symbol": "lr",
         "type": "float", "range_min": 1e-4, "range_max": 1e-3, "candidates": "1e-4, 5e-4, 1e-3",
         "default_phase09": 5e-4, "justification": "Phase 10 grid; stable for AdamW on small batches"},
        {"module": "training", "parameter": "weight_decay", "symbol": "wd",
         "type": "float", "range_min": 1e-5, "range_max": 1e-3, "candidates": "1e-5, 1e-4, 1e-3",
         "default_phase09": 1e-4, "justification": "AdamW decoupled L2; log-spaced regularisation band"},
        {"module": "training", "parameter": "batch_size", "symbol": "B",
         "type": "integer", "range_min": 16, "range_max": 64, "candidates": "16, 32, 64",
         "default_phase09": 32, "justification": "~40 steps/epoch at B=32; memory-safe for 9×7×9 tensor"},
    ]
    return pd.DataFrame(rows)


def optimization_method_comparison() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "method": "Grid Search",
            "trials_needed": 3**9,
            "reproducibility": 5,
            "val_efficiency": 1,
            "implementation_complexity": 2,
            "small_data_suitability": 2,
            "total_score": 10,
            "selected": False,
            "verdict": "Full Cartesian product infeasible; overfits validation with 19k+ configs.",
        },
        {
            "method": "Random Search",
            "trials_needed": N_STAGE1_TRIALS,
            "reproducibility": 5,
            "val_efficiency": 4,
            "implementation_complexity": 4,
            "small_data_suitability": 4,
            "total_score": 21,
            "selected": True,
            "verdict": "Seeded sampling over constrained space; reproducible and adequate for ~1.3k train windows.",
        },
        {
            "method": "Bayesian Optimization (TPE)",
            "trials_needed": 15,
            "reproducibility": 3,
            "val_efficiency": 5,
            "implementation_complexity": 3,
            "small_data_suitability": 3,
            "total_score": 17,
            "selected": False,
            "verdict": "Efficient but Optuna/version sensitivity; val set too small (277 rows) for surrogate overfit risk.",
        },
    ])


def write_search_space(ranges: pd.DataFrame) -> None:
    lines = [
        "# Hyperparameter Search Space — Phase 11",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        f"Target model: **PF-STGT (B07)**",
        "",
        "## Fixed parameters (not searched)",
        "",
        "| Parameter | Value | Source |",
        "| --- | --- | --- |",
    ]
    for k, v in FIXED.items():
        if k in ("final_seeds",):
            continue
        lines.append(f"| `{k}` | {v} | Phase 09/10 |")
    lines += [
        "",
        "## Searchable parameters (9 dimensions)",
        "",
        ranges[["module", "parameter", "symbol", "candidates", "default_phase09", "justification"]].to_markdown(index=False),
        "",
        "## Sampling constraints",
        "",
        "1. **`num_attention_heads` must divide `graph_hidden_dim`** — invalid combos rejected and resampled.",
        "2. **`graph_hidden_dim` ∈ {64, 128, 192}** — paired with compatible head counts only.",
        "3. **Dropout** sampled independently from {0.1, 0.2, 0.3} for graph and transformer modules.",
        "4. **Loss weights λ1, λ2** fixed at 1.0 / 0.5 (Phase 10); not searched to limit val overfitting.",
        "",
        "## Effective search space size",
        "",
        "- Raw Cartesian: 3⁹ = 19,683 combinations (infeasible).",
        f"- **Protocol:** {N_STAGE1_TRIALS} random valid trials + top-{N_FINALIST_CONFIGS} finalist confirmation.",
        "",
        "## Baseline models (B01–B06)",
        "",
        "Use **fixed small grids** from Phase 10 `training_strategy.md`; no joint HPO with PF-STGT. ",
        "PF-STGT tuned config compared against Phase 10 default baselines on identical splits.",
        "",
    ]
    (OPT_DIR / "search_space.md").write_text("\n".join(lines))


def write_optimization_strategy(methods: pd.DataFrame) -> None:
    winner = methods[methods["selected"]].iloc[0]
    lines = [
        "# Optimization Strategy — Phase 11",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Method comparison",
        "",
        methods.to_markdown(index=False),
        "",
        f"## Selected: **{OPTIMIZATION_METHOD}** (score {int(winner['total_score'])}/25)",
        "",
        winner["verdict"],
        "",
        "## Two-stage protocol",
        "",
        "### Stage 1 — Exploration (HPO)",
        "",
        f"| Setting | Value |",
        f"| --- | --- |",
        f"| Trials | {N_STAGE1_TRIALS} |",
        f"| Seed | {FIXED['primary_seed_hpo']} (trial sampler) |",
        f"| Data | Train split only for fitting; **validation for scoring** |",
        f"| Epochs | Up to {FIXED['max_epochs']} with early stopping (patience {FIXED['early_stopping_patience']}) |",
        f"| Metric | {PRIMARY_METRIC} |",
        "",
        "Procedure:",
        "",
        "1. Sample 20 valid hyperparameter vectors uniformly from discrete candidates.",
        "2. Train PF-STGT from scratch per trial (single seed 42).",
        "3. Record validation macro demand MAE and stress MAE.",
        "4. Rank trials; select **top-3** configs as finalists.",
        "",
        "### Stage 2 — Confirmation (finalist stability)",
        "",
        f"| Setting | Value |",
        f"| --- | --- |",
        f"| Configs | Top {N_FINALIST_CONFIGS} from Stage 1 |",
        f"| Seeds | {FIXED['final_seeds']} per config |",
        f"| Runs | {N_FINALIST_CONFIGS} × {N_FINAL_SEEDS} = {N_FINALIST_CONFIGS * N_FINAL_SEEDS} training runs |",
        f"| Selection | Best config by mean val {PRIMARY_METRIC} across seeds |",
        "",
        "### Stage 3 — Test (implementation phase, not HPO)",
        "",
        "- Load best Stage-2 config + best seed checkpoint.",
        "- Evaluate **once** on test split (Phase 10 protocol).",
        "",
        "## Why not Grid or Bayesian?",
        "",
        "- **Grid:** 19,683 combos with 277 validation rows → severe multiple-comparison overfitting.",
        "- **Bayesian:** Surrogate models unstable on small val sets; less reproducible across library versions.",
        "- **Random:** Standard for moderate-dimensional DL HPO (Bergstra & Bengio, 2012); fully logged and replayable.",
        "",
        "## Reproducibility requirements",
        "",
        "```",
        "optimization/trial_manifest.csv   # all 20 Stage-1 configs + val scores",
        "optimization/finalist_configs.yaml",
        "optimization/hpo_log_seed42.json",
        "```",
        "",
    ]
    (OPT_DIR / "optimization_strategy.md").write_text("\n".join(lines))


def write_computational_budget(ranges: pd.DataFrame) -> None:
    train_rows = 1295
    val_rows = 277
    warmup = 7
    train_windows = train_rows - warmup - 1
    lines = [
        "# Computational Budget — Phase 11",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Dataset scale",
        "",
        f"| Split | Rows | Approx. windows (T=7) |",
        f"| --- | --- | --- |",
        f"| Train | {train_rows} | ~{train_windows} |",
        f"| Validation | {val_rows} | ~{val_rows - warmup - 1} |",
        "",
        "## Model scale (9-node PF-STGT)",
        "",
        "| Component | Typical parameter count |",
        "| --- | --- |",
        "| d_model=128, L_s=2, L_t=2, H=4 | ~0.8–1.2 M parameters |",
        "| d_model=192, L_s=3, L_t=3, H=8 | ~2.5–3.5 M parameters (upper bound) |",
        "",
        "Small graph (N=9) keeps attention O(N²) negligible vs temporal O(T²), T=7.",
        "",
        "## Trial budget",
        "",
        "| Stage | Runs | Description |",
        "| --- | --- | --- |",
        f"| Stage 1 HPO | {N_STAGE1_TRIALS} | Random search, seed 42 |",
        f"| Stage 2 confirmation | {N_FINALIST_CONFIGS * N_FINAL_SEEDS} | Top-{N_FINALIST_CONFIGS} configs × {N_FINAL_SEEDS} seeds |",
        "| Stage 3 test | 1 | Final selected config, best seed |",
        f"| **Total training runs** | **{N_STAGE1_TRIALS + N_FINALIST_CONFIGS * N_FINAL_SEEDS + 1}** | Before benchmark comparison |",
        "",
        "## Runtime estimates (single GPU, e.g. Apple M-series / T4)",
        "",
        "| Item | Estimate |",
        "| --- | --- |",
        "| Avg epochs to early stop | 35–60 |",
        "| Time per epoch (B=32, ~1M params) | 15–30 s |",
        "| Time per Stage-1 trial | 10–20 min |",
        f"| **Stage 1 total** | **{N_STAGE1_TRIALS * 12 // 60}–{N_STAGE1_TRIALS * 20 // 60} h** (~4–7 h) |",
        f"| **Stage 2 total** | **{N_FINALIST_CONFIGS * N_FINAL_SEEDS * 12 // 60}–{N_FINALIST_CONFIGS * N_FINAL_SEEDS * 20 // 60} h** (~1–2 h) |",
        "| **HPO subtotal** | **~5–9 GPU-hours** |",
        "",
        "## Resource requirements",
        "",
        "| Resource | Minimum | Recommended |",
        "| --- | --- | --- |",
        "| GPU VRAM | 4 GB | 8 GB |",
        "| System RAM | 8 GB | 16 GB |",
        "| Storage per trial | ~50 MB checkpoint | ~1 GB total HPO artifacts |",
        "| CPU fallback | Supported (3–5× slower) | GPU preferred |",
        "",
        "## Budget guardrails",
        "",
        f"- Hard cap: **{N_STAGE1_TRIALS}** Stage-1 trials (no adaptive expansion).",
        "- Stop trial early if val MAE diverges (>2× train MAE after epoch 10).",
        "- No nested cross-validation (insufficient data; Phase 06 chronological split frozen).",
        "",
    ]
    (OPT_DIR / "computational_budget.md").write_text("\n".join(lines))


def write_model_selection_protocol() -> None:
    lines = [
        "# Model Selection Protocol — Phase 11",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Selection stages",
        "",
        "| Stage | Data used | Decision |",
        "| --- | --- | --- |",
        "| Stage 1 HPO | Val | Rank 20 trials |",
        "| Stage 2 confirmation | Val | Pick 1 config among top-3 |",
        "| Stage 3 test | Test | Report final metrics (no re-selection) |",
        "",
        "## Primary metric (frozen)",
        "",
        f"**{PRIMARY_METRIC}** — macro-averaged MAE over 9 regional demand forecasts on validation split.",
        "",
        "- Unit: MW",
        "- Aligns with Phase 10 leaderboard and Phase 08.5 Task 1 priority.",
        "- Computed on inverse-scaled predictions if training used normalised targets.",
        "",
        "## Secondary metrics",
        "",
        f"| Metric | Role |",
        f"| --- | --- |",
        f"| **{SECONDARY_METRIC}** | Required for PF-STGT multi-task quality (Phase 08.5 Task 2) |",
        "| validation_combined_loss | Diagnostic (λ1·Huber + λ2·MSE) |",
        "| validation_demand_MAPE | Tie-breaker only (scale-sensitive) |",
        "| validation_stress_R2 | Tie-breaker for stress quality |",
        "",
        "## Tie-breaking strategy (frozen order)",
        "",
        "When primary metrics are equal within **0.05 MW** tolerance:",
        "",
        "1. Lower **validation stress MAE** (secondary).",
        "2. Lower **validation combined loss**.",
        "3. **Simpler model:** lower `L_s + L_t`, then lower `d_model`.",
        "4. Higher **validation stress R²**.",
        "5. Default Phase 09 config if still tied.",
        "",
        "## Final config selection (Stage 2)",
        "",
        "```",
        "config* = argmin_{c ∈ top-3} mean_seed∈{42,123,456} val_macro_demand_MAE(c, seed)",
        "seed*   = argmin_seed val_macro_demand_MAE(config*, seed)",
        "```",
        "",
        "## Test-phase rules",
        "",
        "- **No hyperparameter changes** after Stage 2.",
        "- **No test-set peeking** during HPO or confirmation.",
        "- Report test metrics for config* only (+ Phase 09 default as ablation row).",
        "",
        "## Overfitting safeguards",
        "",
        "- Cap trials at 20 (≈1 trial per 14 validation windows — conservative ratio).",
        "- Prefer simpler models on tie-break (Occam's razor for n≈270 val samples).",
        "- Log train vs val MAE gap; flag trials with gap > 30% for manual review.",
        "",
    ]
    (OPT_DIR / "model_selection_protocol.md").write_text("\n".join(lines))


def write_optimization_summary(methods: pd.DataFrame, locked_md5: dict[str, str]) -> None:
    lines = [
        "# Phase 11 — Hyperparameter Optimization Strategy Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Target model: **PF-STGT (B07)**",
        "",
        "## Frozen HPO protocol",
        "",
        "| Component | Decision |",
        "| --- | --- |",
        f"| Search dimensions | 9 (graph ×3, transformer ×3, training ×3) |",
        f"| Optimization method | {OPTIMIZATION_METHOD} |",
        f"| Stage 1 trials | {N_STAGE1_TRIALS} |",
        f"| Finalists | Top {N_FINALIST_CONFIGS} → {N_FINAL_SEEDS} seeds each |",
        f"| Primary metric | {PRIMARY_METRIC} |",
        f"| Secondary metric | {SECONDARY_METRIC} |",
        f"| Est. GPU budget | ~5–9 hours |",
        "",
        "## Deliverables",
        "",
        "### optimization/",
        "- search_space.md",
        "- parameter_ranges.csv",
        "- optimization_strategy.md",
        "- computational_budget.md",
        "- model_selection_protocol.md",
        "",
        "### results/phases/phase_11_hyperparameter_optimization/",
        "- optimization_summary.md",
        "- optimization_decision_report.md",
        "",
        "## Scope compliance",
        "",
        "- HPO strategy design only; **no implementation or training**.",
        "- Locked phase outputs not modified.",
        "",
        "## Locked input integrity",
        "",
    ]
    for path, md5 in locked_md5.items():
        lines.append(f"- `{path}` MD5: `{md5}`")
    lines += [
        "",
        "## Status",
        "",
        "Ready for PF-STGT implementation and HPO execution (next phase).",
        "",
    ]
    (REPORT_DIR / "optimization_summary.md").write_text("\n".join(lines))


def write_decision_report(methods: pd.DataFrame) -> None:
    lines = [
        "# Optimization Decision Report — Phase 11",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Key decisions",
        "",
        "### 1. Random Search over 20 trials",
        "",
        methods[["method", "total_score", "selected", "verdict"]].to_markdown(index=False),
        "",
        "Grid search rejected (19,683 combos). Bayesian rejected (small val set, reproducibility).",
        "",
        "### 2. Realistic ranges for 9-node STGT",
        "",
        "- d_model capped at 192 (not 256/512) given ~1,287 training windows.",
        "- Layers L_s, L_t capped at 3 to limit over-smoothing and overfitting.",
        "- Batch size 16–64 appropriate for ~40–80 steps/epoch.",
        "",
        "### 3. Two-stage selection",
        "",
        "20 exploratory trials → top-3 configs × 3 seeds → single test evaluation.",
        "",
        "### 4. Fixed loss weights",
        "",
        "λ1=1.0, λ2=0.5 not searched (Phase 10 frozen) to reduce validation overfitting.",
        "",
        "### 5. Alignment with Phase 09 defaults",
        "",
        "Phase 09 default (d=128, L_s=2, L_t=2, H=4, lr=5e-4, B=32) included as **trial #0** ",
        "baseline in Stage 1 manifest for direct before/after comparison.",
        "",
    ]
    (REPORT_DIR / "optimization_decision_report.md").write_text("\n".join(lines))


def generate_trial_manifest_template(ranges: pd.DataFrame) -> None:
    """Save a template manifest with trial 0 = Phase 09/10 defaults (not trained here)."""
    baseline = {
        "trial_id": 0,
        "source": "phase09_default_baseline",
        "num_graph_layers": 2,
        "graph_hidden_dim": 128,
        "graph_dropout": 0.1,
        "num_transformer_layers": 2,
        "num_attention_heads": 4,
        "transformer_dropout": 0.1,
        "learning_rate": 5e-4,
        "weight_decay": 1e-4,
        "batch_size": 32,
    }
    pd.DataFrame([baseline]).to_csv(REPORT_DIR / "trial_0_baseline_config.csv", index=False)


def main() -> None:
    OPT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    locked_paths = {
        "data/features/train_features.parquet": FEATURES_PATH,
        "experiments/training_strategy.md": EXP_DIR / "training_strategy.md",
        "architecture/architecture_overview.md": ARCH_DIR / "architecture_overview.md",
    }
    locked_md5 = {k: file_md5(v) for k, v in locked_paths.items()}

    ranges = parameter_ranges_df()
    methods = optimization_method_comparison()

    ranges.to_csv(OPT_DIR / "parameter_ranges.csv", index=False)
    write_search_space(ranges)
    write_optimization_strategy(methods)
    write_computational_budget(ranges)
    write_model_selection_protocol()
    write_optimization_summary(methods, locked_md5)
    write_decision_report(methods)
    generate_trial_manifest_template(ranges)

    print("Phase 11 hyperparameter optimization strategy complete.")
    print(f"Method: {OPTIMIZATION_METHOD} | Trials: {N_STAGE1_TRIALS}")
    print(f"Reports -> {OPT_DIR.relative_to(ROOT)} , {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
