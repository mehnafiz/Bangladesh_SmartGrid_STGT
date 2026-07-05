# Final Production Optimization Report

**Phase:** IEEE Conference Production Optimization  
**Manuscript:** `paper/conference/main.pdf`  
**Template reference:** `paper/template/IEEE-conference-template-062824/`  
**Date:** 5 July 2026

---

## 1. Author Block Corrections

### Before
- Abbreviated 3-line affiliation (`Dept.\ of CSE, AIUB` on one line)
- Extra newline after `\author{` breaking template continuity
- Inconsistent with journal manuscript and official IEEE template

### After
- Rebuilt to match official IEEE conference template exactly (4-line `\IEEEauthorblockA` per author):
  1. `\textit{Department of Computer Science \& Engineering}`
  2. `\textit{American International University-Bangladesh (AIUB)}`
  3. `Dhaka, Bangladesh`
  4. Email address
- `\author{` opens directly into first `\IEEEauthorblockN` (no intervening blank line)
- All six authors use identical affiliation structure, equal block widths, and consistent line breaks
- Matches `paper/latex/main.tex` and `IEEE-conference-template-062824.tex` layout

---

## 2. Figure Placement Corrections

| Figure | First Citation | Float Input Location | Specifier |
|---|---|---|---|
| Fig. 1 (framework) | Methodology §PF-STGT Architecture | Immediately after citation sentence | `[htbp]` |
| Fig. 2 (S2 architecture) | Methodology §PF-STGT Architecture | After architecture description paragraph | `[htbp]` |
| Fig. 4 (benchmark) | Results §Benchmark Performance | Immediately after opening paragraph | `[htbp]` |
| Fig. 5 (ablation) | Results §Ablation Study | Immediately after opening paragraph | `[htbp]` |
| Fig. 7 (node attribution) | Results §Explainability | Immediately after opening paragraph | `[htbp]` |

### Additional figure fixes
- Replaced `\centering\includegraphics` with IEEE-template `\centerline{\includegraphics[width=\linewidth]{...}}`
- Split Fig. 1 and Fig. 2 placement (previously stacked at section end) to eliminate figure wall
- Consistent `\linewidth` width across all five figures
- Changed `[!t]` → `[htbp]` per official template float philosophy

---

## 3. Table Placement Corrections

| Table | First Citation | Float Input Location | Specifier |
|---|---|---|---|
| Table I (setup) | Methodology §Dataset | Immediately after citation sentence | `[htbp]` |
| Table II (benchmark) | Results §Benchmark Performance | Immediately after opening paragraph | `[htbp]` |
| Table III (ablation) | Results §Ablation Study | Immediately after opening paragraph | `[htbp]` |

### Additional table fixes
- Wrapped tabular in `\begin{center}...\end{center}` per IEEE template convention
- Applied `\resizebox{\columnwidth}{!}{...}` to Tables I and II to eliminate column overflow
- Retained `\scriptsize` for dense numerical tables
- Caption remains above tabular (IEEE table head convention)

---

## 4. Typography Corrections

| Item | Correction |
|---|---|
| Packages | Removed unused `booktabs`; added `textcomp` per template |
| `\BibTeX` macro | Updated to official template definition (double-brace form) |
| OSI equation (Eq. 1) | Split across five `align` lines to eliminate 84 pt overfull hbox |
| Table I | `\resizebox` applied — eliminated 17 pt overfull hbox |
| Figure inclusion | Standardised on `\centerline{}` wrapper |
| Math typography | Preserved `\mathrm`, `\mathcal`, `\hat`, `\mathbf` conventions |
| Non-breaking spaces | Retained `~` in `Task~1`, `Fig.~`, `Table~`, `88.65~MW` |

### Compile log after optimization
- **Overfull hbox:** 0
- **Undefined references:** 0
- **Undefined citations:** 0
- **Compile errors:** 0

Minor `Underfull \hbox` warnings remain (badness 1824–3557) on long statistical sentences — within IEEE production tolerance and do not affect PDF appearance.

---

## 5. Float Optimization

Added to `main.tex` preamble:

```latex
\setcounter{topnumber}{2}
\setcounter{bottomnumber}{2}
\setcounter{totalnumber}{4}
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.08}
\renewcommand{\floatpagefraction}{0.85}
```

### Float distribution strategy
- Floats moved from section-end clusters to inline positions after first `\ref{}` citation
- Benchmark table + figure paired in Results §5.1
- Ablation table + figure paired in Results §5.3
- Explainability figure placed in Results §5.4 after text introduction
- Methodology table placed between dataset prose and graph-construction prose

---

## 6. Layout Optimization

### Page-by-page review

| Page | Content | Status |
|---|---|---|
| **1** | Title, 6-author block, abstract, keywords, Introduction opening | Balanced; author grid matches template |
| **2** | Introduction conclusion, Methodology (formulation, OSI, dataset, Table I) | Table I near citation; equation fits column |
| **3** | Graph construction, PF-STGT architecture, Eq. 2–3, Fig. 1–2 | Figures interleaved with text; no figure wall |
| **4** | Experimental Setup, Results (benchmark, Table II, Fig. 4, ablation, Table III, Fig. 5) | Dense but balanced; floats near citations |
| **5** | Explainability (Fig. 7), Discussion, Conclusion, Acknowledgment, References (22 entries) | References fill column; minor underfull vbox on page 4 only |

### Layout metrics
- **Final page count:** 5 pages
- **Overfull boxes:** 0 (eliminated from 2)
- **Column overflow:** 0
- **Widows/orphans:** None flagged by LaTeX

---

## 7. IEEE Template Compliance Improvements

| Template element | Compliance action |
|---|---|
| `\documentclass[conference]{IEEEtran}` | Unchanged |
| `\IEEEoverridecommandlockouts` | Retained |
| Package set | Aligned with template (`cite`, `amsmath`, `graphicx`, `textcomp`) |
| Author block structure | Rebuilt to 4-line `\IEEEauthorblockA` format |
| Table environment | `[htbp]` + `center` wrapper + caption above |
| Figure environment | `[htbp]` + `\centerline{}` + caption below |
| Float placement rule | "Insert after cited in text" — now enforced inline |
| Acknowledgment | `\section*{Acknowledgment}` (American spelling) |
| Bibliography | `\bibliographystyle{IEEEtran}` + BibTeX |

### Attempted but reverted
- `\IEEEtranbalance` — not defined in bundled `IEEEtran.cls` v1.8b; removed to preserve zero-error compile

---

## 8. Remaining Manual Issues (if any)

| Issue | Severity | Notes |
|---|---|---|
| Underfull hbox on long statistical sentences | Low | Cosmetic; acceptable for IEEE submission |
| Underfull vbox (page 4, badness 10000) | Low | Caused by float-to-text ratio; no visible white gap in PDF |
| Last-page column height imbalance | Low | References column may be slightly shorter; typical for 5-page papers |
| Architecture figures (Fig. 1–2) | None | PNG resolution adequate; no LaTeX scaling defects |

**No scientific content, numerical values, captions, citations, or section order were modified.**

---

## Compile Verification

```
cd paper/conference
pdflatex main.tex → bibtex main → pdflatex main.tex → pdflatex main.tex
Exit code: 0
Output: main.pdf (5 pages, 786,879 bytes)
Overfull hbox: 0 | Errors: 0 | Undefined refs: 0
```

---

## 🟢 Production Quality Achieved

The conference manuscript at `paper/conference/main.pdf` now matches the official IEEE conference template in author layout, float conventions, table/figure environments, and typography. All overfull boxes have been eliminated; floats appear after first citation; and the document compiles without errors or broken references.
