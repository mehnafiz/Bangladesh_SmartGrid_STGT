# Decision Log — Architecture Freeze

**Date:** 2026-06-25  
**Decision:** Adopt **S2** (Correlation-Only PF-STGT) as the final architecture.  
**Supersedes:** S1 (hybrid PF-STGT W20) for all forward experiments and manuscript reporting.

---

## Context

Experiments 03, 03A, and 03B evaluated component contributions, failure modes, and
simplification paths. S2 (Exp03 A6 / Exp03B S2) achieved the best multi-task demand
performance (88.65 MW test MAE, stress R² 0.745) while removing geographical graph noise.

---

## Decision

| Item | Outcome |
| --- | --- |
| Final model | **S2** — `PFSTGT` + `GraphVariant.CORR` + W20 multi-task |
| Original model | **S1** — retained as design reference and Exp02 B07 |
| Checkpoint | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| Next step | Experiment 04 explainability (no retraining) |

---

## Rejected alternatives

- **S4** (corr + no transformer): +21 MW vs S1 — simplifications do not compose
- **A4** (single-task): best demand MAE but no OSI output
- **S1** as production model: superseded by S2 on demand and stress

---

## References

- `experiments/architecture_freeze_revision/Final_Architecture_Decision.md`
- `experiments/architecture_freeze_revision/architecture_transition_summary.md`
- `experiments/architecture_freeze_revision/final_model_specification.md`
