# Ablation Plan — Phase 13

Generated: 2026-06-24
Status: **FROZEN**

## Objective

Isolate and quantify contributions of graph module, transformer module, multi-task learning,
hybrid graph topology, and explainability-enabled architecture for PF-STGT.

## Reference model

**A1 — PF-STGT Full Model** (Phase 09 architecture, Phase 08 hybrid graph, Phase 08.5 dual-task).

## Study categories

### 1. Component removal studies (A2–A3)

| ID | Variant | Isolates |
| --- | --- | --- |
| A2 | Without Graph Module | Spatial / graph contribution |
| A3 | Without Transformer Module | Temporal contribution |

### 2. Hybrid graph studies (A5 family)

| ID | Adjacency | Edges | Density |
| --- | --- | --- | --- |
| A5 / A1 | Hybrid | 24 | 66.7% |
| A5-GEO | Geographical only | 21 | 58.3% |
| A5-CORR | Correlation τ=0.65 | 33 | 91.7% |

### 3. Multi-task studies (A4)

| ID | Variant | Training |
| --- | --- | --- |
| A4 | Demand-only | λ2=0, stress head removed |
| A1 | Full multi-task | λ1=1.0, λ2=0.5 (Phase 10) |

### 4. Explainability studies (A6)

| ID | Variant | Type |
| --- | --- | --- |
| A6 | BiLSTM black-box trunk | Trained ablation (no attention maps) |
| A6-XAI / A1 | Phase 12 XAI stack | Post-hoc analysis on full model |

## Required ablations (Phase 13 spec)

| ablation_id   | variant_name                             | structural_change                                                | hypothesis                                                          |
|:--------------|:-----------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------------|
| A1            | PF-STGT Full Model                       | None — reference model                                           | Best overall demand + stress performance                            |
| A2            | Without Graph Module                     | Remove Graph Transformer; disable spatial branch                 | Spatial graph coupling improves demand MAE vs temporal-only         |
| A3            | Without Transformer Module               | Remove Transformer Encoder; mean-pool T dim before graph block   | Temporal encoding improves demand MAE vs spatial-only snapshot      |
| A4            | Without Multi-Task Learning              | Remove stress head; λ2=0; train demand-only                      | Joint training improves demand and enables stress forecasting       |
| A5-GEO        | Without Hybrid Graph — Geographical Only | Replace A with row-normalised geographic adjacency               | Hybrid correlation weighting adds value over borders-only           |
| A6            | Without Explainability Pathways          | Replace GT+TE with param-matched BiLSTM trunk; no attention maps | Attention-based trunk trades ≤ε performance for native XAI (GAP-05) |

## Training protocol (all variants)

| Rule | Specification |
| --- | --- |
| Hyperparameters | Phase 11 best config (or trial-0 baseline if HPO not yet run) |
| Loss | Phase 10 frozen (Huber + MSE for multi-task) |
| Split | Phase 04 chronological 70/15/15 |
| Early stopping | Val macro demand MAE, patience 15 |
| A1 seeds | 42, 123, 456 |
| Ablation seeds | 42 (single seed for fair budget) |

## Execution order

1. Train A1 (full) → confirm test metrics.
2. Train A2–A4, A5-GEO, A6 (parallelizable).
3. Optional A5-CORR supplementary.
4. Run Phase 12 XAI on A1 (A6-XAI analysis track).
5. Statistical tests vs A1 on test split.

## Total training runs (budget)

| Category | Runs |
| --- | --- |
| A1 full (3 seeds) | 3 |
| Core ablations (5 × 1 seed) | 5 |
| Supplementary A5-CORR | 1 |
| **Total** | **9** |

Est. **~12–18 GPU-hours** (Phase 11 scale × 9 runs).

---

## Post-freeze note (2026-06-25)

Experiment 03 executed ablations A1–A6. **A6 (correlation graph only) is adopted as the
final architecture S2** for Experiment 04 and manuscript work. A1 remains the ablation
reference for historical ΔMAE reporting; results are **not modified**.

See `experiments/architecture_freeze_revision/Final_Architecture_Decision.md`.
