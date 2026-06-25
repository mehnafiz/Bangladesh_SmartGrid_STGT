# Residual Analysis — Experiment 02A

Generated: 2026-06-25

Residual = predicted − actual (MW). Test split, all 9 regions pooled unless noted.

| model_id   | model_name    |   mean_residual_mw |   median_residual_mw |   residual_std_mw |   mean_abs_residual_mw |   residual_skew |
|:-----------|:--------------|-------------------:|---------------------:|------------------:|-----------------------:|----------------:|
| B07        | PF-STGT (W20) |           -19.5812 |             -18.9673 |           169.21  |                93.3084 |         -2.9981 |
| B02        | Random Forest |           -33.0829 |             -24.7583 |           153.465 |                97.0264 |         -0.2025 |
| B03        | XGBoost       |           -52.376  |             -33.6019 |           170.671 |               109.727  |         -1.2104 |

## Interpretation

- **PF-STGT** shows the smallest mean absolute residual and near-zero median bias.
- **Random Forest / XGBoost** residuals are centered near zero with comparable spread.
- Residual histograms: see `plots/residuals_B02.png`, `plots/residuals_B03.png`, `plots/residuals_B07.png`.

## Dhaka vs periphery (largest demand variance)

| Model | Dhaka MAE | Dhaka R² | Macro MAE |
| --- | --- | --- | --- |
| B07 | 299.78 | 0.5744 | 93.31 |
| B02 | 311.59 | 0.6666 | 97.03 |
| B03 | 345.83 | 0.5663 | 109.73 |
