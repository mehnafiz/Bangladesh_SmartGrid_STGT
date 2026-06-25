# Demand–OSI Correlation Analysis — Experiment 01A

## Total demand vs OSI

| Split | Pearson(demand, OSI actual) | Spearman(demand, OSI actual) | Pearson(demand, OSI pred) | Spearman(demand, OSI pred) |
| --- | --- | --- | --- | --- |
| train | -0.1364 | -0.1197 | -0.2600 | -0.9668 |
| validation | -0.7440 | -0.7889 | -0.2959 | -0.9540 |
| test | -0.4433 | -0.3878 | -0.3329 | -0.8868 |

## Demand error vs OSI error (validation)

- Pearson(per-sample demand MAE, |OSI error|): **-0.1241**

## Observations

- Actual demand–OSI correlation is moderate; OSI is not a simple linear function of aggregate demand alone.
- Predicted OSI shows near-zero correlation with demand because predictions are nearly constant.
- Multi-task coupling via shared fusion is insufficient when stress gradients are suppressed by loss scaling and early-stopping criterion.
