# src/models/

**Purpose**
Model architectures, including the spatio-temporal graph transformer and
baselines.

**Implementation:** `pf_stgt.py` — `PFSTGT` class (749,058 parameters).

---

## Architecture freeze (2026-06-25)

| ID | Graph | Status |
| --- | --- | --- |
| S1 | `GraphVariant.HYBRID` | Original design |
| **S2** | `GraphVariant.CORR` | **Final frozen model** |

Same `PFSTGT` forward path for both; graph variant is selected via
`FoundationCoordinator(graph_variant=...)`.

Checkpoint: `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt`
