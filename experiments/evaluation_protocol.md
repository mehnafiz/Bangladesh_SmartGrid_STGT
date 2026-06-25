# Evaluation Protocol — Phase 10

Generated: 2026-06-24
Status: **FROZEN**

## Evaluation scope

- **Primary comparison:** Task 1 regional demand forecasting (all 7 benchmarks).
- **Secondary evaluation:** Task 2 OSI forecasting (PF-STGT only + non-model baselines).
- **Final reporting:** Test split only, once after model selection on validation.

## Task 1 — Demand forecasting metrics (frozen)

| Metric | Formula | Aggregation |
| --- | --- | --- |
| **MAE** | mean(\|y − ŷ\|) MW | Macro-mean over 9 regions + national weighted |
| **RMSE** | sqrt(mean((y − ŷ)²)) MW | Macro-mean over 9 regions |
| **MAPE** | mean(\|y − ŷ\| / \|y\|) × 100% | Macro-mean; exclude y=0 rows |
| **R²** | 1 − SS_res/SS_tot | Macro-mean over 9 regions |

### Aggregation rules

1. Compute each metric **per region** on test split.
2. Report **macro-average** (unweighted mean over 9 regions) as primary leaderboard score.
3. Report **Dhaka** separately (Phase 02: ~35.7% national share).
4. Optional: national eve-peak demand derived from Σ regional predictions for appendix.

## Task 2 — Operational stress metrics (frozen)

| Metric | Formula | Notes |
| --- | --- | --- |
| **MAE** | mean(\|OSI − OSI_hat\|) | Primary |
| **RMSE** | sqrt(mean((OSI − OSI_hat)²)) | Primary |
| **R²** | 1 − SS_res/SS_tot | Primary |
| Pearson r | corr(OSI, OSI_hat) | Supplementary (Phase 09) |

### Non-model OSI baselines (context only, not benchmark models)

| Baseline | Definition |
| --- | --- |
| Persistence | OSI_hat(t+1) = OSI(t) |
| Train median | OSI_hat = median(OSI_train) |

## Statistical reporting

- Deep models (B04–B07): **3 seeds** [42, 123, 456] → report mean ± std on test.
- Classical ML (B01–B03): single deterministic fit (seed=42 where applicable).
- No test-set hyperparameter tuning.

## Leaderboard format (implementation phase)

```
results/experiments/leaderboard_demand_test.csv
results/experiments/leaderboard_stress_test.csv
results/experiments/per_region_metrics_test.csv
```

## Comparison to literature (Phase 07B/07C)

- Report MAPE alongside MAE for cross-paper comparability (20/55 load forecasting papers).
- Document chronological split explicitly (GAP-08 vs metadata-sparse conference baselines).
- PF-STGT must beat T-GCN on macro MAE **and** report stress R² to support GAP-02/GAP-06 claims.
