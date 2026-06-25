# Phase 14 — Error Analysis Framework Summary

- Completion date: 2026-06-24
- Primary model: **B07 PF-STGT (A1 seed 42)**
- Error categories: **6** (E1–E6)
- Test analysis window: **278 days** (no analysis executed in this phase)

## Framework components

| Component | Category | Deliverable |
| --- | --- | --- |
| Overall error | E1 | error_taxonomy.md |
| Regional error | E2 | regional_error_framework.md |
| Stress error | E3 | stress_error_framework.md |
| Extreme events | E4 | extreme_event_framework.md |
| Temporal error | E5 | error_taxonomy.md (§E5) |
| Graph error | E6 | error_taxonomy.md (§E6) + regional framework |
| Root-cause analysis | RC | root_cause_analysis_protocol.md |

## Root-cause pathways (Phase 12 integration)

1. **Feature attribution** — SHAP + Permutation (L1)
2. **Attention review** — spatial + temporal (L3–L4)
3. **Stress attribution** — OSI component decomposition (L5)

Triangulation: ≥2/3 pathway agreement → assign RC label.

## Deliverables

### error_analysis/
- error_taxonomy.md
- error_taxonomy_index.csv
- regional_error_framework.md
- stress_error_framework.md
- extreme_event_framework.md
- root_cause_analysis_protocol.md

### results/phases/phase_14_error_analysis/
- error_analysis_summary.md
- error_analysis_decision_report.md

## Scope compliance

- Error analysis framework design only.
- **No model implementation or training.**
- **No experimental results or residual files generated.**
- Locked phase outputs not modified.

## Locked input integrity

- `data/features/train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16`
- `data/interim/bangladesh_smartgrid_clean.parquet` MD5: `4255024d735a91a4b53b2edee203d0ca`
- `graphs/adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686`
- `explainability/xai_strategy.md` MD5: `8f4440d99976c95fefb832d9e079e756`
- `ablation/ablation_plan.md` MD5: `826896a1f2f0267b445e9a0c55678e9a`

## Status

Ready for post-training error analysis execution (after model training phase).
