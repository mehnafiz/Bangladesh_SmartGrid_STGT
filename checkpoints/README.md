# checkpoints/

**Purpose**
Intermediate training checkpoints enabling resumable training and recovery.
Large binary files are git-ignored.

---

## Canonical frozen model (S2)

| Property | Path |
| --- | --- |
| Final architecture | S2 — Correlation-Only PF-STGT |
| Checkpoint | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| Spec | `experiments/architecture_freeze_revision/final_model_specification.md` |

## Original architecture (S1)

| Property | Path |
| --- | --- |
| Historical reference | S1 — PF-STGT W20 (Exp02 B07) |
| Checkpoint | `experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt` |

Experiment 04 explainability loads **S2** only. No retraining required.
