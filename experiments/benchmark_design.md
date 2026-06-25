# Benchmark Design — Phase 10

Generated: 2026-06-24
Status: **FROZEN**

## Purpose

Define a fair, literature-aligned benchmark suite for evaluating PF-STGT against classical, temporal, and spatio-temporal baselines on the Bangladesh smart-grid dataset.

## Frozen benchmark models (7)

| benchmark_id   | model_name        | family                   | uses_graph   | tasks_supported   |   input_window_T |   horizon_h | adjacency                   | multi_task   |
|:---------------|:------------------|:-------------------------|:-------------|:------------------|-----------------:|------------:|:----------------------------|:-------------|
| B01            | Linear Regression | Classical ML             | False        | demand            |                7 |           1 | N/A                         | False        |
| B02            | Random Forest     | Classical ML             | False        | demand            |                7 |           1 | N/A                         | False        |
| B03            | XGBoost           | Classical ML             | False        | demand            |                7 |           1 | N/A                         | False        |
| B04            | LSTM              | Deep Learning (temporal) | False        | demand            |                7 |           1 | N/A                         | False        |
| B05            | GRU               | Deep Learning (temporal) | False        | demand            |                7 |           1 | N/A                         | False        |
| B06            | T-GCN             | Spatio-Temporal GNN      | True         | demand            |                7 |           1 | graphs/adjacency_matrix.csv | False        |
| B07            | PF-STGT           | Proposed                 | True         | demand;stress     |                7 |           1 | graphs/adjacency_matrix.csv | True         |

## Fair comparison protocol

| Constraint | Specification |
| --- | --- |
| Input window | T=7 observed days (Phase 09) |
| Forecast horizon | h=1 day (Phase 08.5) |
| Warm-up exclusion | Skip first 7 timesteps per split (Phase 06) |
| Graph adjacency | Phase 08 hybrid matrix (B06, B07 only) |
| Feature source | `data/features/*_features.parquet` (Phase 05B/06) |
| Leakage policy | No same-day OSI as input for stress target (Phase 08.5) |

## Model-specific design notes

### B01–B03 Classical ML (demand-only)
- **Input:** Flatten `(T, F_node)` per region → 9 independent regressors OR multi-output linear.
- **Target:** \(D_r(t+1)\) per region.
- **Rationale:** Phase 07B hybrid/ensemble papers; low-complexity lower bound (GAP-08 reproducibility).

### B04 LSTM / B05 GRU (demand-only)
- **Input:** `(T, F_node)` sequence per node; shared weights across nodes.
- **Output:** 9 demand values at t+1.
- **Rationale:** 7/55 transformer/temporal papers; standard DL baseline without graph (GAP-04 contrast).

### B06 T-GCN (demand-only, graph baseline)
- **Input:** `(T, N, F_node)` + hybrid adjacency A.
- **Architecture:** 2-layer temporal graph convolution (ST-first: GCN → GRU), aligned with ST-GCN literature.
- **Rationale:** Phase 07B GNN cluster (5/55 graph papers); isolates graph value vs PF-STGT transformer fusion.

### B07 PF-STGT (proposed, multi-task)
- **Architecture:** Phase 09 PF-STGT design (Graph Transformer ∥ Transformer Encoder → dual heads).
- **Tasks:** Demand (9 nodes) + OSI (graph-level).
- **Rationale:** Full proposed framework; only benchmark with Task 2 stress output.

## Task coverage matrix

| Model | Demand forecast | Stress forecast |
| --- | --- | --- |
| B01–B06 | Yes | No (demand-only baselines) |
| B07 PF-STGT | Yes | Yes |

Stress metrics (Phase 10) are primary for PF-STGT; non-learned persistence/median OSI baselines reported in `evaluation_protocol.md` for context only (not benchmark models).

## Data splits (Phase 04 — frozen)

| Split | Rows | Date range |
| --- | --- | --- |
| Train | 1295 | 2019-11-21 → 2023-06-15 |
| Validation | 277 | 2023-06-16 → 2024-03-19 |
| Test | 278 | 2024-03-20 → 2024-12-30 |

Approximate train windows after warm-up: ~1287.
