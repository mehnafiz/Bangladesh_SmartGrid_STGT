# Training Strategy — Phase 10

Generated: 2026-06-24
Status: **FROZEN**

## Applicable models

Deep learning training protocol applies to **B04 LSTM, B05 GRU, B06 T-GCN, B07 PF-STGT**.
Classical ML (B01–B03) uses library defaults with hyperparameter grid below.

## Hyperparameter search (validation split only)

### Deep learning grid

| Hyperparameter | Candidates | **Selected default** |
| --- | --- | --- |
| Batch size | [16, 32, 64] | **32** |
| Learning rate | [0.0001, 0.0005, 0.001] | **0.0005** |
| Optimizer | ['AdamW', 'Adam'] | **AdamW** |
| Weight decay | — | **0.0001** |
| Max epochs | — | **200** |
| Grad clip norm | — | **1.0** |

Selection criterion on validation: **lowest macro demand MAE** (primary); tie-break on val stress MAE for PF-STGT.

### Classical ML grid

| Model | Search space | Selection metric |
| --- | --- | --- |
| Linear Regression | default (OLS / Ridge α∈{0.1,1,10}) | val macro MAE |
| Random Forest | n_estimators∈{100,300}, max_depth∈{None,10,20} | val macro MAE |
| XGBoost | max_depth∈{4,6,8}, lr∈{0.05,0.1}, n_estimators∈{200,500} | val macro MAE |

## Optimizer configuration (frozen default)

```python
optimizer = AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
```

## Early stopping (frozen)

| Parameter | Value |
| --- | --- |
| Monitor | Validation macro demand MAE |
| Patience | 15 epochs |
| Min delta | 0.01 MW |
| Restore best weights | Yes |

PF-STGT: monitor combined validation loss if demand MAE plateaus but stress improves — log both.

## Checkpoint strategy (frozen)

Save on validation improvement:

```
checkpoints/{benchmark_id}/seed_{seed}/best.pt
checkpoints/{benchmark_id}/seed_{seed}/config.yaml
checkpoints/{benchmark_id}/seed_{seed}/metrics_val.json
```

- Retain **best validation** checkpoint only (not last epoch).
- Final test evaluation loads best val checkpoint.
- Store git commit hash, seed, and data MD5 in checkpoint metadata.

## Training data usage

- **Train:** fit model on train windows only (~1287 samples).
- **Validation:** early stopping + hyperparameter selection.
- **Test:** held out until final single evaluation.

## Multi-seed protocol

- Seeds: `[42, 123, 456]` for B04–B07.
- Report test metrics as mean ± std across seeds.
- Primary claim uses best-seed or mean — document choice in results phase.
