# Camera-Ready Refinement Report

**Phase:** 20 — IEEE Camera-Ready Conference Paper Refinement  
**Manuscript:** `paper/conference/main.pdf`  
**Template reference:** `paper/template/IEEE-conference-template-062824/`  
**Date:** 5 July 2026

---

## Review Passes Completed

| Pass | Focus | Outcome |
|---|---|---|
| **Pass 1** | Scientific quality | Clarified motivation, OSI components, metric rationale, benchmark interpretation, practical implications |
| **Pass 2** | Visual production | Author block rebuilt; floats verified post-citation; captions enriched; microtype added |
| **Pass 3** | IEEE camera-ready | Zero overfull boxes; zero compile errors; 6-page balanced layout within 7-page limit |

---

## 1. Scientific Improvements

| Section | Improvement |
|---|---|
| **Introduction** | Added planning-motivation bridge; stated central research question explicitly; contributions restructured for clarity |
| **Methodology** | Explained OSI component semantics ($c_1$–$c_3$); clarified why demand-loss scaling prevents collapse; motivated correlation graph from inter-regional co-movement |
| **Experimental Setup** | Justified macro MAE as primary metric over $R^2$; explained why Wilcoxon testing targets demand only; clarified ablation design intent |
| **Results** | Interpreted B02 high $R^2$ vs lower MAE divergence; expanded OSI variance explanation (74.5%); clarified ablation trade-off narrative |
| **Discussion** | Added practitioner guidance on correlation graphs; separated practical implications from limitations; distinguished load-only vs joint deployment paths |
| **Conclusion** | Restructured five outcomes as numbered findings for stronger closure |

**No numerical values, statistics, or experimental claims were altered.**

---

## 2. Writing Improvements

- Replaced abrupt transitions with explicit logical connectors (`therefore`, `consequently`, `for centres requiring`)
- Removed robotic inline-list contribution format that caused column underfull; restored flowing First–Fifth enumeration
- Each paragraph now carries one clear message (motivation, gap, formulation, contribution, interpretation)
- Reduced repetition of “frozen evaluation” phrasing while preserving scope qualifiers
- Improved topic sentences in Results subsections for scanability

---

## 3. Author Block Corrections

Rebuilt from official IEEE template (`IEEE-conference-template-062824.tex`), preserving only author order, names, affiliations, and emails.

### Template-compliant structure (per author)
```latex
\IEEEauthorblockN{Name}
\IEEEauthorblockA{\textit{Department of Computer Science \& Engineering} \\
\textit{American International University-Bangladesh (AIUB)}\\
Dhaka, Bangladesh \\
email@domain}
```

### Corrections applied
- Restored trailing space on `Department...` line (`} \\`) matching template line 23
- Restored trailing space on `Dhaka, Bangladesh \\` before email line
- Removed extra newline after `\author{` opening brace
- All six blocks use identical 4-line affiliation depth and typography

---

## 4. Figure Improvements

| Figure | Caption enhancement | Placement |
|---|---|---|
| Fig. 1 | Added pipeline component description | After first citation in §III-C |
| Fig. 2 | Clarified S2 parallel-fusion architecture | After architecture paragraph |
| Fig. 4 | Added $n{=}264$ and S2 ranking context | Immediately after benchmark citation |
| Fig. 5 | Clarified A4 vs S2 ranking interpretation | After ablation citation |
| Fig. 7 | Added connectivity interpretation | After explainability citation |

### Production settings
- `\centerline{\includegraphics[width=\linewidth]{...}}` per IEEE template
- `[htbp]` float specifier throughout
- Full column width retained for maximum readability
- All figures cited before first appearance

---

## 5. Table Improvements

| Table | Caption improvement | Layout |
|---|---|---|
| Table I | “Dataset properties and frozen S2 training configuration” | `\resizebox{\columnwidth}{!}` |
| Table II | “Held-out test benchmark…with Wilcoxon demand-MAE test” | `\resizebox{\columnwidth}{!}` |
| Table III | “Configuration ablation on the held-out test split” | Native `\columnwidth` fit |

- All tables use `\begin{center}` wrapper per template
- Caption above tabular (IEEE table head convention)
- No data values removed or modified

---

## 6. Layout Improvements

- Floats distributed inline after first `\ref{}` citation (not section-end clusters)
- Fig. 1 separated from Fig. 2 by architecture equation text (no figure wall)
- Page count increased from 5 → **6 pages** using available budget for clearer exposition
- Widow/orphan penalties enabled (`\clubpenalty`, `\widowpenalty`, `\displaywidowpenalty` = 10000)
- Float fraction parameters tuned for two-column balance

### Page-by-page review

| Page | Content | Status |
|---|---|---|
| 1 | Title, author grid, abstract, keywords, introduction | Balanced; author block matches template |
| 2 | Introduction close, methodology formulation, OSI, Table I | Equations fit column; table near citation |
| 3 | Graph construction, architecture, Fig. 1–2 | Figures interleaved with text |
| 4 | Experimental setup, benchmark results, Table II, Fig. 4 | Dense, intentional layout |
| 5 | Regional/stress, ablation, Table III, Fig. 5, explainability | Floats paired with discussion |
| 6 | Fig. 7, discussion, conclusion, acknowledgment, references | References complete; columns balanced |

---

## 7. Typography Improvements

| Item | Action |
|---|---|
| `microtype` | Added for improved paragraph justification |
| `textcomp` | Retained per template |
| Unused `booktabs` | Not present (clean) |
| Math | OSI equation split across lines; no overfull boxes |
| Non-breaking spaces | Preserved in `Fig.~`, `Table~`, `Task~1`, `88.65~MW` |
| Bold labels in Discussion | Retained for scanability (`\textbf{Graph prior selection.}` etc.) |

---

## 8. IEEE Template Compliance

| Element | Status |
|---|---|
| `\documentclass[conference]{IEEEtran}` | ✓ |
| `\IEEEoverridecommandlockouts` | ✓ |
| Author `\IEEEauthorblockN` / `\IEEEauthorblockA` | ✓ Rebuilt |
| Table `[htbp]` + `center` + caption above | ✓ |
| Figure `[htbp]` + `\centerline{}` + caption below | ✓ |
| Float-after-citation rule | ✓ |
| `\section*{Acknowledgment}` | ✓ |
| `\bibliographystyle{IEEEtran}` | ✓ |
| Package alignment with template | ✓ |

---

## 9. Final Page Count

**6 pages** (IEEE two-column, including references)

| Metric | Value |
|---|---|
| Body word count | ~2,420 |
| Bibliography entries | 22 |
| Figures | 5 |
| Tables | 3 |
| Equations | 3 numbered |

---

## 10. Final Publication Readiness

### Quality control checklist

| Check | Status |
|---|---|
| No text overlapping figures/tables | ✓ |
| No clipped figures/tables | ✓ |
| No oversized column overflow | ✓ |
| Figures near discussion | ✓ |
| Tables near discussion | ✓ |
| No excessive whitespace | ✓ |
| No overfull boxes | ✓ |
| No broken references | ✓ |
| No broken citations | ✓ |
| Consistent fonts/captions | ✓ |
| Compile errors | 0 |

### Compile verification
```
pdflatex → bibtex → pdflatex × 2
Exit code: 0 | main.pdf (6 pages, 793,025 bytes)
Overfull hbox: 0 | Errors: 0 | Undefined refs: 0
```

### Residual notes
- Minor `Underfull \vbox` (badness 3503–10000) from float-to-text ratio on pages 1 and 5 — cosmetic only, not visible as layout defects in PDF

---

## 🟢 Camera-Ready IEEE Conference Paper

The manuscript at `paper/conference/main.pdf` is scientifically unchanged, production-optimised, template-compliant, and ready for IEEE conference submission.
