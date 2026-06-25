# Training Decision Report — Phase 10

Generated: 2026-06-24

## Frozen decisions summary

### Benchmark models (7)

Linear Regression, Random Forest, XGBoost, LSTM, GRU, T-GCN, PF-STGT

### Evaluation metrics

- **Demand:** MAE, RMSE, MAPE, R² (macro + Dhaka)
- **Stress:** MAE, RMSE, R² (+ Pearson r supplementary)

### Training defaults (deep models)

| Parameter | Frozen value |
| --- | --- |
| Batch size | 32 |
| Learning rate | 0.0005 |
| Optimizer | AdamW |
| Weight decay | 0.0001 |
| Early stopping patience | 15 |
| Max epochs | 200 |
| Seeds | [42, 123, 456] |

### Loss functions

- PF-STGT: λ1=1.0 Huber + λ2=0.5 MSE
- Deep baselines: Huber δ=1.0 MW
- Classical: library default squared error

### Validation protocol

- Chronological 70/15/15 split (Phase 04)
- Model selection on validation macro demand MAE
- Single final test evaluation
- Train-only fit; no test leakage (Phase 06)

## Window and sample counts

| Split | Raw rows | Approx. windows (T=7) |
| --- | --- | --- |
| Train | 1295 | ~1287 |
| Validation | 277 | ~269 |
| Test | 278 | ~270 |

## Next phase

Implement benchmark trainers per `experiments/` protocol; no results generated in Phase 10.
