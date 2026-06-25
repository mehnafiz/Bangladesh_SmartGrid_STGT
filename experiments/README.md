# experiments/

**Purpose**
Self-contained experiment definitions and run artifacts. Keeps each line of
investigation reproducible and isolated from core source code.

---

## Architecture status (frozen 2026-06-25)

| ID | Role | Mapping | Checkpoint |
| --- | --- | --- | --- |
| **S1** | Original architecture | Exp02 B07, Exp03 A1 | `experiment_01B_.../W20/B07/seed_42/best.pt` |
| **S2** | **Final architecture** | Exp03 A6, Exp03B S2 | `experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |

Decision record: `architecture_freeze_revision/Final_Architecture_Decision.md`

---

## Completed experiments

| Experiment | Folder | Summary |
| --- | --- | --- |
| 01 | `experiment_01_pf_stgt/` | Initial PF-STGT training |
| 01A | `experiment_01A_osi_failure_investigation/` | OSI head failure diagnosis |
| 01B | `experiment_01B_multitask_optimization_repair/` | W20 multi-task repair → **S1** checkpoint |
| 02 | `experiment_02_benchmark_models/` | B01–B07 benchmarks (frozen) |
| 02A | `experiment_02A_classical_benchmark_verification/` | MAE vs R² verification |
| 03 | `experiment_03_ablation_studies/` | A1–A6 ablations |
| 03A | `experiment_03A_ablation_failure_investigation/` | Ablation outcome investigation |
| 03B | `experiment_03B_architecture_simplification/` | S1–S4 simplification → **S2** selected |
| Freeze | `architecture_freeze_revision/` | S2 adoption, final spec |
| 04 | `experiment_04_explainability_analysis/` | SHAP, attention, case studies on S2 |

---

## Next experiment

All planned experiments through **04** are complete. Manuscript integration may proceed using
S2 metrics (Exp03/03B) and Exp04 explainability artefacts.

**Publication asset freeze (2026-06-25):** see `paper/publication_freeze/`.

---

## Legacy folders

- `baseline/` — baseline model experiments
- `graph_transformer/` — spatio-temporal graph transformer experiments
- `hyperparameter/` — tuning and search experiments
- `ablation/` — phase-13 ablation plan (see repo root `ablation/`)
