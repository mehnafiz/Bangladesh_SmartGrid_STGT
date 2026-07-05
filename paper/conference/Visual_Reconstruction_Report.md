# Visual Reconstruction Report

**Phase:** 22 — Camera-Ready Visual & Template Reconstruction  
**Manuscript:** `paper/conference/main.pdf`  
**Template reference:** `paper/template/IEEE-conference-template-062824/`  
**Date:** 5 July 2026

---

## Summary

Phase 22 reconstructed the two schematic figures as native LaTeX TikZ vector graphics, unified the publication colour palette across all figures, switched bar-chart figures to PDF vector output, and extracted the author block into a template-derived `authors.tex` file. Scientific content is unchanged.

---

## 1. Author Block Reconstructed from Template

### Action
- Discarded inline `\author{...}` block from `main.tex`
- Created `authors.tex` by copying the **exact** `\author{}` / `\IEEEauthorblockN` / `\IEEEauthorblockA` structure from `IEEE-conference-template-062824.tex` (lines 22–57)
- Replaced only author names, institution lines, city, and emails
- Included via `\input{authors}` in `main.tex`

### Template structure preserved
```latex
\IEEEauthorblockA{\textit{Department...} \\
\textit{American International University-Bangladesh (AIUB)}\\
Dhaka, Bangladesh \\
email@domain}
```

Six equal-depth author blocks with `\and` separators.

---

## 2. Figure 1 Recreated

### Before
- Raster PNG (3261×1911 px, matplotlib-generated)
- Potential scaling artifacts at print resolution

### After
- **Native TikZ vector** in `figures/figure_01_tikz.tex`
- Shared palette via `figures/ieee_fig_colors.tex`
- Scientific content identical:
  - Regional node features $(B,T{=}7,N{=}9,F{=}9)$
  - Global context $(B,T{=}7,F{=}17)$
  - Graph adjacency $(N,N)$
  - Embedding + Positional Encoding
  - Graph Transformer, Temporal Transformer, Gated Parallel Fusion
  - Demand Head (9 MW), Stress Head (OSI)
  - Footer: S2 correlation graph ($\tau{=}0.65$)

### Quality
- Type 1 fonts (Computer Modern via LaTeX)
- Infinitely scalable
- No raster blur
- Rounded boxes, consistent 0.45 pt borders, Stealth arrows

---

## 3. Figure 2 Recreated

### Before
- Raster PNG (2961×1610 px)

### After
- **Native TikZ vector** in `figures/figure_02_tikz.tex`
- Matching palette and box styles with Figure 1
- Scientific content identical:
  - S1 (superseded) hybrid graph → S2 (final) correlation graph
  - $-$4.66 MW improvement arrow
  - Shared trunk (749,058 params)
  - Multi-task loss: Huber/100 + 20·MSE(OSI)
  - Test metrics: 88.65 MW MAE, $R^2$ 0.745

---

## 4. Figure Quality Improvements

| Figure | Format | Improvement |
|---|---|---|
| **Fig. 1** | TikZ vector | Rebuilt from scratch; editable LaTeX source |
| **Fig. 2** | TikZ vector | Rebuilt; visually paired with Fig. 1 |
| **Fig. 4** | PDF vector | Switched from PNG to `figure_04_benchmark_comparison.pdf` |
| **Fig. 5** | PDF vector | Switched from PNG to `figure_05_ablation_comparison.pdf` |
| **Fig. 7** | PNG raster | Retained (frozen Exp04 export; no vector source available) |

### Unified visual identity (`ieee_fig_colors.tex`)

| Colour | Hex | Usage |
|---|---|---|
| ieeeblue | `#2c5282` | Primary borders, schematic boxes |
| ieeelightblue | `#ebf8ff` | Primary fills |
| ieeegreen | `#276749` | S2 / final emphasis |
| ieeered | `#c53030` | Superseded S1 |
| ieeegray | `#4a5568` | Arrows |
| ieeeaccent | `#3182ce` | Bar charts (baseline models) |

Bar charts (Figs. 4–5) use the frozen matplotlib PDF export with the same palette as the original publication asset builder.

---

## 5. Placement Improvements

| Figure | Placement | Status |
|---|---|---|
| Fig. 1 | Immediately after first citation (§III-C) | ✓ |
| Fig. 2 | After architecture paragraph, separated from Fig. 1 by equation | ✓ No figure wall |
| Fig. 4 | With Table II after benchmark citation | ✓ |
| Fig. 5 | With Table III after ablation citation | ✓ |
| Fig. 7 | After explainability citation | ✓ |

Float specifier: `[htbp]` throughout. TikZ figures use `\resizebox{\linewidth}{!}{...}` for optimal column fill.

---

## 6. Visual Consistency Improvements

- Figs. 1–2 share TikZ box styles, arrow weights, rounded corners, and colour definitions
- Figs. 4–5 share matplotlib PDF styling from frozen asset pipeline
- Caption format: figures end with period; tables without period (IEEE convention)
- All schematic and chart figures use IEEE Times body font context
- Line weights: 0.4–0.55 pt arrows, 0.45 pt box borders

---

## 7. Remaining Manual Observations

| Item | Priority | Notes |
|---|---|---|
| **Fig. 7** (node attribution heatmap) | Low | Remains 1050×900 px PNG from frozen Exp04; acceptable at column width but only non-vector figure |
| Last-page column balance | Low | References column slightly shorter; typical for 6-page papers |
| Legacy PNG symlinks | Info | `figure_01_framework.png`, `figure_02_s2_architecture.png` retained but superseded by TikZ in compile |

**No blocking visual defects.**

---

## Compile Verification

```
Packages added: tikz, arrows.meta, calc, positioning
pdflatex → bibtex → pdflatex × 2
Exit code: 0
Output: main.pdf (6 pages, 392,009 bytes)
Overfull hbox: 0 | Errors: 0 | Undefined refs: 0
```

PDF size reduced from ~796 KB (raster figures) to ~392 KB (vector schematics + PDF charts), confirming successful vector integration.

---

## Files Created / Modified

| File | Action |
|---|---|
| `authors.tex` | Created from IEEE template |
| `figures/ieee_fig_colors.tex` | Shared palette |
| `figures/figure_01_tikz.tex` | TikZ Figure 1 |
| `figures/figure_02_tikz.tex` | TikZ Figure 2 |
| `figures/figure_01.tex` | Uses TikZ |
| `figures/figure_02.tex` | Uses TikZ |
| `figures/figure_04.tex` | PDF include |
| `figures/figure_05.tex` | PDF include |
| `figures/figure_04_benchmark_comparison.pdf` | Copied from publication package |
| `figures/figure_05_ablation_comparison.pdf` | Copied from publication package |
| `main.tex` | TikZ packages + `\input{authors}` |

**No changes to** `paper/latex/`, scientific text, numerical values, or conclusions.

---

## 🟢 Camera-Ready Visual Quality Achieved

The conference manuscript now uses true vector graphics for the framework and architecture figures, PDF vector bar charts, a template-derived author block, and a unified IEEE publication colour palette. Ready for submission.
