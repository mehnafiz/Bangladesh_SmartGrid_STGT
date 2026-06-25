# SHAP Design — Phase 12 (Feature Attribution)

Generated: 2026-06-24
Status: **FROZEN**

## Level 1 — Global & local feature attribution

### SHAP variant selection

| Target | SHAP method | Background dataset |
| --- | --- | --- |
| Task 1 demand (per region) | **GradientSHAP** on demand head | 100 train windows (stratified by season) |
| Task 2 OSI | **GradientSHAP** on stress head | 100 train windows (include high/low OSI) |
| Global ranking | **Grouped SHAP** (11 coalitions) | Same background |

### Feature coalitions (leakage-safe groups)

| group_id   | group_name                  | scope   | features                                                                | tasks         | shap_coalition   |
|:-----------|:----------------------------|:--------|:------------------------------------------------------------------------|:--------------|:-----------------|
| G1         | regional_demand_block       | node    | 9 × {Region}_demand                                                     | demand;stress | True             |
| G2         | regional_supply_block       | node    | 9 × {Region}_supply                                                     | demand        | True             |
| G3         | regional_load_block         | node    | 9 × {Region}_load                                                       | demand;stress | True             |
| G4         | engineered_lags_rolling     | node    | demand_lag_1/7, load_lag_1, rolling_mean_7 × 9                          | demand        | True             |
| G5         | regional_share_intensity    | node    | regional_demand_share, regional_load_intensity × 9                      | demand;stress | True             |
| G6         | calendar_trend              | global  | day_of_year_sin/cos, trend_index, gap_days, Holiday_cat                 | demand;stress | True             |
| G7         | grid_aggregates             | global  | total_regional_demand, total_regional_load, generation_reserve          | demand;stress | True             |
| G8         | limitation_stack            | global  | gas, coal, water, maintenance limitations, total_operational_limitation | stress;demand | True             |
| G9         | weather_anomaly             | global  | temperature_anomaly_month                                               | demand        | True             |
| G10        | national_generation_scalars | global  | Max eve peak gen-end, Highest Generation                                | demand;stress | True             |
| G11        | shedding_indicator          | global  | any_regional_shedding                                                   | stress        | True             |

### Output artefacts (implementation phase)

```
results/explainability/shap/demand_shap_values_{region}.csv
results/explainability/shap/stress_shap_values.csv
results/explainability/shap/global_shap_summary.png
results/explainability/shap/shap_beeswarm_demand_dhaka.png
```

### Correlation caution (Phase 07B R-05)

- Report **group-level SHAP** first; then drill to features within top groups.
- Demand≈supply collinearity (Phase 02): interpret G1/G2 jointly, not competitively.
- Use `shap_interaction_values` optionally for Dhaka–national aggregate pairs only.

### Computational budget

| Item | Estimate |
| --- | --- |
| Background samples | 100 |
| GradientSHAP steps | 50 per explanation |
| Full val split (~270 windows) | ~2–4 GPU-hours (batched) |
| Case-study subset (20 days) | ~15 min |

**Publication default:** report SHAP on **20 stratified case-study days** (5 high OSI, 5 low, 5 peak demand, 5 shedding).
