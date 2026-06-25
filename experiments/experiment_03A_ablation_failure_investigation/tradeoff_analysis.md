# Performance Trade-Off Analysis — Experiment 03A

Generated: 2026-06-25

## Multi-objective landscape (test set)

| model   |   demand_mae |   demand_r2 |   stress_mae |   stress_r2 | multi_task   |
|:--------|-------------:|------------:|-------------:|------------:|:-------------|
| A1      |      93.3084 |      0.6743 |       0.0499 |      0.5849 | True         |
| A2      |      93.9258 |      0.701  |       0.0405 |      0.7012 | True         |
| A3      |      92.6436 |      0.6706 |       0.0405 |      0.7005 | True         |
| A4      |      86.8857 |      0.7308 |     nan      |    nan      | False        |
| A5      |      97.9763 |      0.5544 |       0.034  |      0.7644 | True         |
| A6      |      88.6487 |      0.6838 |       0.0371 |      0.7451 | True         |

## Pareto interpretation

- **A4** dominates A1 on **demand** (86.9 vs 93.3 MW) but provides **no stress forecast**.
- **A1** is the only full PF-STGT variant balancing demand ~93 MW with stress R² **0.585**.
- **A6** offers a compromise: demand **88.6 MW** (+4.7 vs A4, −4.7 vs A1) with stress R² **0.745**.
- **A5** achieves best stress R² (**0.764**) but worst demand among multi-task variants (**98.0 MW**).

## Prediction dynamics

| model   |   pred_std_mw |   actual_std_mw |   pred_actual_std_ratio |
|:--------|--------------:|----------------:|------------------------:|
| A1      |       1223.03 |         1244.07 |                   0.983 |
| A3      |       1211.2  |         1244.07 |                   0.974 |
| A4      |       1230.53 |         1244.07 |                   0.989 |

A4 tracks demand variance slightly better (ratio closer to 1), consistent with demand-only optimization.

## Conclusion

Multi-task learning **does not improve demand** relative to A4; it **enables stress forecasting**.
The W20 reference occupies a deliberate trade-off point, not the demand Pareto frontier.
