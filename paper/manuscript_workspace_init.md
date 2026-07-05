# Manuscript Workspace Initialization

**Stage:** 06 workspace prep (post–consistency audit)  
**Executed:** 2026-06-30  
**Action:** Documentation and section scaffolds only — no manuscript prose, no figure/table/experiment changes

---

## Inputs verified

| Source | Path | Status |
| --- | --- | --- |
| Paper outline | `paper/paper_outline/Paper_Outline.md` | ✅ Read |
| Publication freeze | `paper/publication_freeze/` | ✅ Read |
| Final results package | `paper/final_results_package/` | ✅ Read |
| Consistency audit | `paper/consistency_audit/` | ✅ Read |
| Architecture decision | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` | ✅ Read |
| Completed experiments | Exp01–04 (+01A, 01B, 02A, 03A, 03B) | ✅ Frozen |

---

## Task 1 — Section files

Created **12** manuscript section files in `paper/sections/` (outline-aligned; §11 = Appendix A, §12 = BibTeX references).

| # | File | Outline § | Status |
| ---: | --- | ---: | --- |
| 1 | `01_Title.md` | 1 | ✅ Created |
| 2 | `02_Abstract.md` | 2 | ✅ Created |
| 3 | `03_Keywords.md` | 3 | ✅ Created (was missing) |
| 4 | `04_Introduction.md` | 4 | ✅ Created |
| 5 | `05_Related_Work.md` | 5 | ✅ Created |
| 6 | `06_Methodology.md` | 6 | ✅ Created |
| 7 | `07_Experimental_Setup.md` | 7 | ✅ Created |
| 8 | `08_Results.md` | 8 | ✅ Created |
| 9 | `09_Discussion.md` | 9 | ✅ Created |
| 10 | `10_Conclusion.md` | 10 | ✅ Created |
| 11 | `11_Appendix_A_Supplementary_Materials.md` | 11 | ✅ Created |
| 12 | `12_References.bib` | 12 | ✅ Created (BibTeX) |

**Correction applied:** Previous workspace used 10 files with Keywords omitted and Introduction numbered as §3. Renumbered to match `Paper_Outline.md` Part VI.

**Index:** `paper/sections/README.md`

---

## Task 2 — Figure verification

All figures referenced in `Paper_Outline.md` Part II verified present in `paper/final_results_package/figures/`.

| Figure | Title | Asset file | Status |
| --- | --- | --- | --- |
| 1 | Overall Framework | `figure_01_framework.png` | ✅ Exists |
| 2 | Final S2 Architecture | `figure_02_s2_architecture.png` | ✅ Exists |
| 3 | Training Curves | `figure_03_training_curves.png` | ✅ Exists |
| 4 | Benchmark Comparison | `figure_04_benchmark_comparison.png` | ✅ Exists |
| 5 | Ablation Comparison | `figure_05_ablation_comparison.png` | ✅ Exists |
| 6a | SHAP Summary — Stress | `figure_06_shap_summary_stress.png` | ✅ Exists |
| 6b | SHAP Summary — Demand | `figure_06_shap_summary_demand.png` | ✅ Exists |
| 7 | Node Importance | `figure_07_node_importance.png` | ✅ Exists |
| 8 | Temporal Attribution | `figure_08_temporal_attribution.png` | ✅ Exists |
| 9 | Stress Attribution | `figure_09_stress_attribution.png` | ✅ Exists |

**Figure numbering:** 9 main figures + 1 subfigure (6b) — matches outline and `publication_figures.md`.  
**Authority:** Final Results Package numbering (not early freeze inventory).

---

## Task 3 — Table verification

All tables referenced in `Paper_Outline.md` Part III verified in `paper/final_results_package/publication_tables.md`.

| Table | Title | Source section | Status |
| --- | --- | --- | --- |
| 1 | Dataset Summary | `publication_tables.md` §1 | ✅ Exists |
| 2 | Training Configuration | `publication_tables.md` §2 | ✅ Exists |
| 3 | Benchmark Comparison | `publication_tables.md` §3 | ✅ Exists |
| 4 | Benchmark Statistical Significance | `publication_tables.md` §4 | ✅ Exists |
| 5 | Ablation Study Results | `publication_tables.md` §5 | ✅ Exists |
| 6 | Architecture Comparison (S1–S4) | `publication_tables.md` §6 | ✅ Exists |
| 7 | Explainability Summary | `publication_tables.md` §7 | ✅ Exists |

**Table numbering:** 7 main-text tables — matches outline and `manuscript_assets_inventory.md`.

---

## Task 4 — Section numbering verification

| Outline order (Part VI) | Section file | Match |
| ---: | --- | --- |
| 1 Title | `01_Title.md` | ✅ |
| 2 Abstract | `02_Abstract.md` | ✅ |
| 3 Keywords | `03_Keywords.md` | ✅ |
| 4 Introduction | `04_Introduction.md` | ✅ |
| 5 Related Work | `05_Related_Work.md` | ✅ |
| 6 Methodology | `06_Methodology.md` | ✅ |
| 7 Experimental Setup | `07_Experimental_Setup.md` | ✅ |
| 8 Results | `08_Results.md` | ✅ |
| 9 Discussion | `09_Discussion.md` | ✅ |
| 10 Conclusion | `10_Conclusion.md` | ✅ |
| 11 Appendix A | `11_Appendix_A_Supplementary_Materials.md` | ✅ |
| 12 References | `12_References.bib` | ✅ |

**IMRaD mapping:** Outline §6–8 correspond to Methodology, Experimental Setup, Results files §06–08.

---

## Task 5 — Figure numbering verification

| Check | Result |
| --- | --- |
| Sequential IDs 1–9 in outline | ✅ |
| Subfigure 6a/6b paired in §8.5 | ✅ |
| Methodology: Figures 1–2 | ✅ |
| Experimental Setup: Figure 3 | ✅ |
| Results: Figures 4–9 | ✅ |
| Caption source documented | `publication_figures.md` ✅ |

---

## Task 6 — Table numbering verification

| Check | Result |
| --- | --- |
| Sequential IDs 1–7 in outline | ✅ |
| Methodology: Tables 1–2 | ✅ |
| Results: Tables 3–7 | ✅ |
| LaTeX export targets documented | `table_01_dataset.tex` … `table_07_explainability.tex` ✅ |

---

## Task 7 — Bibliography

| Path | Status |
| --- | --- |
| `paper/sections/12_References.bib` | ✅ Official manuscript bibliography (BibTeX) |
| `paper/sections/11_Appendix_A_Supplementary_Materials.md` | ✅ Appendix A |
| `manuscript/overleaf/bibliography/` | ✅ Exists (LaTeX export target) |
| `manuscript/overleaf/bibliography/README.md` | ✅ Present |

Bibliography is maintained exclusively in `12_References.bib`. No Markdown references chapter is used.

---

## Related manuscript directories

| Directory | Purpose | Status |
| --- | --- | --- |
| `paper/sections/` | Markdown section scaffolds | ✅ Initialized |
| `manuscript/drafts/` | Working prose (future) | ✅ Exists |
| `manuscript/overleaf/figures/` | LaTeX figure copies | ✅ Exists (Exp04 assets) |
| `manuscript/overleaf/tables/` | LaTeX table exports | ✅ Exists (README) |
| `manuscript/overleaf/bibliography/` | `.bib` sources | ✅ Exists |
| `manuscript/supplementary/` | Optional S1–S5 assets | ✅ Exists |

---

## Constraints observed

- No manuscript prose written
- No figures modified or regenerated
- No tables modified
- No experiment outputs changed

---

## Definition of done

✔ All 12 manuscript section files present (outline-aligned; §11 = Appendix, §12 = BibTeX)  
✔ All 10 figure assets verified (9 + subfigure 6b)  
✔ All 7 table definitions verified  
✔ Section numbering matches outline  
✔ Figure numbering matches outline  
✔ Table numbering matches outline  
✔ Bibliography folder verified  

**Ready for Stage 06 — Manuscript Writing** (`paper/prompts/Manuscript_Writing_Prompt.md`).
