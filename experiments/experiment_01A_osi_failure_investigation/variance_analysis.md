# Variance Collapse Analysis — Experiment 01A

## Standard deviation comparison

| Split | std(actual) | std(predicted) | std ratio (pred/act) | variance ratio |
| --- | --- | --- | --- | --- |
| train | 0.0839 | 0.0000 | 0.0000 | 0.0000 |
| validation | 0.0656 | 0.0000 | 0.0000 | 0.0000 |
| test | 0.0938 | 0.0000 | 0.0000 | 0.0000 |

## Collapse diagnosis

- Validation std ratio: **0.0000** (predicted variance is 100.0% lower than actual).
- Mean-baseline MSE on validation: **0.004284**
- Model validation stress MSE: **0.092269**

## Interpretation

- std(predicted) ≪ std(actual) on every split → classic **variance collapse**.
- Negative R² in Experiment 01 occurs because flat predictions have higher error than predicting the split mean.
- Collapse is consistent with the stress head receiving weak gradient signal relative to demand (see loss_weight_analysis.md).
