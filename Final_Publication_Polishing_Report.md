# Final Publication Polishing Report — Phase 24

**Date:** 7 July 2026  
**Authority:** Phase 24 — Final Publication Polishing  
**Constraint:** Presentation-only changes. No experiments, metrics, statistical tests, or scientific conclusions were modified.

---

## 1. Executive Summary

Phase 24 unified the visual design system across all publication figures, emphasised S2 over superseded S1 in the architecture diagram, added descriptive coalition labels to explainability plots, rewrote all figure and table captions to publication standard (What / Why / Takeaway), and verified clean compilation of both conference (7 pages) and journal (28 pages) manuscripts.

| Deliverable | Status |
|---|---|
| Global design tokens (`ieee_design.py`) | ✅ Extended |
| Figures 1–2 architecture polish | ✅ Rebuilt |
| Figures 3–6 chart polish | ✅ Rebuilt |
| Explainability descriptive labels | ✅ G1–G11 coalition names |
| Caption rewrite (conference + journal) | ✅ Figs. 1–7 |
| Table polish (conference) | ✅ Tables 1–3 |
| Conference PDF compile | ✅ 7 pages |
| Journal PDF compile | ✅ 28 pages |
| Science / metrics unchanged | ✅ Verified |

---

## 2. Global Design System

**File:** `paper/final_results_package/ieee_design.py`

| Token | Value | Purpose |
|---|---|---|
| `BOX_LW` | 1.2 | Standard diagram box borders |
| `BOX_LW_HERO` | 1.8 | S2 hero / metrics emphasis |
| `ARROW_LW` | 1.25 | Standard connectors |
| `ARROW_LW_EMPHASIS` | 1.45 | Fusion / output flow |
| `ARROW_MUTATION` | 12 | Consistent arrowhead size |
| `BAR_EDGE_LW` | 0.65 | Bar chart borders |
| `TITLE_SIZE` / `LABEL_SIZE` / `TICK_SIZE` | 11 / 10 / 9 pt | Typography hierarchy |
| `COALITION_SHORT` | G1–G11 registry | Descriptive SHAP labels |
| `style_bar_axes()` | helper | Shared grid + spine styling |
| `coalition_tick_labels()` | helper | Two-line ID + name ticks |

**Justification:** One visual language across architecture diagrams, bar charts, and explainability figures improves camera-ready cohesion and grayscale print readability.

---

## 3. Figure Modifications

### 3.1 Figure 1 — PF-STGT Framework

**File:** `build_publication_assets.py` → `figure_01_framework`

| Change | Justification |
|---|---|
| Unified `ARROW_LW` / `ARROW_LW_EMPHASIS` on all connectors | Consistent visual flow |
| Stronger title divider (linewidth 0.8, alpha 0.55) | Clearer information hierarchy |
| Accent-bar boxes with `BOX_LW` borders | Border consistency |
| Colour-coded flow: accent (inputs) → blue (encoding) → green (outputs) | Grayscale-distinguishable via line weight + position |

**Science unchanged:** Same nodes, tensors, graph, fusion, and heads.

### 3.2 Figure 2 — S2 Architecture

| Change | Justification |
|---|---|
| S1 reduced to small dashed muted box (55% alpha, 7 pt text) | De-emphasise superseded model |
| S2 hero enlarged with green shadow + `BOX_LW_HERO` border | Visual emphasis on final model |
| Trunk / metrics boxes use unified `BOX_LW` | Consistent with Fig. 1 |
| `$-$4.66 MW` badge repositioned at S1→S2 transition | Clearer selection narrative |

**Science unchanged:** Same S1/S2 relationship, τ=0.65, 749,058 params, loss, MAE 88.65, R² 0.745.

### 3.3 Figures 3–5 — Training / Benchmark / Ablation

| Figure | Changes |
|---|---|
| Fig. 3 (training curves) | Panel labels (a)/(b); IEEE-blue frame borders at `BOX_LW` |
| Fig. 4 (benchmark) | `style_bar_axes()` grid; consistent label sizes; `BAR_EDGE_LW` |
| Fig. 5 (ablation) | Same bar styling; hatch on A4 retained for demand-only distinction |

**Numerical values unchanged:** All MAE bars read from frozen CSVs.

### 3.4 Figures 6–7 — Explainability

**File:** `replot_frozen_explainability.py`

| Change | Justification |
|---|---|
| X-axis ticks: `G6\n(Calendar & trend)` format from frozen registry | Replaces anonymous G1–G11 labels |
| Dual SHAP panel styling unified with `style_bar_axes()` | Consistent with Figs. 4–5 |
| Heatmap axis labels: "source division" / "target division" | Publication readability |
| OSI component labels: c1/c2/c3 with descriptive names | Clearer dual-path Fig. 9 (journal) |

**Attribution values unchanged:** All |φ| from frozen `global_*.csv`; heatmap from `mean_spatial_matrix.csv`.

---

## 4. Caption Rewrites

All captions now follow **What → Why → Takeaway** structure.

### Conference (`paper/conference/figures/`)

| File | Label |
|---|---|
| `figure_01.tex` | `fig:1` |
| `figure_02.tex` | `fig:2` |
| `figure_04.tex` | `fig:4` |
| `figure_05.tex` | `fig:5` |
| `figure_06.tex` | `fig:6` |
| `figure_07.tex` | `fig:7` |

### Journal (`paper/latex/figures/`)

| File | Label |
|---|---|
| `figure_01.tex` – `figure_07.tex` | `fig:1` – `fig:7` (mirrored captions) |
| `figure_08.tex`, `figure_09.tex` | Retained from Phase 23 (already publication-grade) |

---

## 5. Table Modifications (Conference)

| File | Changes |
|---|---|
| `table_01_setup.tex` | Expanded caption; `\tabcolsep{4pt}`; `\arraystretch{1.2}` |
| `table_02_benchmark.tex` | Expanded caption; tighter column spacing |
| `table_03_ablation.tex` | Expanded caption; improved row spacing |

**Data unchanged:** All cell values identical to frozen experiment outputs.

---

## 6. Manuscript QA

| Check | Conference | Journal |
|---|---|---|
| PDF compiles | ✅ 7 pages | ✅ 28 pages |
| Undefined references | ✅ None (2-pass) | ✅ None (2-pass) |
| Figure numbering | fig:1,2,4,5,6,7 | fig:1–9 |
| Cross-references in text | ✅ Unchanged labels | ✅ Unchanged labels |
| Float placement | `[htbp]` / `[H]` for Fig. 7 | `[!t]` standard |
| Overleaf zip | ✅ Rebuilt | — |

**Note:** Conference printed figure order: Fig. 1–2 (methodology), Fig. 3–4 (results benchmark/ablation), Fig. 5–6 (explainability). Label `fig:4` prints as "Fig. 3" etc. due to omitted training-curve float — labels in `.tex` are authoritative for `\ref{}`.

---

## 7. Scripts Executed

```bash
cd paper/final_results_package
../../.figure_build_venv/bin/python build_publication_assets.py
../../.figure_build_venv/bin/python sync_publication_assets.py

cd paper/conference && pdflatex main.tex && pdflatex main.tex && bash build_overleaf_zip.sh
cd paper/latex && pdflatex main.tex && pdflatex main.tex
```

---

## 8. Files Changed

### Figure pipeline
- `paper/final_results_package/ieee_design.py`
- `paper/final_results_package/build_publication_assets.py`
- `paper/final_results_package/replot_frozen_explainability.py`

### Generated assets (synced to `paper/conference/figures/` and `paper/latex/figures/`)
- `figure_01_framework.{pdf,svg,png}`
- `figure_02_s2_architecture.{pdf,svg,png}`
- `figure_03_training_curves.png`
- `figure_04_benchmark_comparison.{pdf,svg,png}`
- `figure_05_ablation_comparison.{pdf,svg,png}`
- `figure_06_dual_shap.{pdf,svg,png}`
- `figure_07_node_importance.{pdf,svg,png}`
- `figure_08_temporal_attribution.{pdf,svg,png}`
- `figure_09_stress_attribution.{pdf,svg,png}`

### LaTeX — conference
- `paper/conference/figures/figure_01.tex` – `figure_07.tex`
- `paper/conference/tables/table_01_setup.tex` – `table_03_ablation.tex`

### LaTeX — journal
- `paper/latex/figures/figure_01.tex` – `figure_07.tex`

### Package
- `paper/conference_overleaf.zip` (rebuilt)

---

## 9. Remaining Manual Recommendations

1. **Print proof** — Review Fig. 1–2 at 100% scale in grayscale; confirm S2 hero box reads clearly.
2. **Coalition tick density** — If Fig. 6 feels crowded in two-column print, consider rotating x-labels 30° (presentation only).
3. **Journal tables** — Conference tables were polished; journal `paper/latex/tables/` captions can be aligned to the same What/Why/Takeaway format in a follow-up if required.
4. **Page limit** — Conference remains 7 pages; monitor if venue imposes a 6-page hard cap.
5. **Author final read** — Verify coalition descriptive names match supervisor terminology (e.g., "limitation stack" vs. "operational limitation").

---

## 10. Verdict

**Phase 24 COMPLETE.**

The manuscript presentation is now camera-ready quality with a unified IEEE design system, improved figure hierarchy, descriptive explainability labels, and publication-standard captions—without any change to frozen scientific content.
