# Module Specification — Phase 16A

Generated: 2026-06-24
Status: **FROZEN BLUEPRINT**

## Overview

**45 modules** across 8 pipelines. Each row specifies file path,
responsibility, and I/O contract for implementation.

## Full module registry

| file_path                              | pipeline   | class_or_fn           | responsibility                           | inputs            | outputs              |
|:---------------------------------------|:-----------|:----------------------|:-----------------------------------------|:------------------|:---------------------|
| src/data/loader.py                     | P1         | DataLoader            | Load clean parquet + feature parquet     | DataFrame         | Validated DataFrame  |
| src/data/splits.py                     | P1         | SplitManager          | Chronological split indices + MD5 verify | DataFrame         | train/val/test masks |
| src/data/validators.py                 | P1         | DataValidator         | Schema, row count, date continuity       | DataFrame         | ValidationReport     |
| src/datasets/smartgrid_dataset.py      | P1,P2,P4   | SmartGridDataset      | PyTorch Dataset: windowed samples        | index             | batch dict           |
| src/datasets/collate.py                | P1         | collate_fn            | Batch stacking + padding                 | list[dict]        | batched tensors      |
| src/features/node_features.py          | P2         | NodeFeatureBuilder    | Extract F_n=9 per region                 | DataFrame, t      | (N,F_n)              |
| src/features/global_features.py        | P2         | GlobalFeatureBuilder  | Extract F_g=17 (no OSI input)            | DataFrame, t      | (F_g,)               |
| src/features/window_builder.py         | P2         | WindowBuilder         | T=7 gap-aware windows                    | DataFrame         | (T,N,F_n),(T,F_g)    |
| src/features/scaler.py                 | P2         | FeatureScaler         | Load train-fitted StandardScaler         | raw features      | scaled features      |
| src/preprocessing/leakage_guard.py     | P2         | LeakageGuard          | Strip OSI from inputs at h=1             | feature list      | safe feature list    |
| src/graph/adjacency.py                 | P3         | AdjacencyLoader       | Load hybrid CSV, row-normalise           | path              | (N,N) tensor         |
| src/graph/bias.py                      | P3         | AdjacencyBias         | log(A+ε) bias matrix for attention       | (N,N)             | bias (N,N)           |
| src/graph/registry.py                  | P3         | GraphRegistry         | Hybrid/geo/corr variants (ablation)      | variant_id        | (N,N)                |
| src/datasets/targets.py                | P4         | TargetBuilder         | demand_target at t+1                     | DataFrame, t      | (N,) MW              |
| src/datasets/osi_target.py             | P4         | OSITargetBuilder      | OSI at t+1 from frozen formula           | DataFrame, t+1    | scalar [0,1]         |
| src/datasets/multitask_batch.py        | P4         | MultiTaskBatch        | Assemble demand + osi targets            | batch             | target dict          |
| src/models/embeddings.py               | P5         | InputEmbedding        | Node + global + positional enc           | tensors           | H0 (B,T,N,d)         |
| src/models/spatial_encoder.py          | P5         | GraphTransformer      | L_s=2 spatial layers + attn export       | H0, bias          | H_spatial, attn_s    |
| src/models/temporal_encoder.py         | P5         | TemporalTransformer   | L_t=2 encoder + attn export              | H0                | H_temporal, attn_t   |
| src/models/fusion.py                   | P5         | ParallelFusion        | Gated concat → H_shared                  | H_s, H_t          | H_shared (B,N,d)     |
| src/models/heads.py                    | P5         | MultiTaskHeads        | DemandHead (9) + StressHead (1)          | H_shared, h_graph | preds                |
| src/models/pf_stgt.py                  | P5         | PFSTGT                | Full forward + ablation switches         | batch             | ModelOutput          |
| src/models/baselines/                  | P5         | BaselineModels        | B01–B06 implementations                  | batch             | preds                |
| src/models/ablations/                  | P5         | AblationVariants      | A2–A6 structural switches                | batch             | preds                |
| src/losses/multitask.py                | P5         | MultiTaskLoss         | λ1·Huber + λ2·MSE                        | preds, targets    | scalar loss          |
| src/training/trainer.py                | P6         | Trainer               | Train/val loop orchestration             | model, loaders    | history              |
| src/training/callbacks.py              | P6         | EarlyStopping         | Patience 15, val macro MAE               | metrics           | stop signal          |
| src/training/checkpoint.py             | P6         | CheckpointManager     | best.pt + metadata MD5                   | state             | path                 |
| src/training/optimizer.py              | P6         | build_optimizer       | AdamW + ReduceLROnPlateau                | model, config     | optim, sched         |
| src/training/seed.py                   | P6         | set_seed              | Reproducibility 42/123/456               | seed              | —                    |
| src/metrics/demand.py                  | P7         | DemandMetrics         | MAE, RMSE, MAPE, R² macro                | y, y_hat          | metric dict          |
| src/metrics/stress.py                  | P7         | StressMetrics         | OSI MAE, RMSE, R², r                     | osi, osi_hat      | metric dict          |
| src/evaluation/benchmark_runner.py     | P7         | BenchmarkRunner       | B01–B07 test eval                        | checkpoint        | Table 1 rows         |
| src/evaluation/ablation_runner.py      | P7         | AblationRunner        | A1–A6 vs reference                       | checkpoints       | Table 2 rows         |
| src/evaluation/statistics.py           | P7         | StatisticalTests      | Wilcoxon + Bonferroni + bootstrap        | daily errors      | Table 4 rows         |
| src/evaluation/robustness.py           | P7         | RobustnessEvaluator   | Phase 14 segments                        | residuals         | Table S3             |
| src/evaluation/error_analysis.py       | P7         | ErrorAnalysisRunner   | E1–E6 taxonomy                           | predictions       | segment CSVs         |
| src/explainability/shap_runner.py      | P8         | SHAPRunner            | GradientSHAP grouped                     | model, batch      | φ values             |
| src/explainability/attention_export.py | P8         | AttentionExporter     | Spatial + temporal maps                  | model forward     | attn tensors         |
| src/explainability/permutation.py      | P8         | PermutationImportance | Validation global ranks                  | model, val        | importance CSV       |
| src/explainability/stress_decompose.py | P8         | StressDecomposer      | c1/c2/c3 ground truth                    | DataFrame         | driver labels        |
| src/visualization/manuscript.py        | P8         | ManuscriptFigures     | Fig 1–5 renderers                        | artefacts         | PNG/PDF              |
| src/utils/config.py                    | ALL        | Config                | YAML config loader                       | path              | Config dataclass     |
| src/utils/logging.py                   | ALL        | Logger                | Structured experiment logs               | —                 | log files            |
| src/utils/md5.py                       | ALL        | MD5Guard              | Verify locked artefact hashes            | paths             | pass/fail            |

---

## P1 — Data Pipeline

### Responsibilities

| Function | Owner |
| --- | --- |
| Load datasets | `src/data/loader.py` |
| Split management | `src/data/splits.py` |
| Data validation | `src/data/validators.py` |
| PyTorch dataset | `src/datasets/smartgrid_dataset.py` |

### Split specification (frozen)

| Split | Date range | Rows | Warm-up skip |
| --- | --- | --- | --- |
| train | 2019-11-21 → 2023-06-15 | 1295 | 7 |
| validation | 2023-06-16 → 2024-03-19 | 277 | 7 |
| test | 2024-03-20 → 2024-12-30 | 278 | 7 |

### Validation checks

- MD5 match against locked hashes before training.
- Row counts match Phase 04.
- `Date` monotonic within split; no overlap across splits.
- 17 calendar gaps documented (Phase 05B gap-aware lags).

---

## P2 — Feature Pipeline

### Tensor contracts (Phase 09)

| Tensor | Shape | F count | Notes |
| --- | --- | --- | --- |
| `node_features` | (B, T, N, F_n) | F_n=9 | Per-region columns |
| `global_features` | (B, T, F_g) | F_g=17 | No OSI at input |

### Node features (F_n=9 per region)

1. `{r}_demand`, 2. `{r}_supply`, 3. `{r}_load`
4. `demand_lag_1_{r}`, 5. `demand_lag_7_{r}`, 6. `load_lag_1_{r}`
7. `demand_rolling_mean_7_{r}`, 8. `regional_demand_share_{r}`
9. `regional_load_intensity_{r}`

### Global features (F_g=17)

Calendar (Year, Month, DOW, holiday flags), national generation aggregates,
limitations (gas, coal, water, maintenance), temperature anomaly.
**Excluded:** `operational_stress_index`.

### Feature validation

- Reuse Phase 06 screening rules; fail on NaN outside warm-up.
- StandardScaler: load train-fitted params only (no refit on val/test).

---

## P3 — Graph Pipeline

### Responsibilities

| Function | Module |
| --- | --- |
| Hybrid graph loading | `adjacency.py` |
| Adjacency matrix management | `registry.py` (hybrid/geo/corr) |
| Graph tensor construction | `bias.py` → log(A+ε) attention bias |

### Graph variants (ablation)

| Variant | Source | Edges |
| --- | --- | --- |
| hybrid (default) | `graphs/adjacency_matrix.csv` | 24 |
| geo (A5-GEO) | Phase 08 geographic only | 21 |
| corr (A5-CORR) | Phase 08 τ=0.65 | 33 |

### Node order (must match adjacency rows/cols)

```
Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet
```

---

## P4 — Target Pipeline

### Demand targets

- Column: `{Region}_demand` for each of 9 regions.
- Horizon: h=1 → target at index t+1 relative to window end t.
- Shape: `(B, N)` float32 MW.

### OSI targets

```
c1 = L_total / D_total
c2 = 1 - GR / Highest_Gen
c3 = TOL / Highest_Gen
OSI = mean(minmax_train(c1), minmax_train(c2), minmax_train(c3))
```

- Shape: `(B, 1)` float32 ∈ [0, 1].
- A4 ablation: omit `osi_target` and stress head.

### Multi-task batch dict

```python
batch = {
    "node_features": Tensor,
    "global_features": Tensor,
    "adjacency": Tensor,
    "demand_target": Tensor,      # always
    "osi_target": Tensor | None,  # None for B01–B06, A4
    "meta": {"date": ..., "split": ...},
}
```

---

## P5 — PF-STGT Module Structure

### Class hierarchy

```
PFSTGT(nn.Module)
├── InputEmbedding
├── SpatialEncoder (GraphTransformer × L_s=2)
│   └── exports attn_spatial (B, heads, N, N)
├── TemporalEncoder (TransformerEncoder × L_t=2)
│   └── exports attn_temporal (B, heads, T, T)
├── ParallelFusion (gated)
├── DemandHead → (B, N)
└── StressHead → (B, 1)  [optional: A4 off]
```

### ModelOutput dataclass

```python
@dataclass
class ModelOutput:
    demand_pred: Tensor      # (B, N)
    osi_pred: Tensor | None  # (B, 1)
    attn_spatial: Tensor | None
    attn_temporal: Tensor | None
    h_shared: Tensor | None  # for XAI
```

### Ablation switches (config-driven)

| Switch | Effect | Variant |
| --- | --- | --- |
| `use_spatial=False` | Skip GraphTransformer | A2 |
| `use_temporal=False` | Skip TemporalEncoder | A3 |
| `multi_task=False` | No StressHead | A4 |
| `adjacency_variant=geo` | Swap graph | A5-GEO |
| `trunk=bilstm` | Replace encoders | A6 |

### Baseline models (same batch interface)

B01–B06 in `src/models/baselines/` sharing `forward(batch) -> demand_pred`.

---

## P6 — Training Pipeline

### Loop structure

```
for epoch in range(max_epochs):
    train_epoch()   → L_total backward, grad clip 1.0
    val_epoch()     → macro MAE, stress MAE
    scheduler.step(val_mae)
    early_stop.check(val_mae)
    checkpoint.save_if_best()
```

### Frozen hyperparameters (Phase 10/11)

| Param | Value |
| --- | --- |
| Optimizer | AdamW, lr=5e-4, wd=1e-4 |
| Scheduler | ReduceLROnPlateau, factor=0.5, patience=5 |
| Batch size | 32 (HPO search in Phase 11) |
| Max epochs | 200 |
| Early stop patience | 15 |
| λ1, λ2 | 1.0, 0.5 |

### Checkpoint metadata

Store: seed, git hash, locked MD5s, model_id, val metrics, config YAML.

---

## P7 — Evaluation Pipeline

### Sub-modules

| Component | Output | Phase ref |
| --- | --- | --- |
| `DemandMetrics` | MAE, RMSE, MAPE, R² | 10, 15 Table 1 |
| `StressMetrics` | OSI metrics | 15 Table 3 |
| `BenchmarkRunner` | B01–B07 leaderboard | 10 |
| `AblationRunner` | ΔMAE vs A1 | 13 Table 2 |
| `StatisticalTests` | Wilcoxon, bootstrap | 13, 15 Table 4 |
| `RobustnessEvaluator` | Segment metrics | 14, 15 Table S3 |
| `ErrorAnalysisRunner` | E1–E6 residuals | 14 |

### Evaluation order

1. Load best checkpoint (val-selected).
2. Run inference on test loader only.
3. Compute metrics → CSV tables.
4. Run statistics → Table 4.
5. Run error taxonomy → robustness segments.
6. Render figures (delegate to P8 for XAI figures).

---

## P8 — Explainability Pipeline

### Methods (Phase 12 — frozen)

| Method | Module | Output |
| --- | --- | --- |
| SHAP | `shap_runner.py` | grouped φ CSV |
| Attention | `attention_export.py` | spatial/temporal tensors |
| Permutation | `permutation.py` | global importance rank |
| Stress decompose | `stress_decompose.py` | c1/c2/c3 driver labels |

### Quality gates

- SHAP rank stability Spearman > 0.7
- Attention–adjacency Spearman > 0.3
- SHAP–permutation Spearman > 0.5
- Top-2 group agreement ≥ 60%

### Case-study selection (20 dates)

5 high OSI + 5 low OSI + 5 peak demand + 5 shedding events (Phase 12).
