# Architecture Components — Phase 09

Generated: 2026-06-24

## 1. Input Layer

### Node feature tensor

- Shape: `(batch, T=7, N=9, F_n=9)`
- F_n=9 per node (leakage-safe, excludes `operational_stress_index`):

  1. `{r}_demand`
  2. `{r}_supply`
  3. `{r}_load`
  4. `demand_lag_1_{r}`
  5. `demand_lag_7_{r}`
  6. `load_lag_1_{r}`
  7. `demand_rolling_mean_7_{r}`
  8. `regional_demand_share_{r}`
  9. `regional_load_intensity_{r}`

### Global context vector

- Shape: `(batch, T, F_g=17)` broadcast to graph readout and stress head
- Includes calendar, grid aggregates, limitations, national generation scalars
- **Excluded:** `operational_stress_index` (target leakage for Task 2 at h=1)

### Input embedding

```
E_node = Linear(F_n → d_model) + RegionalEmbedding(N → d_model)
E_global = Linear(F_g → d_model)
H0 = E_node + broadcast(E_global) + PosEnc_time(T)
```

## 2. Spatial Module (selected: Graph Transformer)

| option            |   expressiveness |   literature_support |   explainability |   hybrid_adjacency_fit |   stgt_alignment |   total_score | selected   | summary                                                                                  |
|:------------------|-----------------:|---------------------:|-----------------:|-----------------------:|-----------------:|--------------:|:-----------|:-----------------------------------------------------------------------------------------|
| GCN               |                3 |                    4 |                2 |                      4 |                2 |            15 | False      | Fixed-weight message passing; strong baseline but no attention maps for GAP-05.          |
| GAT               |                4 |                    4 |                4 |                      5 |                3 |            20 | False      | Edge-weighted attention; good fit for Phase 08 hybrid weights but limited to neighbours. |
| Graph Transformer |                5 |                    5 |                5 |                      5 |                5 |            25 | True       | Full node self-attention with adjacency bias; aligns with STGT title, GAP-04, NOV-04/05. |

**Mechanism:** Multi-head self-attention over N nodes at each timestep, with additive
mask/bias from Phase 08 hybrid adjacency A (zero bias where A_ij=0).

```
Attn_spatial(Q,K,V) = softmax(QK^T / sqrt(d) + B_adj) V
B_adj[i,j] = log(A_ij + ε)  if A_ij > 0 else -inf
```

## 3. Temporal Module (selected: Transformer Encoder)

| option                                |   long_range_modelling |   literature_support |   T7_window_fit |   implementation_clarity |   stgt_alignment |   total_score | selected   | summary                                                                                       |
|:--------------------------------------|-----------------------:|---------------------:|----------------:|-------------------------:|-----------------:|--------------:|:-----------|:----------------------------------------------------------------------------------------------|
| Temporal Attention (single layer)     |                      3 |                    3 |               3 |                        4 |                3 |            16 | False      | Lightweight but shallow for weekly seasonality patterns (Phase 02).                           |
| Transformer Encoder                   |                      5 |                    5 |               5 |                        5 |                5 |            25 | True       | Multi-head self-attention over T=7; matches lag-7 feature design and 7/55 transformer papers. |
| Temporal Transformer (causal variant) |                      4 |                    4 |               4 |                        3 |                4 |            19 | False      | Causal masking unnecessary for h=1 ex-post window encoding; adds complexity without gain.     |

**Mechanism:** Standard transformer encoder applied per node across T timesteps
(shared weights across nodes for parameter efficiency).

## 4. Fusion Strategy (selected: Parallel Fusion)

| option             |   scientific_validity |   literature_precedent |   multi_task_suitability |   interpretability |   phase02_alignment |   total_score | selected   | summary                                                                                        |
|:-------------------|----------------------:|-----------------------:|-------------------------:|-------------------:|--------------------:|--------------:|:-----------|:-----------------------------------------------------------------------------------------------|
| Spatial → Temporal |                     4 |                      5 |                        3 |                  3 |                   3 |            18 | False      | Classic ST-GCN path; may blur temporal trend before cross-region stress propagation.           |
| Temporal → Spatial |                     3 |                      3 |                        3 |                  3 |                   3 |            15 | False      | Delays spatial coupling of same-day regional shocks; weaker for correlated divisions.          |
| Parallel Fusion    |                     5 |                      4 |                        5 |                  4 |                   5 |            23 | True       | Dual pathway for national seasonality (temporal) and inter-node coupling (spatial); ablatable. |

```
H_spatial = GraphTransformer(H0)      # (B, T, N, d)
H_temporal = TransformerEnc(H0)       # (B, T, N, d)
H_fused = Gate ⊙ H_spatial + (1-Gate) ⊙ H_temporal
Gate = σ(Linear([H_spatial; H_temporal]))
H_shared = H_fused[:, -1, :, :]      # last observed day representation
```

## 5. Shared Representation

- **H_shared** ∈ R^(batch × N × d_model), d_model=128
- Last-timestep fused embedding per node
- Graph readout vector: `h_graph = mean_pool(H_shared) ⊕ E_global[:, -1, :]`

## 6. Multi-Task Heads

### Task 1 — Regional Load Forecasting
- `DemandHead`: Linear(d_model → 1) per node → 9 outputs
- Output: `D_hat(t+1) ∈ R^9` (inverse-transform MW at inference if scaled)
- Loss: Huber(δ=1.0) per node, averaged

### Task 2 — Operational Stress Assessment
- `StressHead`: MLP([h_graph; flatten(H_shared)]) → 1
- Output: `sigmoid` → OSI_hat(t+1) ∈ [0,1]
- Loss: MSE
