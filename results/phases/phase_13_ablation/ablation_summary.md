# Phase 13 — Ablation Studies Design Summary

- Completion date: 2026-06-24
- Reference model: **A1 PF-STGT Full**
- Core ablation variants: **8**
- Total planned training runs: **9** (no runs executed in this phase)

## Study categories

| Category | Variants |
| --- | --- |
| Component removal | A2, A3 |
| Hybrid graph | A5, A5-GEO, A5-CORR |
| Multi-task | A4 vs A1 |
| Explainability | A6 (trained), A6-XAI (analysis) |

## Evaluation metrics (frozen)

Demand: MAE, RMSE, MAPE, R² (macro + Dhaka). Stress: MAE, RMSE, R².

## Deliverables

### ablation/
- ablation_plan.md
- ablation_matrix.csv
- component_contribution_framework.md
- statistical_significance_plan.md

### results/phases/phase_13_ablation/
- ablation_summary.md
- ablation_decision_report.md

## Scope compliance

- Ablation framework design only.
- **No model implementation or training.**
- **No experimental results generated.**
- Locked phase outputs not modified.

## Locked input integrity

- `graphs/adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686`
- `architecture/architecture_overview.md` MD5: `afe5a7abb287604b849e793d9067ab40`
- `experiments/evaluation_protocol.md` MD5: `829faaed417189e0e154cb8b91ed97ff`
- `explainability/xai_strategy.md` MD5: `8f4440d99976c95fefb832d9e079e756`

## Status

Ready for ablation implementation and training (next phase).
