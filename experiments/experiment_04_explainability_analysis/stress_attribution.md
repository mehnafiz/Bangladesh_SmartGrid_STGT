# Stress Attribution — Experiment 04

Generated: 2026-06-25

## Global stress drivers (SHAP)

| Group | Name | φ |
| --- | --- | --- |
| G8 | limitation_stack | 0.0191 |
| G6 | calendar_trend | 0.0190 |
| G7 | grid_aggregates | 0.0087 |
| G10 | national_generation_scalars | 0.0082 |
| G5 | regional_share_intensity | 0.0046 |
| G1 | regional_demand_block | 0.0042 |

## Dual-pathway validation

- Case-study driver agreement rate: **52.2%**
- Path A: grouped SHAP on stress head
- Path B: OSI c1/c2/c3 component decomposition at t+1

Priority stress coalitions: G7 (grid aggregates), G8 (limitations), G3 (load), G11 (shedding).

Figure: `figures/figure_stress_attribution.png`
