# Best Configuration — Experiment 01B

**Recommended config:** `W20`

## Settings

- λ₂ (stress weight): **20.0**
- Demand loss normalization: **Yes (÷100 MW)**
- Balanced early stopping: **Yes (0.7·MAE/100 + 0.3·stress_MAE)**
- Seed: 42 (unchanged)

## Validation performance

| Metric | Value |
| --- | --- |
| Demand MAE | 61.64 MW |
| Demand R² | 0.8630 |
| Stress MAE | 0.0321 |
| Stress R² | 0.6373 |
| OSI pred std | 0.0674 |
| Stress Pearson r | 0.8917 |

## Test performance

| Demand R² | 0.6743 |
| Stress R² | 0.5849 |
| OSI pred std | 0.0977 |

## vs Experiment 01

- Demand R² change: -0.0150
- Stress R² change: +21.1761
- OSI variance restored: 0.0674 (was 0.0)
