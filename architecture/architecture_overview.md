# STGT Architecture Overview — Phase 09

Generated: 2026-06-24
Status: **DESIGN FROZEN (implementation deferred)**

## Selected architecture

**PF-STGT (Parallel-Fusion Spatio-Temporal Graph Transformer)**

An explainable multi-task spatio-temporal graph transformer for:

1. **Task 1:** 9-node regional demand forecasting \( \hat{D}_r(t+1) \) (MW)
2. **Task 2:** Graph-level operational stress \( \widehat{OSI}(t+1) \in [0,1] \)

## Evidence base

| Source | Contribution to design |
| --- | --- |
| Phase 07B | Graph+transformer cluster (8 High-relevance papers); XAI gap (3/55) |
| Phase 07C | GAP-04 graph-temporal coupling; GAP-05 explainability; GAP-02 multi-task |
| Phase 08 | Hybrid adjacency (9 nodes, 24 edges, correlation-weighted) |
| Phase 08.5 | h=1 horizon; demand + OSI targets; leakage exclusions |

## High-level data flow

```
Input window X[t-T+1:t]  (T=7)  +  Global context G[t]
        │
        ├─ Spatial Branch: Graph Transformer × L_s  (adjacency-biased attention)
        │
        └─ Temporal Branch: Transformer Encoder × L_t  (per-node time series)
                    │
              Parallel Fusion (gated concat + projection)
                    │
              Shared representation H ∈ R^{N×d}  (d=128)
                 ┌────┴────┐
           Demand Head   Stress Head
            R^9 (MW)      R^1 [0,1]
```

## Key hyperparameters (design defaults)

| Parameter | Value | Rationale |
| --- | --- | --- |
| Input window T | 7 | Phase 05B lag-7 / rolling-7; Phase 06 warm-up |
| Nodes N | 9 | Phase 08 graph |
| Forecast horizon h | 1 | Phase 08.5 frozen |
| d_model | 128 | Balance capacity vs 1,295 train rows |
| Attention heads | 4 | Standard multi-head for spatial/temporal maps |
| Spatial layers L_s | 2 | Depth without over-parameterisation |
| Temporal layers L_t | 2 | Capture weekly seasonality (Phase 02) |

---

## Architecture freeze addendum (2026-06-25)

Following Experiments 03, 03A, and 03B, the repository adopts **S2** as the **final
architecture** for Experiment 04 and manuscript work.

| Label | Name | Graph | Status |
| --- | --- | --- | --- |
| **S1** | PF-STGT (W20) | Hybrid (24 edges) | **Original** Phase 09 design; Exp02 B07 / Exp03 A1 |
| **S2** | Correlation-Aware Multi-Task Framework | Correlation-only (33 edges, τ=0.65) | **Final** frozen model; Exp03 A6 |

S2 uses the same `PFSTGT` module stack as S1; only the adjacency variant changes at the
data layer (`GraphVariant.CORR`). Geographical edges are removed; graph transformer,
temporal transformer, fusion, and dual heads are **retained**.

See:

- `experiments/architecture_freeze_revision/Final_Architecture_Decision.md`
- `experiments/architecture_freeze_revision/final_model_specification.md`
