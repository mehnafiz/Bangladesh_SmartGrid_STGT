# SHAP Summary — Experiment 04

Generated: 2026-07-06

## Model

- Architecture: **S2** (Correlation-Only PF-STGT)
- Checkpoint: `/Users/mehnafiz/Documents/SEMESTER/Research Paper/Gomes Sir/FInal_DL/Bangladesh_SmartGrid_STGT/experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt`
- Method: grouped integrated gradients (25 steps, zero baseline)

## Global stress SHAP (validation, n=20)

| Rank | Group | Name | φ |
| --- | --- | --- | --- |
| 1 | G8 | limitation_stack | 0.0191 |
| 2 | G6 | calendar_trend | 0.0190 |
| 3 | G7 | grid_aggregates | 0.0087 |
| 4 | G10 | national_generation_scalars | 0.0082 |
| 5 | G5 | regional_share_intensity | 0.0046 |
| 6 | G1 | regional_demand_block | 0.0042 |
| 7 | G3 | regional_load_block | 0.0014 |
| 8 | G11 | shedding_indicator | 0.0013 |

## Global demand SHAP — Dhaka (validation, n=20)

| Rank | Group | Name | φ |
| --- | --- | --- | --- |
| 1 | G6 | calendar_trend | 162.3395 |
| 2 | G4 | engineered_lags_rolling | 101.2568 |
| 3 | G10 | national_generation_scalars | 91.4362 |
| 4 | G7 | grid_aggregates | 85.8438 |
| 5 | G1 | regional_demand_block | 77.7173 |
| 6 | G2 | regional_supply_block | 77.4125 |
| 7 | G5 | regional_share_intensity | 69.4519 |
| 8 | G8 | limitation_stack | 23.1467 |

## Quality

- SHAP–permutation Spearman (demand): **-0.345**
- SHAP–permutation Spearman (stress): **0.627**

## Figures

- `figures/figure_shap_summary_stress.png`
- `figures/figure_shap_summary_demand.png`
- `figures/figure_shap_bar_stress.png`
