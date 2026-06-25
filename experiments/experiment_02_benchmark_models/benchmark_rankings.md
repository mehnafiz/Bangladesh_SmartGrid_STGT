# Benchmark Rankings — Experiment 02

## Demand forecasting (test, primary rank by MAE)

| Rank | ID | Model | MAE | RMSE | MAPE | R² |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | B07 | PF-STGT (W20) | 93.31 | 128.81 | 6.76 | 0.6743 |
| 2 | B02 | Random Forest | 97.03 | 156.99 | 7.04 | 0.9841 |
| 3 | B03 | XGBoost | 109.73 | 178.53 | 7.99 | 0.9794 |
| 4 | B05 | GRU | 233.48 | 274.39 | 14.13 | -0.2014 |
| 5 | B04 | LSTM | 237.03 | 278.67 | 14.35 | -0.2415 |
| 6 | B01 | Linear Regression | 247.79 | 597.01 | 17.32 | 0.7697 |
| 7 | B06 | T-GCN | 257.21 | 301.06 | 15.72 | -0.4832 |

## Stress forecasting (test, rank by MAE)

| Rank | ID | Model | MAE | RMSE | R² |
| --- | --- | --- | --- | --- | --- |
| 1 | B02 | Random Forest | 0.0481 | 0.0624 | 0.5554 |
| 2 | B03 | XGBoost | 0.0497 | 0.0646 | 0.5245 |
| 3 | B07 | PF-STGT (W20) | 0.0499 | 0.0603 | 0.5849 |
| 4 | B04 | LSTM | 0.0861 | 0.1022 | -0.1910 |
| 5 | B05 | GRU | 0.0863 | 0.1032 | -0.2144 |
| 6 | B06 | T-GCN | 0.0891 | 0.1069 | -0.3042 |
| 7 | B01 | Linear Regression | 0.1074 | 0.1573 | -1.8243 |

**Best overall (demand MAE):** PF-STGT (W20) (B07)
