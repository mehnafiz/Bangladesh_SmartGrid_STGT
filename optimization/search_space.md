# Hyperparameter Search Space — Phase 11

Generated: 2026-06-24
Status: **FROZEN**
Target model: **PF-STGT (B07)**

## Fixed parameters (not searched)

| Parameter | Value | Source |
| --- | --- | --- |
| `lookback_window_T` | 7 | Phase 09/10 |
| `forecast_horizon_H` | 1 | Phase 09/10 |
| `num_nodes` | 9 | Phase 09/10 |
| `num_tasks` | 2 | Phase 09/10 |
| `graph_strategy` | Hybrid (Phase 08 adjacency) | Phase 09/10 |
| `optimizer` | AdamW | Phase 09/10 |
| `scheduler` | ReduceLROnPlateau(factor=0.5, patience=5) | Phase 09/10 |
| `early_stopping_patience` | 15 | Phase 09/10 |
| `max_epochs` | 200 | Phase 09/10 |
| `grad_clip_norm` | 1.0 | Phase 09/10 |
| `lambda_demand` | 1.0 | Phase 09/10 |
| `lambda_stress` | 0.5 | Phase 09/10 |
| `huber_delta_mw` | 1.0 | Phase 09/10 |
| `primary_seed_hpo` | 42 | Phase 09/10 |

## Searchable parameters (9 dimensions)

| module      | parameter              | symbol   | candidates       |   default_phase09 | justification                                            |
|:------------|:-----------------------|:---------|:-----------------|------------------:|:---------------------------------------------------------|
| graph       | num_graph_layers       | L_s      | 1, 2, 3          |            2      | 9-node graph; depth 1–3 avoids over-smoothing on small N |
| graph       | graph_hidden_dim       | d_model  | 64, 128, 192     |          128      | ~1,287 train windows; cap capacity vs overfit            |
| graph       | graph_dropout          | p_g      | 0.1, 0.2, 0.3    |            0.1    | Regularise graph attention on 24-edge hybrid graph       |
| transformer | num_transformer_layers | L_t      | 1, 2, 3          |            2      | T=7 window; 1–3 layers cover weekly pattern depth        |
| transformer | num_attention_heads    | H        | 2, 4, 8          |            4      | Must divide d_model; constrained sampling in HPO         |
| transformer | transformer_dropout    | p_t      | 0.1, 0.2, 0.3    |            0.1    | Match graph dropout band for balanced regularisation     |
| training    | learning_rate          | lr       | 1e-4, 5e-4, 1e-3 |            0.0005 | Phase 10 grid; stable for AdamW on small batches         |
| training    | weight_decay           | wd       | 1e-5, 1e-4, 1e-3 |            0.0001 | AdamW decoupled L2; log-spaced regularisation band       |
| training    | batch_size             | B        | 16, 32, 64       |           32      | ~40 steps/epoch at B=32; memory-safe for 9×7×9 tensor    |

## Sampling constraints

1. **`num_attention_heads` must divide `graph_hidden_dim`** — invalid combos rejected and resampled.
2. **`graph_hidden_dim` ∈ {64, 128, 192}** — paired with compatible head counts only.
3. **Dropout** sampled independently from {0.1, 0.2, 0.3} for graph and transformer modules.
4. **Loss weights λ1, λ2** fixed at 1.0 / 0.5 (Phase 10); not searched to limit val overfitting.

## Effective search space size

- Raw Cartesian: 3⁹ = 19,683 combinations (infeasible).
- **Protocol:** 20 random valid trials + top-3 finalist confirmation.

## Baseline models (B01–B06)

Use **fixed small grids** from Phase 10 `training_strategy.md`; no joint HPO with PF-STGT. 
PF-STGT tuned config compared against Phase 10 default baselines on identical splits.
