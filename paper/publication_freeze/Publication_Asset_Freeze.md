# Publication Asset Freeze

## Objective

Freeze all research assets before manuscript preparation.

After this stage, no experimental results, figures, tables, or model configurations should be modified unless a reproducible error is discovered.

---

## Final Architecture

S2 — Correlation-Aware Multi-Task Forecasting Framework

Status:

Frozen

---

## Dataset

Processed Bangladesh Smart Grid Dataset

Status:

Frozen

---

## Data Split

Chronological Train / Validation / Test Split

Status:

Frozen

---

## Training Configuration

Final Configuration

* AdamW Optimizer
* Stress Weight = 20
* Demand Loss Normalization
* Balanced Early Stopping
* Best Configuration from Experiment 01B

Status:

Frozen

---

## Benchmark Results

Source:

Experiment 02

Status:

Frozen

---

## Benchmark Verification

Source:

Experiment 02A

Status:

Frozen

---

## Ablation Results

Source:

Experiment 03

Status:

Frozen

---

## Architecture Validation

Source:

Experiment 03A

Experiment 03B

Status:

Frozen

---

## Explainability Results

Source:

Experiment 04

Status:

Frozen

---

## Tables

Freeze all manuscript tables.

Assign final table numbering.

---

## Figures

Freeze all manuscript figures.

Assign final figure numbering.

---

## Repository Version

Record:

* Git Commit
* Version Tag
* Freeze Date

---

## Deliverables

* frozen_tables_inventory.md
* frozen_figures_inventory.md
* frozen_results_inventory.md

---

## Definition of Done

✔ Final architecture frozen

✔ Dataset frozen

✔ Training configuration frozen

✔ Benchmark results frozen

✔ Ablation results frozen

✔ Explainability results frozen

✔ Tables frozen

✔ Figures frozen

✔ Repository frozen

Ready for manuscript preparation.

---

## Execution Record

**Date:** 2026-06-25  
**Git commit:** `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa`  
**Version tag (designated):** `publication-freeze-2026-06-25`  
**Action:** Documentation-only freeze; no models retrained, no results modified

### Deliverables generated

| File | Purpose |
| --- | --- |
| `freeze_record.md` | Version metadata and verification summary |
| `frozen_tables_inventory.md` | Manuscript table numbering and source paths |
| `frozen_figures_inventory.md` | Manuscript figure numbering and source paths |
| `frozen_results_inventory.md` | Complete frozen results catalogue (Exp01–04) |

### Verification

All domains listed in this document are marked **Frozen** with authoritative file paths
verified present at freeze time. See `freeze_record.md` for checklist.

**Next step:** Manuscript writing only (`manuscript/drafts/`, `manuscript/overleaf/`).

---

## Training configuration note

Frozen W20 protocol uses **Adam** (lr 5×10⁻⁴) per checkpoint configs. The Publication Asset
Freeze spec references AdamW as design intent; executed experiments (01B, 03, 04) used Adam as
recorded in `checkpoints/*/config.yaml`.
