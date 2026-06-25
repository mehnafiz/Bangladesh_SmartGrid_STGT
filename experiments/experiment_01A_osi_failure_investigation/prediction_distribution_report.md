# Prediction Distribution Report — Experiment 01A

## Actual vs Predicted OSI

| Split | Actual Mean | Pred Mean | Actual Std | Pred Std | MAE |
| --- | --- | --- | --- | --- | --- |
| train | 0.2881 | 0.0000 | 0.0839 | 0.0000 | 0.2881 |
| validation | 0.2966 | 0.0000 | 0.0656 | 0.0000 | 0.2966 |
| test | 0.3375 | 0.0000 | 0.0938 | 0.0000 | 0.3375 |

## Validation detail

- Unique predicted values (4 d.p.): **1**
- Fraction of predictions within ±0.01 of prediction mean: **100.0%**
- Prediction range: [0.0000, 0.0000]
- Actual range: [0.1842, 0.5592]

## Observations

- Predicted OSI std is zero on all splits → **complete variance collapse**.
- Validation predictions are constant at **0.0000**; MAE ≈ validation OSI mean (0.2966) → equivalent to predicting a fixed scalar.
- Negative R² occurs because this constant is farther from targets than the split mean baseline.
