# Task Interference Report — Experiment 03A

Generated: 2026-06-25

## Question

Does multi-task optimization (W20) interfere with demand forecasting, explaining why A4 beats A1?

## Evidence

### 1. Performance gap (test set)

- A1 demand MAE: **93.31 MW**
- A4 demand MAE: **86.89 MW** (Δ = -6.42 MW)
- Wilcoxon A1 vs A4: median daily Δ = **−5.25 MW**, p = **0.0028** (A4 better; not Bonferroni-framed as component test but strong)

### 2. Conflicting training objectives

| Setting | A1 (W20 reference) | A4 (Single-Task) |
| --- | --- | --- |
| Stress loss weight λ₂ | 20 | 0 |
| Early stopping | 0.7·(MAE/100) + 0.3·stress_MAE | Val demand MAE only |
| Checkpoint source | Experiment 01B W20 (pre-trained) | Fresh Exp03 demand-only training |

A1 checkpoint was selected to balance **demand and stress**, not to minimize test demand MAE.
A4 checkpoint was selected to minimize **demand MAE only**.

### 3. Gradient probe on A1 (validation batch, W20 loss)

|   demand_loss_raw |   stress_loss_raw |   demand_term_normalized |   stress_term_weighted |   demand_head_grad_l2 |   stress_head_grad_l2 |   shared_backbone_grad_l2 |   grad_ratio_demand_over_stress |   loss_ratio_demand_over_stress_weighted |
|------------------:|------------------:|-------------------------:|-----------------------:|----------------------:|----------------------:|--------------------------:|--------------------------------:|-----------------------------------------:|
|           70.0056 |            0.0011 |                   0.7001 |                 0.0215 |                2.3904 |               13.5317 |                    2.8277 |                          0.1767 |                                  32.5635 |

- Normalized demand loss term is **32.6×** the weighted stress term.
- Despite smaller stress **loss**, stress-head gradient L2 (**13.53**) exceeds demand-head (**2.39**) by **5.7×**.

Shared trunk receives gradients from both tasks; stress optimization pulls representations
toward OSI-relevant features that need not align with per-region demand minimization.

### 4. Regional pattern

- Largest A4 gain vs A1 is **Dhaka**: ΔMAE = **-14.7 MW**.
- Dhaka dominates national variance; multi-task + balanced ES under-weights pure demand fit there.

## Conclusion

**Yes — task interference and objective mismatch are supported.** A4 wins on demand because it
trains and selects checkpoints under a single-task criterion, while A1 (W20) explicitly trades
demand MAE for joint stress performance (A1 stress R² = 0.585 vs A4 N/A).
