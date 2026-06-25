# Loss Function Design — Phase 10 (Frozen)

Generated: 2026-06-24
Status: **FROZEN** (extends Phase 09 design with benchmark-specific rules)

## PF-STGT multi-task loss (B07)

```
L_total = λ1 · L_demand + λ2 · L_stress + λ_reg · L_reg
λ1 = 1.0   (frozen)
λ2 = 0.5    (frozen)
λ_reg = 0.0001 (frozen)
```

### Task 1 — Demand (Huber)

```
L_demand = (1/N) Σ_r Huber_δ(D_hat_r, D_r; δ=1.0 MW)
```

- Robust to Phase 02 upper-tail demand outliers.
- Macro-averaged over N=9 regions.

### Task 2 — Stress (MSE)

```
L_stress = MSE(OSI_hat, OSI)     where OSI_hat = sigmoid(head_output)
```

- Target: OSI(t+1) ∈ [0,1] per Phase 08.5 SF-04.

### Regularisation

```
L_reg = weight_decay · ||θ_heads||_2   (via AdamW decoupled weight decay)
```

## Single-task deep baselines (B04–B06)

```
L = (1/N) Σ_r Huber_δ(D_hat_r, D_r; δ=1.0)
```

Same Huber formulation as PF-STGT Task 1 for fair loss comparison.

## Classical ML baselines (B01–B03)

| Model | Training objective | Notes |
| --- | --- | --- |
| Linear Regression | Squared error (OLS) or Ridge penalty | Matches Huber at δ→∞ for Gaussian errors |
| Random Forest | MSE impurity | Non-differentiable ensemble |
| XGBoost | Squared error (reg:squarederror) | eval_metric=rmse on validation |

## Combined loss strategy (PF-STGT only)

1. **Fixed weights** λ1=1.0, λ2=0.5 for primary experiments (frozen).
2. **Ablation (future):** λ2 ∈ {0.25, 0.5, 1.0} on validation only.
3. **Optional extension:** Kendall uncertainty weighting — not primary protocol.

## Loss-to-metric alignment

| Task | Training loss | Primary eval metric |
| --- | --- | --- |
| Demand | Huber | MAE (test) |
| Stress | MSE | RMSE, R² (test) |

MAPE reported at evaluation only (not optimised — Phase 02 MAPE sensitivity to scale).
