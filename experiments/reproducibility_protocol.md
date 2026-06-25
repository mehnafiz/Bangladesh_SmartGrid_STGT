# Reproducibility Protocol — Phase 10

Generated: 2026-06-24
Status: **FROZEN**

## Data versioning

| Artifact | Path | Verification |
| --- | --- | --- |
| Raw dataset | `data/raw/bangladesh_smartgrid_raw.csv` | MD5 in Phase 01 |
| Feature splits | `data/features/*_features.parquet` | MD5 before/after training |
| Adjacency | `graphs/adjacency_matrix.csv` | MD5 in Phase 08 |
| Preprocessing | `models/preprocessing_pipeline.pkl` | Phase 04 frozen |

## Chronological split (Phase 04 — immutable)

| Split | Rows | Dates |
| --- | --- | --- |
| Train | 1295 | 2019-11-21 → 2023-06-15 |
| Validation | 277 | 2023-06-16 → 2024-03-19 |
| Test | 278 | 2024-03-20 → 2024-12-30 |

- No shuffling across time.
- No refitting scalers/encoders on val/test.
- Window builder uses only past observations within split (+ train history for val/test lag features per Phase 06).

## Random seed control

| Component | Seed |
| --- | --- |
| Deep learning runs | [42, 123, 456] |
| NumPy / Python / PyTorch | Set per run; document in config |
| Classical ML | 42 |

## Experiment configuration files (implementation phase)

```
configs/experiments/{benchmark_id}.yaml
configs/experiments/pf_stgt.yaml
configs/experiments/protocol_phase10.yaml   # frozen constants from this phase
```

Each config must record: benchmark_id, seed, split paths, T, h, λ1, λ2, batch_size, lr.

## Logging requirements

- Per-epoch: train/val loss components, macro demand MAE, stress MAE (PF-STGT).
- Final: test metrics JSON + CSV per region.
- Hardware: CPU/GPU model, PyTorch version, wall-clock time.

## Test protocol (single pass)

1. Select hyperparameters on **validation** only.
2. Retrain on train+val OR load best-val checkpoint from train-only (document choice).
   - **Frozen choice:** train-only with best-val checkpoint (no val data in final fit).
3. Evaluate once on **test**; no test feedback loop.

## GAP-08 alignment

Explicit split documentation, fixed seeds, and published leaderboard CSVs address 
reproducibility gap identified in 52/55 metadata-sparse literature papers (Phase 07C).
