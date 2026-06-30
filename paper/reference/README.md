# Reference Repository

**Purpose:** Single source of truth for Stage 06 manuscript writing.  
**Revised:** 2026-06-30 (final reference revision)  
**Constraint:** Validated frozen information only — no invented results, no manuscript prose.

---

## Contents

| File | Purpose |
| --- | --- |
| [`MASTER_REFERENCE.md`](MASTER_REFERENCE.md) | Project snapshot, status, writing order, frozen numbers |
| [`Terminology_Guide.md`](Terminology_Guide.md) | Canonical names, aliases, and forbidden variants |
| [`Notation_Guide.md`](Notation_Guide.md) | Symbols, dimensions, metrics, statistical notation |
| [`Writing_Style_Guide.md`](Writing_Style_Guide.md) | Prose tone, wording, references, evidence discipline |
| [`Figure_Index.md`](Figure_Index.md) | All main-text figures with paths and claims |
| [`Table_Index.md`](Table_Index.md) | All main-text tables with paths and claims |
| [`Experiment_Index.md`](Experiment_Index.md) | Experiments → sections, subsections, assets |
| [`Contribution_Map.md`](Contribution_Map.md) | C1–C5 → evidence mapping |
| [`Claim_Guide.md`](Claim_Guide.md) | Defensible vs qualified vs forbidden claims |
| [`Citation_Map.md`](Citation_Map.md) | Section → literature domain mapping (citation needs) |
| [`Reviewer_Risk_Register.md`](Reviewer_Risk_Register.md) | Anticipated reviewer challenges and responses |

---

## Authority hierarchy

When sources conflict during manuscript writing:

1. **`MASTER_REFERENCE.md`** — authoritative consolidated snapshot for authors
2. Frozen experiment CSV/JSON/checkpoints (`experiments/`)
3. `paper/final_results_package/publication_tables.md` + `statistical_summary.md`
4. `paper/consistency_audit/` (claim guardrails)
5. `paper/paper_outline/Paper_Outline.md` (structure)
6. `paper/publication_freeze/` (inventory metadata)

**Figure/table numbering:** Final Results Package + Paper Outline (not early freeze inventory).  
**Manuscript files:** `paper/sections/NN_*.md` where `NN` equals journal section number (e.g. `06_Methodology.md` = Section 6).

---

## Writing Rules

Repository-wide rules for all manuscript work:

- **Never manually invent metrics.** Copy numerical values from `MASTER_REFERENCE.md` or `publication_tables.md`.
- **Always follow `Terminology_Guide.md`** for model names (S2 vs B07 vs A6), tasks, and regions.
- **Check `Claim_Guide.md`** before writing Abstract, Results, Discussion, and Conclusion.
- **Consult `Writing_Style_Guide.md`** for tone, preferred wording, and figure/table citation format.
- **Every scientific claim must be supported** by frozen project evidence (experiments, tables, figures, audit).
- **Never invent citations.** Add references only via `Citation_Map.md` into `manuscript/overleaf/bibliography/`.
- **Never rename frozen figures or tables.** Use IDs 1–9 and 1–7 per `Figure_Index.md` / `Table_Index.md`.
- **Never modify frozen experimental results**, checkpoints, CSVs, or JSON under `experiments/`.
- **Do not regenerate or edit** publication figures/tables in `paper/final_results_package/`.
- **Read the target section file** before writing; preserve continuity with existing prose.
- **Modify only the section file** named in the task; never create duplicate section files.
- **If information conflicts, `MASTER_REFERENCE.md` is authoritative** for manuscript authors.

---

## Related project paths

| Asset | Path |
| --- | --- |
| Manuscript sections | `paper/sections/` (`01_Title.md` … `11_References.md`) |
| Manuscript workspace init | `paper/manuscript_workspace_init.md` |
| Consistency audit | `paper/consistency_audit/` |
| Publication figures | `paper/final_results_package/figures/` |
| Overleaf bibliography | `manuscript/overleaf/bibliography/` |
| Architecture decision | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
| Model specification | `experiments/architecture_freeze_revision/final_model_specification.md` |

---

## Usage rules

1. Cross-check every numeric claim against `MASTER_REFERENCE.md`.
2. Apply `Claim_Guide.md` before drafting Abstract, Results, and Conclusion.
3. Use `Terminology_Guide.md` and `Notation_Guide.md` consistently.
4. Do not modify experiment outputs, figures, or tables.
5. Follow the **Official Manuscript Writing Order** in `MASTER_REFERENCE.md`.

---

## Freeze metadata

| Field | Value |
| --- | --- |
| Freeze date | 2026-06-25 |
| Git commit | `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa` |
| Tag | `publication-freeze-2026-06-25` |
| Final model | **S2** (A6, seed 42) |
