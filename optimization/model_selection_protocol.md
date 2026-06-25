# Model Selection Protocol — Phase 11

Generated: 2026-06-24
Status: **FROZEN**

## Selection stages

| Stage | Data used | Decision |
| --- | --- | --- |
| Stage 1 HPO | Val | Rank 20 trials |
| Stage 2 confirmation | Val | Pick 1 config among top-3 |
| Stage 3 test | Test | Report final metrics (no re-selection) |

## Primary metric (frozen)

**validation_macro_demand_MAE** — macro-averaged MAE over 9 regional demand forecasts on validation split.

- Unit: MW
- Aligns with Phase 10 leaderboard and Phase 08.5 Task 1 priority.
- Computed on inverse-scaled predictions if training used normalised targets.

## Secondary metrics

| Metric | Role |
| --- | --- |
| **validation_stress_MAE** | Required for PF-STGT multi-task quality (Phase 08.5 Task 2) |
| validation_combined_loss | Diagnostic (λ1·Huber + λ2·MSE) |
| validation_demand_MAPE | Tie-breaker only (scale-sensitive) |
| validation_stress_R2 | Tie-breaker for stress quality |

## Tie-breaking strategy (frozen order)

When primary metrics are equal within **0.05 MW** tolerance:

1. Lower **validation stress MAE** (secondary).
2. Lower **validation combined loss**.
3. **Simpler model:** lower `L_s + L_t`, then lower `d_model`.
4. Higher **validation stress R²**.
5. Default Phase 09 config if still tied.

## Final config selection (Stage 2)

```
config* = argmin_{c ∈ top-3} mean_seed∈{42,123,456} val_macro_demand_MAE(c, seed)
seed*   = argmin_seed val_macro_demand_MAE(config*, seed)
```

## Test-phase rules

- **No hyperparameter changes** after Stage 2.
- **No test-set peeking** during HPO or confirmation.
- Report test metrics for config* only (+ Phase 09 default as ablation row).

## Overfitting safeguards

- Cap trials at 20 (≈1 trial per 14 validation windows — conservative ratio).
- Prefer simpler models on tie-break (Occam's razor for n≈270 val samples).
- Log train vs val MAE gap; flag trials with gap > 30% for manual review.
