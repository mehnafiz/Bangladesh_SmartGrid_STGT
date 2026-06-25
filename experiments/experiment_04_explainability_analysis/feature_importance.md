# Feature Importance — Experiment 04

Generated: 2026-06-25

Coalition-level permutation importance on validation (8 batches, demand MAE degradation).

| group_id   | group_name                  |   perm_mean_delta |   shap_abs_phi |
|:-----------|:----------------------------|------------------:|---------------:|
| G2         | regional_supply_block       |         1.95548   |       77.4125  |
| G3         | regional_load_block         |         1.01264   |        2.28269 |
| G1         | regional_demand_block       |         0.648988  |       77.7173  |
| G5         | regional_share_intensity    |         0.641831  |       69.4519  |
| G8         | limitation_stack            |         0.598711  |       23.1467  |
| G10        | national_generation_scalars |         0.422718  |       91.4362  |
| G7         | grid_aggregates             |         0.293888  |       85.8438  |
| G9         | weather_anomaly             |         0.267737  |       10.869   |
| G6         | calendar_trend              |         0.0772366 |      162.34    |
| G4         | engineered_lags_rolling     |         0.0128904 |      101.257   |

### Top stress permutation groups

| group_id   | group_name                  |   mean_delta |
|:-----------|:----------------------------|-------------:|
| G8         | limitation_stack            |  3.80105e-05 |
| G5         | regional_share_intensity    |  1.67651e-05 |
| G6         | calendar_trend              |  2.79322e-06 |
| G11        | shedding_indicator          |  4.08912e-07 |
| G1         | regional_demand_block       |  5.06137e-08 |
| G3         | regional_load_block         |  0           |
| G7         | grid_aggregates             |  0           |
| G10        | national_generation_scalars |  0           |

Figure: `figures/figure_feature_importance_ranking.png`
