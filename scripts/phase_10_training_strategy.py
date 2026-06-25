"""Phase 10 — Training Strategy & Benchmark Design.

Defines the complete experimental protocol: benchmark models, evaluation metrics,
training strategy, validation procedure, and frozen loss functions.

Does NOT implement models, train models, or generate experimental results.
Does NOT modify locked phase outputs.

Inputs (read-only):
    architecture/
    targets/
    graphs/
    data/features/
    references/gap_analysis/
    configs/preprocessing_config.yaml

Outputs:
    experiments/  (5 deliverables)
    results/phases/phase_10_training_strategy/  (3 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXP_DIR = ROOT / "experiments"
REPORT_DIR = ROOT / "results" / "phases" / "phase_10_training_strategy"
ARCH_DIR = ROOT / "architecture"
TARGETS_DIR = ROOT / "targets"
GRAPHS_DIR = ROOT / "graphs"
FEATURES_DIR = ROOT / "data" / "features"
CONFIG_PATH = ROOT / "configs" / "preprocessing_config.yaml"

REGIONS = [
    "Barishal", "Chattogram", "Cumilla", "Dhaka", "Khulna",
    "Mymensingh", "Rajshahi", "Rangpur", "Sylhet",
]

# ── Frozen protocol constants ──────────────────────────────────────────────
INPUT_WINDOW = 7
FORECAST_HORIZON = 1
N_NODES = 9
WARMUP_SKIP = 7

BENCHMARK_MODELS = [
    {"id": "B01", "name": "Linear Regression", "family": "Classical ML", "graph": False, "tasks": ["demand"]},
    {"id": "B02", "name": "Random Forest", "family": "Classical ML", "graph": False, "tasks": ["demand"]},
    {"id": "B03", "name": "XGBoost", "family": "Classical ML", "graph": False, "tasks": ["demand"]},
    {"id": "B04", "name": "LSTM", "family": "Deep Learning (temporal)", "graph": False, "tasks": ["demand"]},
    {"id": "B05", "name": "GRU", "family": "Deep Learning (temporal)", "graph": False, "tasks": ["demand"]},
    {"id": "B06", "name": "T-GCN", "family": "Spatio-Temporal GNN", "graph": True, "tasks": ["demand"]},
    {"id": "B07", "name": "PF-STGT", "family": "Proposed", "graph": True, "tasks": ["demand", "stress"]},
]

BATCH_SIZE_CANDIDATES = [16, 32, 64]
LEARNING_RATE_CANDIDATES = [1e-4, 5e-4, 1e-3]
OPTIMIZER_CANDIDATES = ["AdamW", "Adam"]
FROZEN_BATCH_SIZE = 32
FROZEN_LR = 5e-4
FROZEN_OPTIMIZER = "AdamW"
EARLY_STOPPING_PATIENCE = 15
MAX_EPOCHS = 200
GRAD_CLIP_NORM = 1.0
WEIGHT_DECAY = 1e-4
RANDOM_SEEDS = [42, 123, 456]

LAMBDA_DEMAND = 1.0
LAMBDA_STRESS = 0.5
LAMBDA_REG = 1e-4
HUBER_DELTA_MW = 1.0


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_split_info() -> dict:
    cfg = yaml.safe_load(CONFIG_PATH.read_text()) if CONFIG_PATH.exists() else {}
    train = pd.read_parquet(FEATURES_DIR / "train_features.parquet")
    val = pd.read_parquet(FEATURES_DIR / "validation_features.parquet")
    test = pd.read_parquet(FEATURES_DIR / "test_features.parquet")
    return {
        "train_rows": len(train),
        "val_rows": len(val),
        "test_rows": len(test),
        "train_dates": f"{train['Date'].min().date()} → {train['Date'].max().date()}",
        "val_dates": f"{val['Date'].min().date()} → {val['Date'].max().date()}",
        "test_dates": f"{test['Date'].min().date()} → {test['Date'].max().date()}",
        "split_ratio": cfg.get("split", {}).get("ratios", "70/15/15"),
    }


def benchmark_table() -> pd.DataFrame:
    rows = []
    for m in BENCHMARK_MODELS:
        rows.append({
            "benchmark_id": m["id"],
            "model_name": m["name"],
            "family": m["family"],
            "uses_graph": m["graph"],
            "tasks_supported": ";".join(m["tasks"]),
            "input_window_T": INPUT_WINDOW,
            "horizon_h": FORECAST_HORIZON,
            "adjacency": "graphs/adjacency_matrix.csv" if m["graph"] else "N/A",
            "multi_task": "demand" in m["tasks"] and "stress" in m["tasks"],
        })
    return pd.DataFrame(rows)


def write_benchmark_design(split: dict) -> None:
    bench = benchmark_table()
    lines = [
        "# Benchmark Design — Phase 10",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Purpose",
        "",
        "Define a fair, literature-aligned benchmark suite for evaluating PF-STGT against "
        "classical, temporal, and spatio-temporal baselines on the Bangladesh smart-grid dataset.",
        "",
        "## Frozen benchmark models (7)",
        "",
        bench.to_markdown(index=False),
        "",
        "## Fair comparison protocol",
        "",
        "| Constraint | Specification |",
        "| --- | --- |",
        f"| Input window | T={INPUT_WINDOW} observed days (Phase 09) |",
        f"| Forecast horizon | h={FORECAST_HORIZON} day (Phase 08.5) |",
        f"| Warm-up exclusion | Skip first {WARMUP_SKIP} timesteps per split (Phase 06) |",
        f"| Graph adjacency | Phase 08 hybrid matrix (B06, B07 only) |",
        f"| Feature source | `data/features/*_features.parquet` (Phase 05B/06) |",
        f"| Leakage policy | No same-day OSI as input for stress target (Phase 08.5) |",
        "",
        "## Model-specific design notes",
        "",
        "### B01–B03 Classical ML (demand-only)",
        "- **Input:** Flatten `(T, F_node)` per region → 9 independent regressors OR multi-output linear.",
        "- **Target:** \\(D_r(t+1)\\) per region.",
        "- **Rationale:** Phase 07B hybrid/ensemble papers; low-complexity lower bound (GAP-08 reproducibility).",
        "",
        "### B04 LSTM / B05 GRU (demand-only)",
        "- **Input:** `(T, F_node)` sequence per node; shared weights across nodes.",
        "- **Output:** 9 demand values at t+1.",
        "- **Rationale:** 7/55 transformer/temporal papers; standard DL baseline without graph (GAP-04 contrast).",
        "",
        "### B06 T-GCN (demand-only, graph baseline)",
        "- **Input:** `(T, N, F_node)` + hybrid adjacency A.",
        "- **Architecture:** 2-layer temporal graph convolution (ST-first: GCN → GRU), aligned with ST-GCN literature.",
        "- **Rationale:** Phase 07B GNN cluster (5/55 graph papers); isolates graph value vs PF-STGT transformer fusion.",
        "",
        "### B07 PF-STGT (proposed, multi-task)",
        "- **Architecture:** Phase 09 PF-STGT design (Graph Transformer ∥ Transformer Encoder → dual heads).",
        "- **Tasks:** Demand (9 nodes) + OSI (graph-level).",
        "- **Rationale:** Full proposed framework; only benchmark with Task 2 stress output.",
        "",
        "## Task coverage matrix",
        "",
        "| Model | Demand forecast | Stress forecast |",
        "| --- | --- | --- |",
        "| B01–B06 | Yes | No (demand-only baselines) |",
        "| B07 PF-STGT | Yes | Yes |",
        "",
        "Stress metrics (Phase 10) are primary for PF-STGT; non-learned persistence/median OSI "
        "baselines reported in `evaluation_protocol.md` for context only (not benchmark models).",
        "",
        "## Data splits (Phase 04 — frozen)",
        "",
        f"| Split | Rows | Date range |",
        f"| --- | --- | --- |",
        f"| Train | {split['train_rows']} | {split['train_dates']} |",
        f"| Validation | {split['val_rows']} | {split['val_dates']} |",
        f"| Test | {split['test_rows']} | {split['test_dates']} |",
        "",
        f"Approximate train windows after warm-up: ~{split['train_rows'] - WARMUP_SKIP - FORECAST_HORIZON}.",
        "",
    ]
    (EXP_DIR / "benchmark_design.md").write_text("\n".join(lines))


def write_evaluation_protocol() -> None:
    lines = [
        "# Evaluation Protocol — Phase 10",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Evaluation scope",
        "",
        "- **Primary comparison:** Task 1 regional demand forecasting (all 7 benchmarks).",
        "- **Secondary evaluation:** Task 2 OSI forecasting (PF-STGT only + non-model baselines).",
        "- **Final reporting:** Test split only, once after model selection on validation.",
        "",
        "## Task 1 — Demand forecasting metrics (frozen)",
        "",
        "| Metric | Formula | Aggregation |",
        "| --- | --- | --- |",
        "| **MAE** | mean(\\|y − ŷ\\|) MW | Macro-mean over 9 regions + national weighted |",
        "| **RMSE** | sqrt(mean((y − ŷ)²)) MW | Macro-mean over 9 regions |",
        "| **MAPE** | mean(\\|y − ŷ\\| / \\|y\\|) × 100% | Macro-mean; exclude y=0 rows |",
        "| **R²** | 1 − SS_res/SS_tot | Macro-mean over 9 regions |",
        "",
        "### Aggregation rules",
        "",
        "1. Compute each metric **per region** on test split.",
        "2. Report **macro-average** (unweighted mean over 9 regions) as primary leaderboard score.",
        "3. Report **Dhaka** separately (Phase 02: ~35.7% national share).",
        "4. Optional: national eve-peak demand derived from Σ regional predictions for appendix.",
        "",
        "## Task 2 — Operational stress metrics (frozen)",
        "",
        "| Metric | Formula | Notes |",
        "| --- | --- | --- |",
        "| **MAE** | mean(\\|OSI − OSI_hat\\|) | Primary |",
        "| **RMSE** | sqrt(mean((OSI − OSI_hat)²)) | Primary |",
        "| **R²** | 1 − SS_res/SS_tot | Primary |",
        "| Pearson r | corr(OSI, OSI_hat) | Supplementary (Phase 09) |",
        "",
        "### Non-model OSI baselines (context only, not benchmark models)",
        "",
        "| Baseline | Definition |",
        "| --- | --- |",
        "| Persistence | OSI_hat(t+1) = OSI(t) |",
        "| Train median | OSI_hat = median(OSI_train) |",
        "",
        "## Statistical reporting",
        "",
        f"- Deep models (B04–B07): **3 seeds** {RANDOM_SEEDS} → report mean ± std on test.",
        "- Classical ML (B01–B03): single deterministic fit (seed=42 where applicable).",
        "- No test-set hyperparameter tuning.",
        "",
        "## Leaderboard format (implementation phase)",
        "",
        "```",
        "results/experiments/leaderboard_demand_test.csv",
        "results/experiments/leaderboard_stress_test.csv",
        "results/experiments/per_region_metrics_test.csv",
        "```",
        "",
        "## Comparison to literature (Phase 07B/07C)",
        "",
        "- Report MAPE alongside MAE for cross-paper comparability (20/55 load forecasting papers).",
        "- Document chronological split explicitly (GAP-08 vs metadata-sparse conference baselines).",
        "- PF-STGT must beat T-GCN on macro MAE **and** report stress R² to support GAP-02/GAP-06 claims.",
        "",
    ]
    (EXP_DIR / "evaluation_protocol.md").write_text("\n".join(lines))


def write_training_strategy(split: dict) -> None:
    lines = [
        "# Training Strategy — Phase 10",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Applicable models",
        "",
        "Deep learning training protocol applies to **B04 LSTM, B05 GRU, B06 T-GCN, B07 PF-STGT**.",
        "Classical ML (B01–B03) uses library defaults with hyperparameter grid below.",
        "",
        "## Hyperparameter search (validation split only)",
        "",
        "### Deep learning grid",
        "",
        "| Hyperparameter | Candidates | **Selected default** |",
        "| --- | --- | --- |",
        f"| Batch size | {BATCH_SIZE_CANDIDATES} | **{FROZEN_BATCH_SIZE}** |",
        f"| Learning rate | {LEARNING_RATE_CANDIDATES} | **{FROZEN_LR}** |",
        f"| Optimizer | {OPTIMIZER_CANDIDATES} | **{FROZEN_OPTIMIZER}** |",
        f"| Weight decay | — | **{WEIGHT_DECAY}** |",
        f"| Max epochs | — | **{MAX_EPOCHS}** |",
        f"| Grad clip norm | — | **{GRAD_CLIP_NORM}** |",
        "",
        "Selection criterion on validation: **lowest macro demand MAE** (primary); tie-break on val stress MAE for PF-STGT.",
        "",
        "### Classical ML grid",
        "",
        "| Model | Search space | Selection metric |",
        "| --- | --- | --- |",
        "| Linear Regression | default (OLS / Ridge α∈{0.1,1,10}) | val macro MAE |",
        "| Random Forest | n_estimators∈{100,300}, max_depth∈{None,10,20} | val macro MAE |",
        "| XGBoost | max_depth∈{4,6,8}, lr∈{0.05,0.1}, n_estimators∈{200,500} | val macro MAE |",
        "",
        "## Optimizer configuration (frozen default)",
        "",
        "```python",
        "optimizer = AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)",
        "scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)",
        "```",
        "",
        "## Early stopping (frozen)",
        "",
        f"| Parameter | Value |",
        f"| --- | --- |",
        f"| Monitor | Validation macro demand MAE |",
        f"| Patience | {EARLY_STOPPING_PATIENCE} epochs |",
        f"| Min delta | 0.01 MW |",
        f"| Restore best weights | Yes |",
        "",
        "PF-STGT: monitor combined validation loss if demand MAE plateaus but stress improves — log both.",
        "",
        "## Checkpoint strategy (frozen)",
        "",
        "Save on validation improvement:",
        "",
        "```",
        "checkpoints/{benchmark_id}/seed_{seed}/best.pt",
        "checkpoints/{benchmark_id}/seed_{seed}/config.yaml",
        "checkpoints/{benchmark_id}/seed_{seed}/metrics_val.json",
        "```",
        "",
        "- Retain **best validation** checkpoint only (not last epoch).",
        "- Final test evaluation loads best val checkpoint.",
        "- Store git commit hash, seed, and data MD5 in checkpoint metadata.",
        "",
        "## Training data usage",
        "",
        f"- **Train:** fit model on train windows only (~{split['train_rows'] - WARMUP_SKIP - FORECAST_HORIZON} samples).",
        "- **Validation:** early stopping + hyperparameter selection.",
        "- **Test:** held out until final single evaluation.",
        "",
        "## Multi-seed protocol",
        "",
        f"- Seeds: `{RANDOM_SEEDS}` for B04–B07.",
        "- Report test metrics as mean ± std across seeds.",
        "- Primary claim uses best-seed or mean — document choice in results phase.",
        "",
    ]
    (EXP_DIR / "training_strategy.md").write_text("\n".join(lines))


def write_loss_function_design() -> None:
    lines = [
        "# Loss Function Design — Phase 10 (Frozen)",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN** (extends Phase 09 design with benchmark-specific rules)",
        "",
        "## PF-STGT multi-task loss (B07)",
        "",
        "```",
        f"L_total = λ1 · L_demand + λ2 · L_stress + λ_reg · L_reg",
        f"λ1 = {LAMBDA_DEMAND}   (frozen)",
        f"λ2 = {LAMBDA_STRESS}    (frozen)",
        f"λ_reg = {LAMBDA_REG} (frozen)",
        "```",
        "",
        "### Task 1 — Demand (Huber)",
        "",
        "```",
        f"L_demand = (1/N) Σ_r Huber_δ(D_hat_r, D_r; δ={HUBER_DELTA_MW} MW)",
        "```",
        "",
        "- Robust to Phase 02 upper-tail demand outliers.",
        "- Macro-averaged over N=9 regions.",
        "",
        "### Task 2 — Stress (MSE)",
        "",
        "```",
        "L_stress = MSE(OSI_hat, OSI)     where OSI_hat = sigmoid(head_output)",
        "```",
        "",
        "- Target: OSI(t+1) ∈ [0,1] per Phase 08.5 SF-04.",
        "",
        "### Regularisation",
        "",
        "```",
        "L_reg = weight_decay · ||θ_heads||_2   (via AdamW decoupled weight decay)",
        "```",
        "",
        "## Single-task deep baselines (B04–B06)",
        "",
        "```",
        f"L = (1/N) Σ_r Huber_δ(D_hat_r, D_r; δ={HUBER_DELTA_MW})",
        "```",
        "",
        "Same Huber formulation as PF-STGT Task 1 for fair loss comparison.",
        "",
        "## Classical ML baselines (B01–B03)",
        "",
        "| Model | Training objective | Notes |",
        "| --- | --- | --- |",
        "| Linear Regression | Squared error (OLS) or Ridge penalty | Matches Huber at δ→∞ for Gaussian errors |",
        "| Random Forest | MSE impurity | Non-differentiable ensemble |",
        "| XGBoost | Squared error (reg:squarederror) | eval_metric=rmse on validation |",
        "",
        "## Combined loss strategy (PF-STGT only)",
        "",
        "1. **Fixed weights** λ1=1.0, λ2=0.5 for primary experiments (frozen).",
        "2. **Ablation (future):** λ2 ∈ {0.25, 0.5, 1.0} on validation only.",
        "3. **Optional extension:** Kendall uncertainty weighting — not primary protocol.",
        "",
        "## Loss-to-metric alignment",
        "",
        "| Task | Training loss | Primary eval metric |",
        "| --- | --- | --- |",
        "| Demand | Huber | MAE (test) |",
        "| Stress | MSE | RMSE, R² (test) |",
        "",
        "MAPE reported at evaluation only (not optimised — Phase 02 MAPE sensitivity to scale).",
        "",
    ]
    (EXP_DIR / "loss_function_design.md").write_text("\n".join(lines))


def write_reproducibility_protocol(split: dict) -> None:
    lines = [
        "# Reproducibility Protocol — Phase 10",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Data versioning",
        "",
        "| Artifact | Path | Verification |",
        "| --- | --- | --- |",
        "| Raw dataset | `data/raw/bangladesh_smartgrid_raw.csv` | MD5 in Phase 01 |",
        "| Feature splits | `data/features/*_features.parquet` | MD5 before/after training |",
        "| Adjacency | `graphs/adjacency_matrix.csv` | MD5 in Phase 08 |",
        "| Preprocessing | `models/preprocessing_pipeline.pkl` | Phase 04 frozen |",
        "",
        "## Chronological split (Phase 04 — immutable)",
        "",
        f"| Split | Rows | Dates |",
        f"| --- | --- | --- |",
        f"| Train | {split['train_rows']} | {split['train_dates']} |",
        f"| Validation | {split['val_rows']} | {split['val_dates']} |",
        f"| Test | {split['test_rows']} | {split['test_dates']} |",
        "",
        "- No shuffling across time.",
        "- No refitting scalers/encoders on val/test.",
        "- Window builder uses only past observations within split (+ train history for val/test lag features per Phase 06).",
        "",
        "## Random seed control",
        "",
        f"| Component | Seed |",
        f"| --- | --- |",
        f"| Deep learning runs | {RANDOM_SEEDS} |",
        f"| NumPy / Python / PyTorch | Set per run; document in config |",
        f"| Classical ML | 42 |",
        "",
        "## Experiment configuration files (implementation phase)",
        "",
        "```",
        "configs/experiments/{benchmark_id}.yaml",
        "configs/experiments/pf_stgt.yaml",
        "configs/experiments/protocol_phase10.yaml   # frozen constants from this phase",
        "```",
        "",
        "Each config must record: benchmark_id, seed, split paths, T, h, λ1, λ2, batch_size, lr.",
        "",
        "## Logging requirements",
        "",
        "- Per-epoch: train/val loss components, macro demand MAE, stress MAE (PF-STGT).",
        "- Final: test metrics JSON + CSV per region.",
        "- Hardware: CPU/GPU model, PyTorch version, wall-clock time.",
        "",
        "## Test protocol (single pass)",
        "",
        "1. Select hyperparameters on **validation** only.",
        "2. Retrain on train+val OR load best-val checkpoint from train-only (document choice).",
        "   - **Frozen choice:** train-only with best-val checkpoint (no val data in final fit).",
        "3. Evaluate once on **test**; no test feedback loop.",
        "",
        "## GAP-08 alignment",
        "",
        "Explicit split documentation, fixed seeds, and published leaderboard CSVs address ",
        "reproducibility gap identified in 52/55 metadata-sparse literature papers (Phase 07C).",
        "",
    ]
    (EXP_DIR / "reproducibility_protocol.md").write_text("\n".join(lines))


def write_benchmark_rationale() -> None:
    lines = [
        "# Benchmark Rationale — Phase 10",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Literature and gap evidence",
        "",
        "| Benchmark | Evidence |",
        "| --- | --- |",
        "| Linear Regression | Lower bound; Phase 07B hybrid papers use statistical baselines |",
        "| Random Forest / XGBoost | Phase 07B ensemble/hybrid cluster; strong tabular baselines on engineered features (GAP-07) |",
        "| LSTM / GRU | 7/55 temporal DL papers; isolates recurrence without graph (GAP-04 ablation) |",
        "| T-GCN | 5/55 graph papers; standard ST-GNN baseline with Phase 08 adjacency |",
        "| PF-STGT | Proposed; addresses GAP-04/05/06 multi-task graph-transformer gap |",
        "",
        "## Progressive complexity ladder",
        "",
        "```",
        "Linear → RF/XGB → LSTM/GRU → T-GCN → PF-STGT",
        "  (none)   (none)    (temporal)  (+graph)  (+transformer+multi-task+XAI)",
        "```",
        "",
        "Each step adds capacity justified by Phase 07C gaps; PF-STGT must demonstrate ",
        "incremental value over T-GCN on demand **and** provide stress predictions T-GCN cannot.",
        "",
        "## Why demand-only baselines for B01–B06",
        "",
        "- Phase 08.5 defines dual-task formulation for PF-STGT only.",
        "- Literature baselines (Phase 07B) rarely report joint stress forecasting.",
        "- Fair comparison: same input features and horizon for Task 1 across all models.",
        "",
    ]
    (REPORT_DIR / "benchmark_rationale.md").write_text("\n".join(lines))


def write_training_decision_report(split: dict) -> None:
    lines = [
        "# Training Decision Report — Phase 10",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Frozen decisions summary",
        "",
        "### Benchmark models (7)",
        "",
        ", ".join(m["name"] for m in BENCHMARK_MODELS),
        "",
        "### Evaluation metrics",
        "",
        "- **Demand:** MAE, RMSE, MAPE, R² (macro + Dhaka)",
        "- **Stress:** MAE, RMSE, R² (+ Pearson r supplementary)",
        "",
        "### Training defaults (deep models)",
        "",
        f"| Parameter | Frozen value |",
        f"| --- | --- |",
        f"| Batch size | {FROZEN_BATCH_SIZE} |",
        f"| Learning rate | {FROZEN_LR} |",
        f"| Optimizer | {FROZEN_OPTIMIZER} |",
        f"| Weight decay | {WEIGHT_DECAY} |",
        f"| Early stopping patience | {EARLY_STOPPING_PATIENCE} |",
        f"| Max epochs | {MAX_EPOCHS} |",
        f"| Seeds | {RANDOM_SEEDS} |",
        "",
        "### Loss functions",
        "",
        f"- PF-STGT: λ1={LAMBDA_DEMAND} Huber + λ2={LAMBDA_STRESS} MSE",
        f"- Deep baselines: Huber δ={HUBER_DELTA_MW} MW",
        "- Classical: library default squared error",
        "",
        "### Validation protocol",
        "",
        "- Chronological 70/15/15 split (Phase 04)",
        "- Model selection on validation macro demand MAE",
        "- Single final test evaluation",
        "- Train-only fit; no test leakage (Phase 06)",
        "",
        "## Window and sample counts",
        "",
        f"| Split | Raw rows | Approx. windows (T={INPUT_WINDOW}) |",
        f"| --- | --- | --- |",
        f"| Train | {split['train_rows']} | ~{max(0, split['train_rows'] - WARMUP_SKIP - FORECAST_HORIZON)} |",
        f"| Validation | {split['val_rows']} | ~{max(0, split['val_rows'] - WARMUP_SKIP - FORECAST_HORIZON)} |",
        f"| Test | {split['test_rows']} | ~{max(0, split['test_rows'] - WARMUP_SKIP - FORECAST_HORIZON)} |",
        "",
        "## Next phase",
        "",
        "Implement benchmark trainers per `experiments/` protocol; no results generated in Phase 10.",
        "",
    ]
    (REPORT_DIR / "training_decision_report.md").write_text("\n".join(lines))


def write_experiment_summary(locked_md5: dict[str, str]) -> None:
    lines = [
        "# Phase 10 — Training Strategy & Benchmark Design Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Frozen protocol",
        "",
        "| Component | Status |",
        "| --- | --- |",
        "| 7 benchmark models | FROZEN |",
        "| Demand metrics (MAE, RMSE, MAPE, R²) | FROZEN |",
        "| Stress metrics (MAE, RMSE, R²) | FROZEN |",
        "| Training strategy | FROZEN |",
        "| Validation / test protocol | FROZEN |",
        "| Multi-task loss (λ1=1.0, λ2=0.5) | FROZEN |",
        "",
        "## Deliverables",
        "",
        "### experiments/",
        "- benchmark_design.md",
        "- evaluation_protocol.md",
        "- training_strategy.md",
        "- loss_function_design.md",
        "- reproducibility_protocol.md",
        "",
        "### results/phases/phase_10_training_strategy/",
        "- experiment_summary.md",
        "- benchmark_rationale.md",
        "- training_decision_report.md",
        "",
        "## Scope compliance",
        "",
        "- Experimental protocol definition only.",
        "- **No model implementation.**",
        "- **No training or results generated.**",
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
        "Ready for implementation and training (next phase).",
        "",
    ]
    (REPORT_DIR / "experiment_summary.md").write_text("\n".join(lines))


def main() -> None:
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    locked_paths = {
        "data/features/train_features.parquet": FEATURES_DIR / "train_features.parquet",
        "graphs/adjacency_matrix.csv": GRAPHS_DIR / "adjacency_matrix.csv",
        "targets/multitask_formulation.md": TARGETS_DIR / "multitask_formulation.md",
        "architecture/architecture_overview.md": ARCH_DIR / "architecture_overview.md",
    }
    locked_md5 = {k: file_md5(v) for k, v in locked_paths.items()}

    split = load_split_info()
    bench = benchmark_table()
    bench.to_csv(REPORT_DIR / "benchmark_registry.csv", index=False)

    write_benchmark_design(split)
    write_evaluation_protocol()
    write_training_strategy(split)
    write_loss_function_design()
    write_reproducibility_protocol(split)
    write_benchmark_rationale()
    write_training_decision_report(split)
    write_experiment_summary(locked_md5)

    print("Phase 10 training strategy & benchmark design complete.")
    print(f"Benchmark models frozen: {len(BENCHMARK_MODELS)}")
    print(f"Reports -> {EXP_DIR.relative_to(ROOT)} , {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
