# Manuscript Sections — Workspace Index

**Stage:** 06 manuscript (complete prose + BibTeX bibliography)  
**Outline authority:** `paper/paper_outline/Paper_Outline.md`  
**Audit authority:** `paper/consistency_audit/final_readiness_report.md`

---

## Section files (final submission order)

| File | Order | Title | Tables | Figures |
| --- | ---: | --- | --- | --- |
| `01_Title.md` | 1 | Title | — | — |
| `02_Abstract.md` | 2 | Abstract | — | — |
| `03_Keywords.md` | 3 | Keywords | — | — |
| `04_Introduction.md` | 4 | Introduction | — | — |
| `05_Related_Work.md` | 5 | Related Work | — | — |
| `06_Methodology.md` | 6 | Methodology | 1, 2 | 1, 2 |
| `07_Experimental_Setup.md` | 7 | Experimental Setup | 2 (xref) | 3 |
| `08_Results.md` | 8 | Results | 3–7 | 4–9 |
| `09_Discussion.md` | 9 | Discussion | — | — |
| `10_Conclusion.md` | 10 | Conclusion | — | — |
| `11_Appendix_A_Supplementary_Materials.md` | 11 | Appendix A — Supplementary Materials | S1–S4 | — |
| `12_References.bib` | 12 | References (BibTeX) | — | — |

---

## Bibliography policy

- **Official bibliography:** `12_References.bib` (BibTeX only).
- References are generated and maintained exclusively in this `.bib` file.
- **Do not** create `11_References.md`, `12_References.md`, or any Markdown references chapter.
- For LaTeX/Overleaf export, copy or symlink `12_References.bib` into `manuscript/overleaf/bibliography/`.

---

## Asset paths (frozen — do not modify)

| Asset type | Package source | Overleaf target |
| --- | --- | --- |
| Figures 1–9 | `paper/final_results_package/figures/` | `manuscript/overleaf/figures/` |
| Tables 1–7 | `paper/final_results_package/publication_tables.md` | `manuscript/overleaf/tables/` |
| Bibliography | `paper/sections/12_References.bib` | `manuscript/overleaf/bibliography/` |

---

## Drafting rules

1. One section per file; do not merge sections.
2. Cross-check numbers against `paper/final_results_package/statistical_summary.md`.
3. Apply claim guardrails from `paper/consistency_audit/claim_audit.md`.
4. Do not modify experiment outputs or regenerate frozen figures.
5. Add or edit bibliography entries only in `12_References.bib`; never recreate a Markdown references section.
