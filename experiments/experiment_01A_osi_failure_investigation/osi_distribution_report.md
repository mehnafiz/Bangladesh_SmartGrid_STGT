# OSI Distribution Report — Experiment 01A

## Summary

Ground-truth OSI(t+1) distribution across chronological splits.

| Split | N | Mean | Std | Min | Max | Skewness |
| --- | --- | --- | --- | --- | --- | --- |
| train | 1281 | 0.2881 | 0.0839 | 0.0613 | 0.7113 | 0.8865 |
| validation | 263 | 0.2966 | 0.0656 | 0.1842 | 0.5592 | 0.9946 |
| test | 264 | 0.3375 | 0.0938 | 0.1570 | 0.5646 | 0.1117 |

## Observations

- Train OSI std: **0.0839** — target signal is narrow (bounded [0, 1]).
- Validation OSI std: **0.0656**
- Test OSI std: **0.0938**
- OSI is a composite scalar with limited dynamic range; small absolute errors can still yield poor R² when variance is low.

## Experiment 01 reference metrics

- Val stress MAE: 0.2966
- Val stress R²: -20.5387
- Test stress MAE: 0.3375
- Test stress R²: -12.9918
