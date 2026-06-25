# Loss Weight Sensitivity Analysis — Experiment 01A

**Note:** No retraining performed. Analysis uses Experiment 01 checkpoint and counterfactual λ₂ values.

## Current configuration (Experiment 01)

- λ₁ (demand) = 1.0
- λ₂ (stress) = 0.5
- Early stopping monitors **validation macro demand MAE only** (stress ignored).

At best epoch 35:
- Train demand loss: 61.83
- Train stress loss: 0.092080
- Val demand MAE: 56.67
- Val stress MAE: 0.2966

## Counterfactual λ₂ on a validation batch (gradient probe, no weight update)

| λ₂ | L_demand | L_stress | L_demand/L_stress | Demand share | Stress share | ‖∇‖ demand head | ‖∇‖ stress head |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5 | 60.73 | 0.059081 | 1028 | 100.0% | 0.05% | 285.6312 | 0.000000 |
| 1.0 | 60.73 | 0.059081 | 1028 | 99.9% | 0.10% | 285.6312 | 0.000000 |
| 2.0 | 60.73 | 0.059081 | 1028 | 99.8% | 0.19% | 285.6312 | 0.000000 |

## Sensitivity summary

- Raw loss ratio L_demand/L_stress ≈ **1028:1** at best-epoch scale.
- At λ₂=0.5, demand contributes **100.0%** of total loss; stress **0.05%**.
- Stress head L2 gradient norm ≈ **0.000000** vs demand head **285.6312** → stress head effectively starved.
- Raising λ₂ to 2.0 increases stress loss share only to **0.19%** (still negligible vs demand).
- Training logs show val stress MAE plateauing at ~0.2966 (= validation OSI mean) for many epochs while demand MAE improved.

## Recommendation (no architecture change)

1. Increase λ₂ (e.g. 5–20) **or** normalize demand loss to [0,1] scale before combining.
2. Use combined early-stopping criterion (demand MAE + weighted stress MAE).
3. Consider stress-only fine-tuning phase from Experiment 01 checkpoint.
