# Camera-Ready Production Report — Phase 25

**Date:** 7 July 2026  
**Authority:** Phase 25 — Camera-Ready IEEE Conference Production Polishing  
**Scope:** Presentation and typesetting only. Scientific content, metrics, methodology, references, and conclusions are unchanged.

---

## 1. Executive Summary

Phase 25 converted the conference manuscript from research-complete to camera-ready production quality. All Phase 24 “What / Why / Takeaway” caption scaffolding was removed in favour of concise IEEE-style prose. The author block was restored to the official `\IEEEauthorblockN` / `\IEEEauthorblockA` template structure. Float specifiers were unified, explainability reading flow was corrected, and typography/placement was tuned for two-column balance.

| Check | Result |
|---|---|
| Conference PDF | ✅ 7 pages, clean compile |
| Journal PDF | ✅ 28 pages, clean compile |
| Undefined references | ✅ None (two-pass) |
| Science frozen | ✅ Verified |
| Camera-ready assessment | ✅ **YES** — suitable for competitive IEEE conference submission |

---

## 2. Figure Caption Rewrites (Conference)

All captions rewritten in natural IEEE conference style. Artificial **What / Why / Takeaway** labels removed.

| Label | File | New caption (abridged) |
|---|---|---|
| `fig:1` | `figure_01.tex` | End-to-end PF-STGT framework (frozen S2): seven-day tensors, correlation graph, parallel encoding, dual heads. |
| `fig:2` | `figure_02.tex` | Frozen S2 (A6) with $\tau{=}0.65$; replaces S1; MAE 88.65 MW, $R^2$ 0.745. |
| `fig:4` | `figure_04.tex` | Test-set macro demand MAE; S2 lowest at 88.65 MW. |
| `fig:5` | `figure_05.tex` | Ablation demand MAE; A4 demand-only; S2 leads multi-task variants. |
| `fig:6` | `figure_06.tex` | Dual-panel GradientSHAP on G1--G11; demand vs stress coalition rankings. |
| `fig:7` | `figure_07.tex` | Spatial attention heatmap; masked diagonal; $\rho{=}0.422$. |

**Typography fixes on floats:**
- Replaced `\centerline{...}` with `\centering` (Figs. 4–5).
- Unified placement to `[!t]` on all figures and tables.
- Fig. 7 width restored to `\linewidth` (was 0.92).

---

## 3. Table Caption Rewrites (Conference)

| Label | File | Before | After |
|---|---|---|---|
| `tab:setup` | `table_01_setup.tex` | Long What/Why/Takeaway block | *Dataset properties and S2 training configuration.* |
| `tab:benchmark` | `table_02_benchmark.tex` | Long What/Why/Takeaway block | *Held-out test benchmark comparison ($n{=}264$ windows).* |
| `tab:ablation` | `table_03_ablation.tex` | Long What/Why/Takeaway block | *Configuration ablation on the held-out test split (A6 = S2).* |

Wilcoxon statistics remain in the table footnote row (not the caption), per IEEE convention.

---

## 4. Figure & Table Relocations

| Change | File | Justification |
|---|---|---|
| Explainability intro moved **before** Fig. 7 | `sections/04_results.tex` | Avoid figure appearing before its subsection context |
| Fig. 7 → interpretive sentence → Fig. 6 | `sections/04_results.tex` | Logical read order: spatial heatmap then coalition SHAP |
| Removed `[H]` fixed placement on Fig. 7 | `figure_07.tex` | Eliminates forced whitespace and column imbalance |
| Removed `\usepackage{float}` | `main.tex` | No longer needed without `[H]` floats |
| All floats → `[!t]` | figures/*.tex, tables/*.tex | Consistent IEEE top-float behaviour |

**No figures or tables were moved across sections** — only within Explainability subsection for reading flow.

---

## 5. Author Block

**File:** `paper/conference/authors.tex` (mirrored in `paper/latex/authors.tex`)

| Before | After |
|---|---|
| Custom `tabular` 2×3 grid without italics | Official IEEE `\IEEEauthorblockN` + `\IEEEauthorblockA` + `\and` |
| Roman affiliation text | `\textit{Department...}` and `\textit{AIUB...}` per IEEE template |
| Non-standard structure | Matches `IEEE-conference-template-062824.tex` lines 22–57 |

Names, affiliations, and emails unchanged.

---

## 6. Typography & Layout Improvements

| Item | Change |
|---|---|
| Float specifiers | Uniform `[!t]` across figures and tables |
| Figure inclusion | `\centering` + `\includegraphics[width=\linewidth]` throughout |
| Caption verbosity | Reduced ~60–70% on average |
| `float` package | Removed from `main.tex` |
| `placeins` + `\FloatBarrier` | Retained at end of Results to prevent explainability floats drifting into Discussion |
| `microtype` | Retained for margin polish |
| Caption skip lengths | Unchanged at IEEE production defaults (4 pt above) |

---

## 7. Journal Manuscript (Parallel Pass)

Journal figure captions (`paper/latex/figures/figure_01.tex` – `figure_09.tex`) updated to the same concise IEEE style. Journal table captions were already concise; no data changes.

---

## 8. Visual Consistency

Figures were **not regenerated** in this phase (Phase 24 design system remains authoritative). Phase 25 focused on LaTeX production layer:

- Consistent `[!t]` float behaviour
- Consistent `\centering` and `\linewidth` inclusion
- Consistent caption voice (declarative, single paragraph)
- Author block matches IEEEtran visual convention

---

## 9. Final QA Checklist

| Item | Status |
|---|---|
| Figure numbering (`fig:1`–`fig:7`) | ✅ |
| Table numbering (`tab:setup`, `benchmark`, `ablation`) | ✅ |
| Cross-references resolve | ✅ |
| No orphan What/Why/Takeaway labels | ✅ |
| No `[H]` forced floats | ✅ |
| Conference page count | 7 pages |
| Overleaf zip rebuilt | ✅ `paper/conference_overleaf.zip` |
| Metrics / values in captions | Unchanged (88.65, 0.745, 0.422, etc.) |

---

## 10. Remaining Manual Recommendations

1. **Author alignment** — If the official `\and` grid shows column drift on Overleaf, compare against local `main.pdf`; the IEEE template structure is now authoritative per Phase 25.
2. **Page limit** — Verify venue page cap (6 vs 7 pages); current PDF is 7 pages.
3. **Print proof** — Review Fig. 6 (tall dual SHAP) at two-column width on physical print or 100% PDF zoom.
4. **Final author proofread** — Scan abstract and conclusion once for typos (out of scope for automated production pass).

---

## 11. Files Modified

### Conference
- `main.tex`
- `authors.tex`
- `sections/02_methodology.tex` (restored truncated spatial-branch paragraph after accidental edit)
- `sections/04_results.tex`
- `figures/figure_01.tex` – `figure_07.tex` (6 files)
- `tables/table_01_setup.tex` – `table_03_ablation.tex` (3 files)

### Journal
- `authors.tex`
- `figures/figure_01.tex` – `figure_09.tex` (9 files)

### Package
- `paper/conference_overleaf/` (synced from `paper/conference/`)
- `paper/conference_overleaf.zip` (rebuilt)

---

## 12. Final Camera-Ready Assessment

**Question:** *If this PDF were submitted to a competitive IEEE conference today, would it visually resemble a professionally typeset accepted paper?*

**Answer: YES.**

The manuscript now exhibits:
- Concise IEEE-style captions without template-artefact scaffolding
- Official author-block formatting
- Consistent float and inclusion markup
- Logical explainability figure ordering
- Clean two-pass compilation with no reference errors

No further obvious production-quality issues remain within the conference scope.

---

## 13. Verdict

**Phase 25 COMPLETE.**

Camera-ready production polishing is finished. The paper is ready for supervisor final review and conference submission packaging.

---

## 14. Follow-Up Layout Pass (7 July 2026)

User-requested fixes after visual review:

### Author block (restored per user preference)
- Reverted from official `\IEEEauthorblockN`/`\and` stack to **2×3 fixed-width `tabular` grid**
- **No italic** affiliations — straight roman text
- Fixed column widths (`0.46\textwidth`) for vertical alignment
- Updated: `paper/conference/authors.tex`, `paper/latex/authors.tex`, `paper/conference_overleaf/`

### Blank-space / float fixes
- Removed `\FloatBarrier` and `placeins` package (was forcing asymmetric column gaps)
- Added `dblfloatfix` + `\raggedbottom` (eliminates stretched vertical glue in two-column mode)
- All floats: `[!t]` → `[!htbp]` for placement near citation
- Explainability: **full narrative paragraph first**, then figures (no text split between floats)
- Fig. 6 → `figure*` at `0.92\textwidth` (dual SHAP spans both columns; removes left-column orphan gap)
- Fig. 7 → `0.96\linewidth` single-column placement
- Benchmark/ablation: figure moved **after** supporting paragraph (table → text → figure)
- Tighter float separation: `\textfloatsep`, `\floatsep`, `\intextsep` reduced

### Compile result
- Conference PDF: **7 pages**, no underfull vbox warnings
- `conference_overleaf.zip` rebuilt

