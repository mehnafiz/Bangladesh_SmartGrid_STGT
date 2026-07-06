# Publication Graphics Implementation Report — Phase 20

**Date:** 7 July 2026  
**Authority:** `paper/prompts/20_Publication_Graphics_Implementation.md`  
**Blueprint:** `Publication_Graphics_Enhancement_Report.md` (Phase 19, approved)  
**Constraint:** Graphics-only — no science, numerics, experiments, references, or manuscript prose changed

---

## 1. Implementation Summary

Phase 20 executed the approved publication graphics blueprint across the authoritative asset pipeline (`paper/final_results_package/`) and propagated outputs to journal (`paper/latex/`) and conference (`paper/conference/`) venues.

### 1.1 Design system (unified)

| Token | Hex | Applied to |
|---|---|---|
| `IEEE_BLUE` | `#2c5282` | Borders, axes, temporal bars |
| `IEEE_LIGHT_BLUE` | `#ebf8ff` | Box fills, annotation badges |
| `IEEE_GREEN` | `#276749` | S2 / final-model emphasis |
| `IEEE_LIGHT_GREEN` | `#f0fff4` | S2 architecture panels |
| `IEEE_RED` | `#c53030` | Superseded S1, OSI c3 |
| `IEEE_ACCENT` | `#3182ce` | Baseline bar charts |
| `IEEE_GRAY` | `#4a5568` | Arrows, secondary text |
| `IEEE_DARK` | `#1a202c` | Titles, bar edges |

**Typography:** Times serif via matplotlib `RC_PARAMS`; minimum 8 pt axis labels; vector PDF primary export via `export_triple()`.

### 1.2 Priority delivery

| Priority | Figures | Status |
|---|---|---|
| **P0** | Fig. 1 (framework), Fig. 2 (S2 architecture) | ✅ Single master — PDF/SVG/PNG; journal + conference share same asset |
| **P1** | Fig. 4, Fig. 5, Fig. 7 | ✅ Vector PDF; journal switched from PNG; conference unified |
| **P2** | Fig. 6a/6b, Fig. 9 | ✅ Replot from frozen CSV with IEEE palette |
| **P3** | Fig. 8, Tables | ✅ Temporal bar restyle; `\arraystretch` polish on journal tables |
| P4 | Fig. 3 | ⚠️ Panel borders harmonised; content remains raster (Exp01 reference) |

### 1.3 Venue unification

| Figure | Before | After |
|---|---|---|
| Fig. 1 | Journal PNG ≠ conference TikZ | **Same `figure_01_framework.pdf`** |
| Fig. 2 | Journal PNG ≠ conference TikZ | **Same `figure_02_s2_architecture.pdf`** |
| Figs. 4–9 | Mixed PNG/PDF | **PDF primary** in all `\includegraphics` wrappers |

Conference TikZ sources (`figure_01_tikz.tex`, `figure_02_tikz.tex`) remain on disk but are **no longer referenced** by `figure_01.tex` / `figure_02.tex`.

---

## 2. Modified Files

### 2.1 Pipeline scripts (authoritative source)

| File | Change |
|---|---|
| `paper/final_results_package/ieee_design.py` | Unified IEEE design tokens, `heatmap_cmap()`, `export_triple()` |
| `paper/final_results_package/build_publication_assets.py` | Redrawn Figs. 1–2; styled Figs. 4–5; IEEE borders on Fig. 3 |
| `paper/final_results_package/replot_frozen_explainability.py` | Styled Figs. 6–9; vectorised Fig. 7 from frozen PNG matrix |
| `paper/final_results_package/sync_publication_assets.py` | **New** — copies PDF/SVG/PNG to journal and conference trees |

### 2.2 Frozen derived data (style-only, no experiment rerun)

| File | Purpose |
|---|---|
| `paper/final_results_package/frozen/figure_07_matrix.csv` | 9×9 spatial matrix extracted once from Exp04 frozen PNG for vector replot |

### 2.3 LaTeX figure wrappers — journal (`paper/latex/figures/`)

| File | Change |
|---|---|
| `figure_01.tex` | PNG → PDF |
| `figure_02.tex` | PNG → PDF |
| `figure_04.tex` | PNG → PDF |
| `figure_05.tex` | PNG → PDF |
| `figure_06a.tex` | PNG → PDF |
| `figure_06b.tex` | PNG → PDF |
| `figure_07.tex` | PNG → PDF |
| `figure_08.tex` | PNG → PDF |
| `figure_09.tex` | PNG → PDF |

### 2.4 LaTeX figure wrappers — conference (`paper/conference/figures/`)

| File | Change |
|---|---|
| `figure_01.tex` | TikZ `\input` → `\includegraphics{figure_01_framework.pdf}` |
| `figure_02.tex` | TikZ `\input` → `\includegraphics{figure_02_s2_architecture.pdf}` |
| `figure_07.tex` | PNG → PDF |

(Figs. 4–5 conference wrappers already used PDF — unchanged.)

### 2.5 Journal tables (`paper/latex/tables/`)

| File | Change |
|---|---|
| `table_01_dataset.tex` | `\arraystretch{1.2}` |
| `table_02_training.tex` | `\arraystretch{1.2}` |
| `table_03_benchmark.tex` | `\arraystretch{1.15}` |
| `table_04_benchmark_stats.tex` | `\arraystretch{1.15}` |
| `table_05_ablation.tex` | `\arraystretch{1.15}` |
| `table_06_architecture.tex` | `\arraystretch{1.15}` |
| `table_07_explainability.tex` | `\arraystretch{1.15}` |

**No table data values changed.** Conference tables already had `\arraystretch{1.15}` — unchanged.

### 2.6 Build artefacts

| File | Change |
|---|---|
| `paper/conference/main.pdf` | Recompiled (6 pages) |
| `paper/latex/main.pdf` | Recompiled (28 pages) |
| `paper/conference_overleaf.zip` | Regenerated with new PDF/SVG/PNG assets |

---

## 3. Generated Assets

All assets written to `paper/final_results_package/figures/` and synced to `paper/latex/figures/` and `paper/conference/figures/`.

### 3.1 P0 — Architecture masters (PDF + SVG + PNG)

| Asset | PDF | SVG | PNG |
|---|---|---|---|
| `figure_01_framework` | 51 KB | 107 KB | 189 KB |
| `figure_02_s2_architecture` | 53 KB | 94 KB | 121 KB |

### 3.2 P1 — Results bar charts (PDF + SVG + PNG)

| Asset | PDF | SVG | PNG |
|---|---|---|---|
| `figure_04_benchmark_comparison` | 32 KB | 59 KB | 82 KB |
| `figure_05_ablation_comparison` | 33 KB | 64 KB | 104 KB |
| `figure_07_node_importance` | 31 KB | 83 KB | 108 KB |

### 3.3 P2/P3 — Explainability (PDF + SVG + PNG)

| Asset | PDF | SVG | PNG |
|---|---|---|---|
| `figure_06_shap_summary_stress` | 24 KB | 44 KB | 69 KB |
| `figure_06_shap_summary_demand` | 26 KB | 47 KB | 69 KB |
| `figure_08_temporal_attribution` | 18 KB | 34 KB | 43 KB |
| `figure_09_stress_attribution` | 21 KB | 43 KB | 71 KB |

### 3.4 Unchanged raster

| Asset | Format | Notes |
|---|---|---|
| `figure_03_training_curves` | PNG only | Exp01 W20 reference panels; border harmonisation only |

**Total new triple-format figures:** 9 (27 vector files + 9 PNG fallbacks)  
**Sync count:** 56 file copies per run (`sync_publication_assets.py`)

---

## 4. Verification

| Check | Result |
|---|---|
| **Grayscale readability** | ✅ Box borders (`IEEE_DARK` 0.6 pt), hatch on A4 bar, green/red distinguishable by weight and position |
| **Print readability** | ✅ Vector PDF for Figs. 1–2, 4–5, 6–9, 7; 300 DPI PNG fallbacks |
| **Two-column readability** | ✅ Conference compiles at 6 pages; Fig. 7 at `0.92\linewidth` |
| **Overleaf compatibility** | ✅ `conference_overleaf.zip` regenerated; real PNG fallbacks included; PDF primary in wrappers |
| **Vector asset integrity** | ✅ `file figure_01_framework.pdf` → PDF 1.4, 1 page |
| **LaTeX compile — conference** | ✅ `pdflatex main.tex` — 6 pages, exit 0 |
| **LaTeX compile — journal** | ✅ `pdflatex main.tex` — 28 pages, exit 0 |
| **Science unchanged** | ✅ All numeric sources remain frozen CSV/JSON; no experiment reruns |

### 4.1 Rebuild commands

```bash
cd paper/final_results_package
../.figure_build_venv/bin/python build_publication_assets.py
../.figure_build_venv/bin/python sync_publication_assets.py
```

Requires `.figure_build_venv` (matplotlib, numpy, pillow).

---

## 5. Remaining Limitations

| Item | Detail | Recommended follow-up |
|---|---|---|
| **Fig. 7 matrix source** | 9×9 values extracted from frozen Exp04 PNG via YlOrRd inverse mapping; rank structure preserved, not raw `mean_spatial` floats | Export `mean_spatial` to JSON in freeze pipeline (future experiment packaging only) |
| **Fig. 3 training curves** | Still raster screenshots from Exp01 W20 | Replot from frozen loss CSV if available (P4 / supplementary) |
| **Legacy TikZ files** | `figure_01_tikz.tex`, `figure_02_tikz.tex` orphaned in conference tree | Safe to delete in cleanup pass |
| **Matplotlib SVG** | Text paths may not be fully editable in Illustrator | Use PDF for journal submission |
| **Fig. 7 ρ annotation** | Added in-figure (`ρ=0.422`) per blueprint; also in caption/table | Confirm author preference for duplication |
| **Conference overleaf zip** | Includes unused TikZ and extra explainability assets | Trim in packaging cleanup if upload size matters |

---

## 6. Visual Consistency Checklist

| Criterion | Status |
|---|---|
| Single colour palette across all figures | ✅ `ieee_design.py` |
| Times-compatible serif typography | ✅ matplotlib serif RC |
| S2 / A6 visually dominant in Figs. 2, 4, 5 | ✅ green emphasis + larger S2 panel |
| S1 superseded styling (muted red) | ✅ Fig. 2 |
| Consistent bar chart styling (Figs. 4, 5, 6, 8, 9) | ✅ edge colour, spine removal, label size |
| Heatmap IEEE sequential colormap | ✅ `heatmap_cmap()` Fig. 7 |
| Journal = conference asset for Figs. 1–2 | ✅ shared PDF masters |
| Tables: uniform row spacing | ✅ journal `\arraystretch` |
| No manuscript prose edits | ✅ sections untouched |
| No numerical value changes | ✅ frozen CSV/JSON only |

---

## 7. Figure-by-Figure Implementation Notes

### Figure 1 — PF-STGT framework (P0)
Three-band layout (INPUTS → ENCODING → OUTPUTS); gated fusion highlighted in green; tensor annotations preserved; exported PDF/SVG/PNG.

### Figure 2 — S2 architecture (P0)
S2 panel enlarged vs muted S1; −4.66 MW arrow; test metrics box unchanged; shared master with journal.

### Figures 4 & 5 — Bar charts (P1)
Frozen CSV values unchanged; S2/A6 green; A4 hatch pattern; `[final]` text label replaces star glyph (font compatibility).

### Figure 7 — Node heatmap (P1)
Vector PDF with IEEE sequential cmap; region labels 9 pt; ρ(attn, adj)=0.422 annotation badge.

### Figures 6a/6b — SHAP (P2)
Replotted from `results/explainability/shap/global_*.csv`; G6/G8 coalition highlight.

### Figure 8 — Temporal α_t (P3)
Near-uniform bars preserved; minimal IEEE blue styling.

### Figure 9 — Dual-path stress (P2)
OSI components: green/accent/red; SHAP panel IEEE blue; frozen case `2024-09-08`.

### Tables (P3)
Spacing-only polish; conference tables already compliant.

---

**Phase 20 status: COMPLETE**  
**Next optional phase:** Caption enrichment (separate manuscript edit phase per Phase 19 blueprint)
