# Benchmark Rationale — Phase 10

Generated: 2026-06-24

## Literature and gap evidence

| Benchmark | Evidence |
| --- | --- |
| Linear Regression | Lower bound; Phase 07B hybrid papers use statistical baselines |
| Random Forest / XGBoost | Phase 07B ensemble/hybrid cluster; strong tabular baselines on engineered features (GAP-07) |
| LSTM / GRU | 7/55 temporal DL papers; isolates recurrence without graph (GAP-04 ablation) |
| T-GCN | 5/55 graph papers; standard ST-GNN baseline with Phase 08 adjacency |
| PF-STGT | Proposed; addresses GAP-04/05/06 multi-task graph-transformer gap |

## Progressive complexity ladder

```
Linear → RF/XGB → LSTM/GRU → T-GCN → PF-STGT
  (none)   (none)    (temporal)  (+graph)  (+transformer+multi-task+XAI)
```

Each step adds capacity justified by Phase 07C gaps; PF-STGT must demonstrate 
incremental value over T-GCN on demand **and** provide stress predictions T-GCN cannot.

## Why demand-only baselines for B01–B06

- Phase 08.5 defines dual-task formulation for PF-STGT only.
- Literature baselines (Phase 07B) rarely report joint stress forecasting.
- Fair comparison: same input features and horizon for Task 1 across all models.
