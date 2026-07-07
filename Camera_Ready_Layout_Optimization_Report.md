# Camera-Ready Layout Optimization Report — Phase 26

**Date:** 7 July 2026  
**Scope:** `paper/conference/` — LaTeX layout only  
**Constraint:** No scientific content, metrics, figures, or plot regeneration changed

---

## 1. Executive Summary

Phase 26 optimised the conference PDF from **7 pages** to **6 pages** by right-sizing figures, converting unnecessary `figure*` spans to single-column floats, tightening float spacing, and improving float placement relative to first citation. All numerical values, captions (wording), and scientific claims are unchanged.

| Check | Before | After |
|---|---|---|
| Page count | 7 | **6** |
| `figure*` floats | 3 (Figs. 2, 6, 7) | **0** |
| Undefined references | — | **0** (clean bibtex build) |
| Scientific content | Frozen | **Unchanged** |

---

## 2. Figure Resizing (LaTeX scale only)

| Figure | Before | After | Column mode | Rationale |
|---|---|---|---|---|
| **Fig. 1** (framework) | `0.90\linewidth` | **`0.74\linewidth`** | Single | Vertical pipeline; 74% preserves labels without dominating column |
| **Fig. 2** (S2 arch.) | `figure*` `0.94\textwidth` | **`0.86\linewidth`** | Single | Horizontal diagram readable in one column; removes full-page float |
| **Fig. 4** (benchmark) | `\linewidth` | **`0.90\linewidth`** | Single | Bar chart; slight reduction frees text room |
| **Fig. 5** (ablation) | `\linewidth` | **`0.84\linewidth`** | Single | Six-row bar chart; was visually heavy at full width |
| **Fig. 6** (dual SHAP) | `figure*` `0.88\textwidth` | **`0.90\linewidth`** | Single | Stacked panels fit column at 90%; avoids spanning blank gutters |
| **Fig. 7** (heatmap) | `figure*` `0.50\textwidth` | **`0.76\linewidth`** | Single | Square heatmap; single-column 76% is smallest readable width |

**No PDF/PNG assets were regenerated.** Only `\includegraphics[width=...]` parameters changed.

---

## 3. Float Placement Moves

### Methodology (`sections/02_methodology.tex`)

| Before | After |
|---|---|
| Fig. 1 inserted **between** architecture intro and Eq. (spatial) | Architecture text + equation **complete first** |
| Fig. 2 at subsection end | Figs. 1 and 2 **together** at subsection end |

**Justification:** Prevents equation/text split by a tall vertical figure; both architecture figures appear after the full architectural description.

### Results — Benchmark (`sections/04_results.tex`)

| Before | After |
|---|---|
| Table → Wilcoxon paragraph → Fig. 4 | Table → **Fig. 4** → Wilcoxon paragraph |

**Justification:** Fig. 4 cited in opening sentence with Table II; placing the figure immediately after the table keeps visual evidence adjacent to the benchmark claim.

### Results — Explainability (`sections/04_results.tex`)

| Before | After |
|---|---|
| Intro → Fig. 7 para → Fig. 7 → Fig. 6 para → Fig. 6 → closing | Intro + **both figure narratives in one block** → Fig. 7 → Fig. 6 → closing |

**Justification:** Reduces float queue fragmentation; both explainability figures float together after their combined discussion.

### Tables

| Table | Placement | Change |
|---|---|---|
| Table I (`tab:setup`) | After graph-construction paragraph | **Unchanged** — correct first citation |
| Table II (`tab:benchmark`) | After benchmark opening paragraph | **Unchanged** |
| Table III (`tab:ablation`) | After ablation opening paragraph | **Unchanged** |

---

## 4. Global Typography / Spacing (`main.tex`)

| Parameter | Before | After |
|---|---|---|
| `\textfloatsep` | 7pt | **5pt** |
| `\floatsep` | 6pt | **4pt** |
| `\intextsep` | 6pt | **5pt** |
| `\abovecaptionskip` | 4pt | **3pt** |
| `\belowcaptionskip` | 0pt | 0pt (unchanged) |
| `\raggedbottom` | enabled | enabled (unchanged) |

---

## 5. Page-by-Page Layout Assessment

### Page 1 — Title block + Introduction
- Balanced text density.
- Author 2×3 grid unchanged.
- **No change required.**

### Page 2 — Introduction (end) + Methodology (start)
- Problem formulation and OSI equation flow continuously.
- Table I appears after dataset paragraph (appropriate).
- **Improved:** No oversized floats on this page.

### Page 3 — Methodology (architecture text)
- Full spatial/temporal description and Eq. (2) without figure interruption.
- **Improved:** Reading flow no longer broken mid-equation.

### Page 4 — Figs. 1–2 + Experimental Setup
- Figs. 1 (74%) and 2 (86%) stack in single column after architecture text.
- **Improved:** Replaced full-width Fig. 2 that previously consumed an entire page top.

### Page 5 — Results (benchmark + ablation)
- Table II + Fig. 4 (90%) adjacent.
- Regional/stress text fills column.
- Table III + Fig. 5 (84%).
- **Improved:** Text-to-figure ratio balanced; no graphic-only page.

### Page 6 — Explainability + Discussion + Conclusion + References
- Fig. 7 (76%) and Fig. 6 (90%) in single column.
- Discussion and conclusion follow with references.
- **Improved:** Eliminated large whitespace band from `figure*` placement; explainability no longer orphans Discussion text in one column.

---

## 6. Two-Column Decision Summary

| Figure | Decision | Reason |
|---|---|---|
| Fig. 1 | **Single-column** | Tall portrait diagram; 74% linewidth sufficient |
| Fig. 2 | **Single-column** (was `figure*`) | Wide but low aspect ratio; fits one column at 86% |
| Fig. 4 | **Single-column** | Standard bar chart |
| Fig. 5 | **Single-column** | Standard bar chart |
| Fig. 6 | **Single-column** (was `figure*`) | Dual panel readable at 90% column width |
| Fig. 7 | **Single-column** (was `figure*`) | 9×9 heatmap readable at 76% |

**Rule applied:** Use the **smallest width that preserves readability**; reserve `figure*` only when single-column scaling would make labels illegible (none required after this pass).

---

## 7. Files Modified

```
paper/conference/main.tex
paper/conference/sections/02_methodology.tex
paper/conference/sections/04_results.tex
paper/conference/figures/figure_01.tex
paper/conference/figures/figure_02.tex
paper/conference/figures/figure_04.tex
paper/conference/figures/figure_05.tex
paper/conference/figures/figure_06.tex
paper/conference/figures/figure_07.tex
paper/conference_overleaf/  (synced)
paper/conference_overleaf.zip  (rebuilt)
```

---

## 8. Remaining Manual Recommendations

1. **Print proof at 100% zoom** — Verify Fig. 6 coalition tick labels (G1–G11) remain legible at 90% column width; if a venue prints at small margins, consider `0.88\linewidth`.
2. **Page-limit check** — Final PDF is **6 pages** including references; confirm venue maximum (some IEEE tracks cap at 6).
3. **Fig. 1 legibility** — At 74% width, fine print in the footer annotation is small; do not reduce further without visual check.
4. **Last-page balance** — If references leave a short column tail on Page 6, `\IEEEtriggeratref{N}` + `\IEEEtranbalance` may be applied before `\bibliography` (not needed in current build).

---

## 9. Final Assessment

**Question:** Does each page look like a published IEEE conference paper?

**Answer: YES.**

The manuscript now has:
- No unnecessary full-width floats
- Figures sized to content, not maximised by default
- Floats adjacent to first discussion
- Reduced vertical whitespace and caption gaps
- Continuous text flow in methodology and results
- **6-page** camera-ready PDF with balanced text/figure mix

**Phase 26 COMPLETE.** Layout-only optimisation finished; scientific content identical.
