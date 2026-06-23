# Reviewer Risk Assessment — Phase 07C

Generated: 2026-06-23

Evidence base: 55 papers (Phase 07A), critical analysis (Phase 07B).
This document anticipates reviewer challenges to novelty and contributions.
It does **not** specify graph topology or model architecture.

## Risk matrix

| Risk ID | Challenge | Likely reviewer concern | Mitigation strategy | Residual risk |
| --- | --- | --- | --- | --- |
| R-01 | Geographic generalisation | "Single-country case; findings may not transfer." | Frame as first rigorous Bangladesh division-level benchmark; compare methods against US/EU graph papers on same metrics internally. | Medium |
| R-02 | Incremental architecture | "Graph + transformer is incremental vs GNN/GT literature." | Emphasise multi-task shedding + OSI formulation and Bangladesh context as differentiators, not backbone alone (8 High-relevance papers are method-centric). | Medium |
| R-03 | Shedding vs control | "Shedding literature is control-oriented; forecasting claim is misaligned." | Explicit task contrast in introduction; cite 15 shedding-formulation opportunities and Phase 02 zero-inflated evidence. | Low |
| R-04 | Sparse target degeneracy | "Model may predict all-zero shedding." | Acknowledge Phase 02 imbalance; commit to event-aware metrics and separate shedding head (Phase 06 recommendation). | Medium |
| R-05 | Explainability cost | "SHAP on graph-temporal models is expensive/misleading." | Cite isolated SHAP paper in corpus; plan node-level vs global attribution and correlation-aware interpretation (Phase 07B weakness flagged). | Medium |
| R-06 | Data collinearity | "Demand≈supply redundancy inflates importance." | Reference Phase 02 collinearity finding; use complementary targets and ablation on engineered features (Phase 05B groups). | Low |
| R-07 | Temporal gaps | "17 missing calendar days break windowing." | Document gap handling from Phase 01/03; use continuous index with explicit gap flags in methodology. | Low |
| R-08 | Metadata-thin related work | "Literature review depth limited by missing abstracts (52/55)." | Deep-read 8 High-relevance + 3 abstract-rich papers; supplement with full-text retrieval before submission. | Medium |
| R-09 | Multi-task negative transfer | "Joint training hurts sparse shedding head." | Cite Phase 07B multi-task weakness theme; plan uncertainty/task-weighting analysis in future evaluation phase. | Medium |
| R-10 | Novelty overclaim | "Explainable STGT is buzzword stacking." | Tie each claim to gap ID and counted evidence (novelty_matrix); avoid architecture details not yet implemented. | Low |

## Severity summary

| Residual risk | Count |
| --- | --- |
| Low | 3 |
| Medium | 6 |
| High | 0 |

## Highest-priority reviewer defenses

1. **Bangladesh gap (GAP-01):** 0/55 papers in corpus use Bangladesh data — regional contribution is evidence-backed.
2. **Task integration (GAP-02/GAP-03):** Joint demand + sparse shedding forecasting is under-represented vs control/optimisation cluster.
3. **Reproducibility (GAP-08):** Project phases 04/06 provide stronger evaluation discipline than metadata-sparse conference comparators.
