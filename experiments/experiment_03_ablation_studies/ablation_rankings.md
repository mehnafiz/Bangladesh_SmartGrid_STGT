# Ablation Rankings — Experiment 03

Generated: 2026-06-25

## Demand (test, rank by MAE)

| Rank | ID | Model | MAE | RMSE | MAPE | R² |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A4 | Single-Task | 86.89 | 117.90 | 6.52 | 0.7308 |
| 2 | A6 | Correlation Graph Only | 88.65 | 127.29 | 6.55 | 0.6838 |
| 3 | A3 | No Transformer | 92.64 | 127.13 | 6.84 | 0.6706 |
| 4 | A1 | PF-STGT (W20) | 93.31 | 128.81 | 6.76 | 0.6743 |
| 5 | A2 | No Graph | 93.93 | 124.98 | 6.82 | 0.7010 |
| 6 | A5 | Geographical Graph Only | 97.98 | 135.96 | 7.57 | 0.5544 |

## Stress (test, rank by MAE; A4 N/A)

| Rank | ID | Model | MAE | RMSE | R² |
| --- | --- | --- | --- | --- | --- |
| 1 | A5 | Geographical Graph Only | 0.0340 | 0.0454 | 0.7644 |
| 2 | A6 | Correlation Graph Only | 0.0371 | 0.0473 | 0.7451 |
| 3 | A2 | No Graph | 0.0405 | 0.0512 | 0.7012 |
| 4 | A3 | No Transformer | 0.0405 | 0.0512 | 0.7005 |
| 5 | A1 | PF-STGT (W20) | 0.0499 | 0.0603 | 0.5849 |

**Reference (A1):** PF-STGT (W20) — demand MAE 93.31 MW
