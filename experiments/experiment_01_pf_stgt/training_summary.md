# Experiment 01 — Training Summary

Generated: 2026-06-24

## Run metadata

- Seed: 42
- Device: mps
- Parameters: 749,058
- Training time: 281.2s
- Epochs run: 50
- Best epoch: 35
- Early stopping epoch: 50
- Stopped early: True

## Validation metrics (best checkpoint)

| Metric | Demand | Stress |
| --- | --- | --- |
| MAE | 56.6708 | 0.2966 |
| RMSE | 76.8344 | 0.3038 |
| MAPE | 4.5926 | — |
| R² | 0.8780 | -20.5387 |

## Test metrics (best checkpoint)

| Metric | Demand | Stress |
| --- | --- | --- |
| MAE | 86.8181 | 0.3375 |
| RMSE | 118.3754 | 0.3502 |
| MAPE | 6.5199 | — |
| R² | 0.7299 | -12.9918 |

## Outputs

- `best_model.pt`
- `metrics.json`
- `train_loss.png`
- `val_loss.png`
- `training_log.txt`
