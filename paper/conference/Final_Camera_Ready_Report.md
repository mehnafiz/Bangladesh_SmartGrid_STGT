# Final Camera-Ready Report

**Phase:** Final Camera-Ready Research Refinement  
**Manuscript:** `paper/conference/main.pdf`  
**Template reference:** `paper/template/IEEE-conference-template-062824/`  
**Date:** 5 July 2026

---

## Four-Pass Review Summary

| Pass | Focus | Key actions |
|---|---|---|
| **Pass 1** | Scientific clarity | Expanded Discussion with WHY-oriented subsections; added methodology fusion intuition; interpretive benchmark sentence |
| **Pass 2** | Writing quality | Fixed paragraph break in Introduction; tightened figure captions; improved transitions |
| **Pass 3** | Layout/production | Table `\arraystretch{1.15}`; floats verified post-citation; zero overfull boxes |
| **Pass 4** | IEEE publication | Author block verified against template; compile-clean; 6-page balanced layout |

---

## 1. Scientific Improvements

| Location | Improvement |
|---|---|
| **Methodology §III-C** | Explained why parallel fusion (not fixed spatial-then-temporal ordering) suits synchronised national load movements; clarified shared-encoder benefit for both tasks |
| **Results §V-A** | Interpreted T-GCN underperformance: shallow graph convolution insufficient for dense correlation and weekly window |
| **Discussion (new structure)** | Reframed from bullet labels to five interpretive subsections answering *why* results occur |

**All numerical values, statistics, and experimental claims remain unchanged.**

---

## 2. Discussion Improvements

Discussion restructured into five IEEE-style subsections:

| Subsection | Content |
|---|---|
| **V-A Why Correlation Graphs Outperform Geography** | National co-movement vs border adjacency; A5 stress--demand divergence; graded edge weights vs equal-weight geography |
| **V-B Why Multi-Task Learning Behaves as Observed** | Shared limitation/calendar structure; loss-balancing mechanism; Pareto trade-off interpretation (not destructive interference) |
| **V-C Bangladesh Grid Implications** | Co-visible stress fields; Dhaka dominance; daily cadence alignment with transformer capacity |
| **V-D Practical Deployment Considerations** | Single-service workflow; Dhaka monitoring; shadow-mode recommendation; scope qualifiers preserved |
| **V-E Limitations and Future Work** | Inferential bounds; attribution limits; replication, probabilistic forecasting, operator validation (no new experiments) |

Word count in Discussion: **~740** (up from ~349), using page budget for reviewer comprehension without filler.

---

## 3. Writing Improvements

- Separated contributions paragraph from section roadmap (missing line break corrected)
- Replaced bold-label Discussion blocks with formal `\subsection{}` headings for IEEE scanability
- Tightened figure captions to concise IEEE style while preserving scientific meaning
- Removed repetitive “frozen evaluation” phrasing in favour of precise scope statements
- Each Discussion subsection opens with a clear interpretive claim before evidence

---

## 4. Author Block Improvements

Verified and preserved exact IEEE template structure:

```latex
\author{\IEEEauthorblockN{Name}
\IEEEauthorblockA{\textit{Department of Computer Science \& Engineering} \\
\textit{American International University-Bangladesh (AIUB)}\\
Dhaka, Bangladesh \\
email@domain}
\and ...}
```

| Template element | Status |
|---|---|
| `\author{` opens directly into `\IEEEauthorblockN` | ✓ |
| Dept line: `\textit{...} \\` (space before break) | ✓ |
| Org line: `\textit{...}\\` (no extra space) | ✓ |
| City line: `Dhaka, Bangladesh \\` | ✓ |
| Email on fourth line | ✓ |
| Six equal-depth blocks | ✓ |

---

## 5. Figure Improvements

| Figure | Refinement |
|---|---|
| Fig. 1 | Caption tightened; full `\linewidth`; `[htbp]`; post-citation placement |
| Fig. 2 | Caption tightened; interleaved after architecture text |
| Fig. 4 | Concise caption with $n{=}264$; paired with Table II |
| Fig. 5 | Clarified A4 vs S2 distinction in caption |
| Fig. 7 | Concise attribution caption; placed after explainability text |

PNG assets unchanged (figures declared FINAL). LaTeX presentation optimised only.

---

## 6. Table Improvements

| Table | Refinement |
|---|---|
| Table I | `\arraystretch{1.15}` for row readability; `\resizebox{\columnwidth}{!}` |
| Table II | `\arraystretch{1.15}`; Wilcoxon footnote row retained |
| Table III | `\arraystretch{1.15}`; native column-width fit |

Captions unchanged in scientific content; placement immediately after first citation in each section.

---

## 7. Layout Improvements

| Metric | Result |
|---|---|
| Page count | **6** (within 7-page limit) |
| Overfull hbox | **0** |
| Compile errors | **0** |
| Broken refs/citations | **0** |
| Float placement | Inline after first `\ref{}` |
| Figure wall | Eliminated (Fig. 1 separated from Fig. 2 by equation text) |

Minor `Underfull \vbox` (badness 3029–10000) on pages 1 and 5 from float-to-text ratio — cosmetic only, not visible as layout defects.

---

## 8. IEEE Template Compliance

| Element | Compliant |
|---|---|
| `\documentclass[conference]{IEEEtran}` | ✓ |
| Author `\IEEEauthorblockN` / `\IEEEauthorblockA` | ✓ |
| Table: `[htbp]`, caption above, `center` wrapper | ✓ |
| Figure: `[htbp]`, `\centerline{}`, caption below | ✓ |
| Float-after-citation rule | ✓ |
| `microtype`, widow/orphan penalties | ✓ |
| `\section*{Acknowledgment}` | ✓ |
| `\bibliographystyle{IEEEtran}` | ✓ |

---

## 9. Final Page Count

| Metric | Value |
|---|---|
| **Pages** | **6** |
| Body words | ~2,659 |
| Bibliography | 22 entries |
| Figures | 5 |
| Tables | 3 |
| Equations | 3 numbered |

---

## 10. Camera-Ready Readiness

### Quality control

| Check | Status |
|---|---|
| Science unchanged | ✓ |
| No new experiments | ✓ |
| WHY-oriented Discussion | ✓ |
| Author block matches template | ✓ |
| Figures/tables complete | ✓ |
| Zero compile errors | ✓ |
| Zero overfull boxes | ✓ |
| Within 7-page limit | ✓ |

### Compile command
```bash
cd paper/conference
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

---

## 🟢 Camera-Ready IEEE Conference Paper

The manuscript at `paper/conference/main.pdf` is scientifically frozen, interpretively strengthened, template-compliant, and ready for IEEE conference submission.
