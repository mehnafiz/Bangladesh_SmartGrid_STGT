# Component Contribution — Experiment 03

Generated: 2026-06-25

ΔMAE = ablation MAE − A1 MAE (positive ⇒ removing/changing component hurts).
ΔR² = A1 R² − ablation R² (positive ⇒ component helps variance explanation).

| component                   | ablation_id   |   delta_mae_mw |   relative_degradation_pct |   delta_r2 |   stress_delta_mae | verdict               |
|:----------------------------|:--------------|---------------:|---------------------------:|-----------:|-------------------:|:----------------------|
| Graph module                | A2            |         0.6174 |                     0.6616 |    -0.0267 |            -0.0094 | Supports component    |
| Transformer module          | A3            |        -0.6648 |                    -0.7124 |     0.0037 |            -0.0094 | No measurable benefit |
| Multi-task learning         | A4            |        -6.4226 |                    -6.8832 |    -0.0565 |           nan      | No measurable benefit |
| Hybrid graph (vs geo-only)  | A5            |         4.668  |                     5.0027 |     0.1199 |            -0.016  | Supports component    |
| Hybrid graph (vs corr-only) | A6            |        -4.6597 |                    -4.9938 |    -0.0095 |            -0.0129 | No measurable benefit |

## Summary

- **Graph module (A2):** ΔMAE = +0.62 MW
- **Transformer (A3):** ΔMAE = -0.66 MW
- **Multi-task (A4):** ΔMAE = -6.42 MW
- **Hybrid vs geo-only (A5):** ΔMAE = +4.67 MW
- **Hybrid vs corr-only (A6):** ΔMAE = -4.66 MW
