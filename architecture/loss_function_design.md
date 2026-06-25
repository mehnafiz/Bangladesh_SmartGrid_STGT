# Loss Function Design — Phase 09

Generated: 2026-06-24

## Multi-task objective

```
L_total = λ1 · L_demand + λ2 · L_stress + λ_reg · L_reg
```

## Task 1 — Regional demand (Huber)

```
L_demand = (1/N) Σ_r Huber_δ(D_hat_r, D_r; δ=1.0 MW)
```

- **Rationale:** Robust to Phase 02 upper-tail demand outliers (record-high days).
- Per-node errors averaged; optional node weights for Dhaka dominance (Phase 02 ~35.7% share).

## Task 2 — Operational stress (MSE)

```
L_stress = MSE(OSI_hat, OSI)
```

- **Rationale:** Continuous [0,1] target (Phase 08.5 SF-04); bounded sigmoid output.
- MSE penalises moderate stress mis-ranking suitable for operational assessment.

## Default task weights (design starting point)

| Weight | Value | Note |
| --- | --- | --- |
| λ1 | 1.0 | Primary forecasting task |
| λ2 | 0.5 | Auxiliary stress; scale OSI MSE to demand magnitude |
| λ_reg | 1e-4 | L2 on head weights (optional) |

Uncertainty-based balancing (Kendall et al.) recommended at implementation — not trained here.

## Metrics (evaluation phase — not trained here)

| Task | Primary metrics |
| --- | --- |
| Demand | MAE, MAPE, RMSE per region and macro-avg |
| Stress | MAE, RMSE, Pearson r on OSI |
