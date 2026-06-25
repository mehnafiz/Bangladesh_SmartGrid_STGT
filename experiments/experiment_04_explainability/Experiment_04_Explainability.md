# Experiment 04 — Explainability Analysis

## Status

**Prepared** — scaffold only (Architecture Freeze Revision, 2026-06-25).  
No execution yet.

---

## Objective

Run Phase 12 / Sprint 04 explainability pipelines on the **frozen final model (S2)**:
feature, node, temporal, graph, and stress attribution — without retraining.

---

## Reference model (frozen)

| Property | Value |
| --- | --- |
| Architecture | **S2** — Correlation-Only PF-STGT |
| Checkpoint | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| Graph | `GraphVariant.CORR` |
| Coordinator | `FoundationCoordinator(verify_md5=True, graph_variant=GraphVariant.CORR)` |

See `experiments/architecture_freeze_revision/final_model_specification.md`.

---

## Scope

| In scope | Out of scope |
| --- | --- |
| SHAP / attention / permutation on S2 | Retraining S2 or any benchmark |
| Case-study selection (Phase 12 protocol) | Modifying Exp02/03 results |
| XAI quality gates (Phase 12) | Dataset or split changes |
| Manuscript figure exports | Ablation re-runs |

---

## Protocol references

- `explainability/explainability_protocol.md`
- `docs/sprints/Sprint_04_Explainability_System.md`
- `docs/phases/Phase_12_Explainability_Design_Framework.md`

---

## Expected deliverables (TBD at execution)

- Attention maps (spatial + temporal) for stratified case studies
- SHAP summaries (demand per region, stress global)
- Permutation importance validation
- Cross-method agreement metrics
- `results/explainability/` artefact tree per evaluation protocol

---

## Prerequisites (complete)

- [x] Experiment 03 ablations (A1–A6)
- [x] Experiment 03A investigation
- [x] Experiment 03B simplification — **S2 selected**
- [x] Architecture Freeze Revision — documentation updated
- [x] Sprint 04 explainability modules (`src/explainability/`)

---

## Execution Record

_Pending Experiment 04 run._
