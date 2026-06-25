# Publication Freeze Record

**Freeze date:** 2026-06-25 (UTC)  
**Status:** **FROZEN** — manuscript development may proceed; no experimental regeneration

---

## Repository version

| Field | Value |
| --- | --- |
| **Git commit (HEAD at freeze)** | `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa` |
| **Commit message** | `update` |
| **Designated version tag** | `publication-freeze-2026-06-25` |
| **Tag status** | Pending — apply after committing frozen experiment assets |

> Experiment outputs (01–04) exist in the working tree at freeze time. Tag the repository
> once all paths listed in the inventories are committed to preserve reproducibility.

---

## Frozen domains

| Domain | Authority document / source | Status |
| --- | --- | --- |
| Final architecture (S2) | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` | Frozen |
| Dataset & splits | `src/constants.py` LOCKED_MD5 + Phase 04 splits | Frozen |
| Training configuration (W20) | Exp01B + S2 checkpoint config | Frozen |
| Benchmark results | Exp02 | Frozen |
| Benchmark verification | Exp02A | Frozen |
| Ablation results | Exp03 | Frozen |
| Architecture validation | Exp03A, Exp03B | Frozen |
| Explainability results | Exp04 | Frozen |

---

## Verification summary

| Check | Result |
| --- | --- |
| S2 checkpoint present | Yes — `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| Benchmark CSV present | Yes — `experiments/experiment_02_benchmark_models/benchmark_results.csv` |
| Ablation CSV present | Yes — `experiments/experiment_03_ablation_studies/ablation_results.csv` |
| XAI reports (8) present | Yes — `experiments/experiment_04_explainability_analysis/*.md` |
| Manuscript figures (7) present | Yes — `manuscript/overleaf/figures/figure_*.png` |
| Locked dataset MD5 documented | Yes — `src/constants.py` |
| All experiments 01–04 complete | Yes |

**Ready for manuscript preparation.**

---

## Change policy (post-freeze)

Do **not** retrain models, regenerate experiment CSVs/figures, or alter locked data artefacts.
Permitted changes: manuscript prose, LaTeX layout, citation formatting, and non-result documentation.

If a reproducible error is discovered, open a new experiment revision (e.g. Exp0X-fix) rather
than silently editing frozen assets.
