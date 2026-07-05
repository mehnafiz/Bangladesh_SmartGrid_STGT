# Section Editorial Report

**Date:** 2026-07-05  
**Section optimized:** Appendix A — Supplementary Materials only  
**File modified:** `paper/latex/sections/08_appendix.tex`  
**Scope:** Editorial refinement — no other sections modified

---

## 1. Section Optimized

**Appendix A: Supplementary Materials** (`\section{Supplementary Materials}` under `\appendices`)

Seven subsections preserved:
1. Complete benchmark tables (A.1.1–A.1.5)  
2. Additional statistical summaries (Wilcoxon, $R^2$ notes)  
3. Hyperparameter configuration  
4. Feature dictionary (tensors, channels, coalitions)  
5. Graph construction details  
6. Additional explainability outputs  
7. Reproducibility checklist  

- Line count: **584 → 540** (−8%; primarily spacing normalisation)  
- All table rows, numerical values, MD5 hashes, paths, and citations **unchanged**

---

## 2. Editorial Improvements

| Area | Change |
|------|--------|
| Opening paragraph | Tightened freeze-scope statement; removed redundant phrasing |
| Table intros | Shortened benchmark, ablation, per-region, and Wilcoxon lead-ins |
| Unavailable blocks | Standardised label to “Not in frozen repository”; condensed lists without omitting items |
| Hyperparameters | Direct authority statement; supporting-doc block preserved |
| Feature dictionary | Tighter leakage policy; coalition intro shortened |
| Graph construction | Condensed attention-bias and design-report prose |
| Explainability | Shortened unavailable-items block |
| Reproducibility | Streamlined checklist intro and reproduction guidance |
| Cross-references | `Section~6.4` → `Section~\ref{subsection:feature_engineering}` |
| Global | Active voice; removed journal-style qualifiers; preserved British spelling |

**Preserved intact:** All benchmark/ablation/architecture table values (88.65 MW, 0.0371, etc.); Wilcoxon p-values and CIs; hyperparameter settings ($\tau$ = 0.65, $\lambda_2$ = 20.0, seed 42); Spearman ρ values; MD5 hashes; git commit; chronological split counts; 10-item unavailable-artefacts list; all `\cite{}` keys and `\url{}` paths.

---

## 3. Layout Improvements

| Item | Status |
|------|--------|
| Paragraph spacing | Normalised triple blank lines after `\end{center}` to single blank line |
| Table formatting | `\scriptsize`, `\resizebox{\columnwidth}{!}{}`, and tabular content unchanged |
| Typography | `$R^2$`, en-dashes, `\texttt{}` paths preserved |
| Cross-references | Feature-dictionary pointer uses `\ref{subsection:feature_engineering}` |
| Section hierarchy | All `\subsection`/`\subsubsection` labels unchanged |

No float environment or caption changes required (appendix uses inline `center` + `tabular` blocks).

---

## 4. Figure/Table Adjustments

**Table content not modified.**

| Item | Status |
|------|--------|
| Benchmark tables (S2, B01–B07; A1–A6; S1–S4) | Values and formatting unchanged |
| Per-region MAE/$R^2$ tables | Unchanged |
| Wilcoxon / $R^2$ summary tables | Unchanged |
| Hyperparameter, feature, graph, XAI, reproducibility tables | Unchanged |
| Figure path references (Figures S1, 3–9) | Unchanged |

Caption placement and `\resizebox` scaling retained for IEEE column-width compliance.

---

## 5. Compile Status

| Step | Result |
|------|--------|
| `pdflatex main.tex` | ✅ Success |
| `bibtex main` | ✅ Success |
| `pdflatex` (cross-ref pass ×2) | ✅ Success |
| Output | `main.pdf` — **28 pages** |
| LaTeX errors | 0 |
| Undefined citations/references | 0 |
| Other sections modified | 0 |

---

## 6. Final Recommendation

Appendix A now reads as a compact IEEE supplementary reference: direct table intros, standardised “Not in frozen repository” blocks, and normalised spacing—while every frozen numeric value, statistical result, path, and hash remains verbatim. The appendix is suitable for reviewer verification against the publication freeze.

**Optional manual check:** Skim resized tables in the PDF to confirm all columns remain legible at `\scriptsize` scale.

---

## Status

🟢 **Section Ready**
