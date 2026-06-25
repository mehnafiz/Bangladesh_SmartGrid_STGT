# Component Contribution Framework — Phase 13

Generated: 2026-06-24
Status: **FROZEN**

## Contribution metrics

For each ablation variant v vs reference A1 on **test split**:

```
ΔMAE_v   = MAE_v − MAE_A1          (positive = variant worse)
ΔRMSE_v  = RMSE_v − RMSE_A1
ΔMAPE_v  = MAPE_v − MAPE_A1
ΔR²_v    = R²_A1 − R²_v            (positive = variant worse)

Relative demand degradation:
  RD_v = ΔMAE_v / MAE_A1 × 100%
```

### Stress task (multi-task variants only)

```
ΔMAE_OSI_v = MAE_OSI_v − MAE_OSI_A1     (A4: stress undefined → report N/A)
ΔR²_OSI_v  = R²_OSI_A1 − R²_OSI_v
```

## Component attribution interpretation

| Component | Comparison | Expected signal if component matters |
| --- | --- | --- |
| Graph module | A1 vs A2 | ΔMAE_A2 > 0 significant |
| Transformer | A1 vs A3 | ΔMAE_A3 > 0 significant |
| Multi-task | A1 vs A4 | ΔMAE_A4 > 0 OR ΔR²_OSI_A4 = N/A |
| Hybrid graph | A1 vs A5-GEO | ΔMAE_GEO > 0 |
| Hybrid vs corr | A1 vs A5-CORR | Compare MAE and graph density tradeoff |
| Explainability trunk | A1 vs A6 | ΔMAE_A6 small if XAI is low-cost |

## Contribution decomposition table (implementation output)

```
results/ablation/component_contributions.csv
```

| Column | Description |
| --- | --- |
| ablation_id | Variant ID |
| delta_mae_mw | Test MAE change vs A1 |
| relative_degradation_pct | ΔMAE / MAE_A1 |
| significant | Wilcoxon p < α_adj |
| component_verdict | Supports / Does not support hypothesis |

## Graph study summary metrics

Report alongside demand metrics:

- Edge density vs MAE scatter (A5-GEO, A5-CORR, A1)
- Spearman(attention, A_ij) per graph variant

## Multi-task benefit criteria

Multi-task learning **supported** if ALL hold:

1. A1 demand MAE ≤ A4 demand MAE (within 0.05 MW or significant).
2. A1 stress MAE < persistence baseline (Phase 10).
3. No collapse: A1 stress R² > 0 on test.

## Explainability tradeoff criteria

Explainability pathway **justified** if:

1. |ΔMAE_A6| / MAE_A1 < 5% (performance cost acceptable), OR
2. A6-XAI attention–SHAP agreement ≥ 60% (Phase 12 protocol) AND A6 lacks native maps.
