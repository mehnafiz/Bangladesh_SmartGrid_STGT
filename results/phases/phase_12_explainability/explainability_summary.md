# Phase 12 — Explainability Design Framework Summary

- Completion date: 2026-06-24
- Selected toolkit: **Hybrid XAI Stack (SHAP-primary + Attention-native + Permutation-validation)**

## Five attribution levels defined

| Level | Coverage |
| --- | --- |
| L1 Feature Attribution | SHAP + Permutation |
| L2 Node Attribution | SHAP node coalitions + spatial attention |
| L3 Temporal Attribution | Temporal attention over T=7 |
| L4 Graph Attention | Spatial attention + hybrid adjacency overlay |
| L5 Stress Attribution | SHAP + OSI c1/c2/c3 decomposition |

## Deliverables

### explainability/
- xai_strategy.md
- shap_design.md
- attention_analysis_design.md
- node_importance_design.md
- stress_attribution_design.md
- explainability_protocol.md

### results/phases/phase_12_explainability/
- explainability_summary.md
- explainability_decision_report.md
- xai_method_comparison.csv

## Scope compliance

- Explainability framework design only.
- **No model implementation or training.**
- Locked phase outputs not modified.

## Locked input integrity

- `architecture/explainability_design.md` MD5: `8aef5dfac194bc3414b6be7ee18f2688`
- `graphs/adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686`
- `targets/multitask_formulation.md` MD5: `f4fb421b36f6f9eefa8ad6f8bd5f92ef`
- `references/gap_analysis/research_gap_matrix.csv` MD5: `d95ece0b123115f34648331ddbc62f17`

## Status

Ready for PF-STGT implementation with integrated XAI pipeline (next phase).
