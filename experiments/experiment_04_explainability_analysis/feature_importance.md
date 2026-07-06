# Feature Importance — Experiment 04

Generated: 2026-07-06

Coalition-level permutation importance on validation (8 batches, demand MAE degradation).

| group_id   | group_name                  |   perm_mean_delta |   shap_abs_phi |
|:-----------|:----------------------------|------------------:|---------------:|
| G1         | regional_demand_block       |         1.34764   |       77.7173  |
| G2         | regional_supply_block       |         1.33833   |       77.4125  |
| G5         | regional_share_intensity    |         1.28231   |       69.4519  |
| G3         | regional_load_block         |         0.788379  |        2.28269 |
| G10        | national_generation_scalars |         0.561348  |       91.4362  |
| G7         | grid_aggregates             |         0.48936   |       85.8438  |
| G8         | limitation_stack            |         0.429027  |       23.1467  |
| G9         | weather_anomaly             |         0.425121  |       10.869   |
| G6         | calendar_trend              |         0.0610659 |      162.34    |
| G4         | engineered_lags_rolling     |         0         |      101.257   |

### Top stress permutation groups

| group_id   | group_name                  |   mean_delta |
|:-----------|:----------------------------|-------------:|
| G8         | limitation_stack            |  5.23921e-05 |
| G5         | regional_share_intensity    |  9.10966e-06 |
| G6         | calendar_trend              |  6.06447e-07 |
| G1         | regional_demand_block       |  0           |
| G3         | regional_load_block         |  0           |
| G7         | grid_aggregates             |  0           |
| G10        | national_generation_scalars |  0           |
| G11        | shedding_indicator          |  0           |

Figure: `figures/figure_feature_importance_ranking.png`
