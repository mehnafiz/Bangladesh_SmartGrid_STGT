# XAI Strategy — Phase 12

Generated: 2026-06-24
Status: **FROZEN**

## Objective (GAP-05 / NOV-05)

Provide operator-facing, scientifically defensible explanations for:

1. **Task 1:** 9-node regional demand forecasts \( \hat{D}_r(t+1) \)
2. **Task 2:** National operational stress \( \widehat{OSI}(t+1) \)

Only **3/55** papers in Phase 07B corpus report integrated XAI for graph-temporal load models.

## Selected toolkit

**Hybrid XAI Stack (SHAP-primary + Attention-native + Permutation-validation)**

| Layer | Method | Purpose |
| --- | --- | --- |
| Primary A | **SHAP** (GradientSHAP + grouped coalitions) | Feature & stress attribution |
| Primary B | **Attention export** (Graph Transformer + Temporal Encoder) | Node, temporal, graph influence |
| Validation | **Permutation importance** (validation split) | Global feature ranking sanity check |

## Method evaluation summary

| method                      |   interpretability |   computational_cost |   literature_support |   pf_stgt_suitability |   multi_task_coverage |   total_score | role                                                                       | selected   |
|:----------------------------|-------------------:|---------------------:|---------------------:|----------------------:|----------------------:|--------------:|:---------------------------------------------------------------------------|:-----------|
| SHAP                        |                  5 |                    2 |                    5 |                     5 |                     5 |            22 | Primary — feature & stress attribution                                     | True       |
| Attention Visualization     |                  4 |                    5 |                    4 |                     5 |                     3 |            21 | Primary — node, temporal, graph analysis                                   | True       |
| Permutation Importance      |                  4 |                    3 |                    4 |                     3 |                     4 |            18 | Validation — global sanity check                                           | True       |
| SHAP only (standalone)      |                  5 |                    2 |                    5 |                     3 |                     4 |            19 | Rejected as sole toolkit — misses native graph/temporal structure          | False      |
| Attention only (standalone) |                  3 |                    5 |                    3 |                     3 |                     2 |            16 | Rejected as sole toolkit — not faithful attributions (Jain & Wallace 2019) | False      |

**Decision:** No single method covers all five attribution levels. Hybrid stack maximises 
interpretability while keeping computational cost feasible for N=9, T=7.

## Five-level explainability framework

| Level | Name | Primary method | Deliverable |
| --- | --- | --- | --- |
| L1 | Feature Attribution | SHAP + Permutation | `shap_design.md` |
| L2 | Node Attribution | SHAP coalitions + spatial attention | `node_importance_design.md` |
| L3 | Temporal Attribution | Temporal attention + SHAP time groups | `attention_analysis_design.md` |
| L4 | Graph Attention Analysis | Spatial attention + hybrid adjacency overlay | `attention_analysis_design.md` |
| L5 | Stress Attribution | SHAP on stress head + OSI component decomposition | `stress_attribution_design.md` |

## Scope boundaries

- Explanations computed **post-training** on validation/test case studies.
- **Excluded input:** same-day OSI when explaining OSI(t+1) (Phase 08.5 leakage rule).
- No model implementation in this phase.
