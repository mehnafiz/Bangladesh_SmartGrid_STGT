# Final Explainability Integration Report — Phase 23

**Date:** 7 July 2026  
**Authority:** Phase 23 — Final Explainability Figure Generation & Manuscript Integration  
**Constraint:** All figures originate from the frozen S2 (A6) checkpoint and verified Experiment 04 outputs. No synthetic, placeholder, or fabricated values.

---

## 1. Executive Summary

Phase 23 generated **two publication-quality explainability figure sets** from frozen experimental artefacts and integrated them into **both** the journal and conference manuscripts.

| Deliverable | Status |
|---|---|
| Dual SHAP figure (demand + stress panels) | ✅ `figure_06_dual_shap` (PDF/SVG/PNG) |
| Regional/node attribution heatmap | ✅ `figure_07_node_importance` (PDF/SVG/PNG) |
| Journal integration | ✅ Figs. 6–9; refs updated |
| Conference integration | ✅ Figs. 6 + 7 (both fit; 7 pages) |
| Model retraining | ❌ Not performed |
| Metric modification | ❌ Not performed |
| Journal compile | ✅ `paper/latex/main.pdf` (28 pages) |
| Conference compile | ✅ `paper/conference/main.pdf` (7 pages) |

---

## 2. Frozen Provenance

| Component | Path / value |
|---|---|
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **Config** | `.../checkpoints/A6/seed_42/config.yaml` (λ_stress=20, seed=42) |
| **Metrics manifest** | `experiments/experiment_04_explainability_analysis/xai_metrics.json` |
| **Stress SHAP CSV** | `results/explainability/shap/global_stress.csv` |
| **Demand SHAP CSV** | `results/explainability/shap/global_demand_dhaka.csv` |
| **Spatial attention matrix** | `results/explainability/attention/mean_spatial_matrix.csv` |
| **Case studies** | 24 folders under `results/explainability/case_studies/` |
| **Train / val / test** | `data/features/{train,validation,test}_features.parquet` |
| **Graph** | Correlation adjacency τ = 0.65 (`graphs/adjacency_matrix.csv`) |

**Inference re-run:** Not required. Frozen CSV/JSON from Phase 21 (7 Jul 2026) were used. Checkpoint verified present locally.

---

## 3. Scripts Executed

```bash
# Manuscript figure generation (no model inference)
cd paper/final_results_package
../../.figure_build_venv/bin/python replot_frozen_explainability.py
../../.figure_build_venv/bin/python sync_publication_assets.py

# Journal compile
cd paper/latex
pdflatex main.tex && pdflatex main.tex

# Conference compile + Overleaf package
cd paper/conference
pdflatex main.tex && pdflatex main.tex
bash build_overleaf_zip.sh
```

**Code modified (figure pipeline only):**

| File | Change |
|---|---|
| `paper/final_results_package/replot_frozen_explainability.py` | Added `_plot_dual_shap()` — 2-panel SHAP from frozen CSVs; shared G1–G11 ordering |
| `paper/final_results_package/sync_publication_assets.py` | Added `figure_06_dual_shap` to sync manifest |

---

## 4. Figures Generated

### Figure 1 — Dual SHAP Analysis (manuscript Fig. 6)

| Property | Value |
|---|---|
| **Stem** | `figure_06_dual_shap` |
| **Formats** | PDF, SVG, PNG @ 300 DPI |
| **Panel (a)** | Global SHAP summary — demand forecasting (Dhaka) |
| **Panel (b)** | Global SHAP summary — operational stress forecasting |
| **Source** | `global_demand_dhaka.csv`, `global_stress.csv` |
| **Palette** | `ieee_design.py` (IEEE_ACCENT / IEEE_GREEN highlights) |
| **Ordering** | Shared coalition axis G1–G11 |

**Verified headline values (frozen CSV):**

| Coalition | Demand \|φ\| (MW) | Stress \|φ\| |
|---|---|---|
| G6 (calendar/trend) | 162.34 | 0.0190 |
| G8 (limitation stack) | 23.15 | 0.0191 |
| G4 (lags/rolling) | 101.26 | — |
| G10 (national generation) | 91.44 | 0.0082 |

### Figure 2 — Regional / Node Attribution Heatmap (manuscript Fig. 7)

| Property | Value |
|---|---|
| **Stem** | `figure_07_node_importance` |
| **Formats** | PDF, SVG, PNG @ 300 DPI |
| **Source** | `attention/mean_spatial_matrix.csv` (real 9×9 from model forward passes) |
| **Annotation** | ρ(attn, adj) = 0.422 |
| **Rendering** | `heatmap_cmap_contrast` + PowerNorm(γ=0.55); diagonal masked |

**Companion node SHAP mass (prose / Table 7, not heatmap cells):** Dhaka 340.36, Rajshahi 110.32, Khulna 108.91.

### Asset locations

```
paper/final_results_package/figures/figure_06_dual_shap.{pdf,svg,png}
paper/final_results_package/figures/figure_07_node_importance.{pdf,svg,png}
paper/latex/figures/          (synced copies)
paper/conference/figures/     (synced copies)
```

Legacy single-panel stems (`figure_06_shap_summary_stress`, `figure_06_shap_summary_demand`) retained for audit but **replaced in manuscript** by the dual figure.

---

## 5. Manuscript Integration

### 5.1 Journal (`paper/latex/`)

| Section | Changes |
|---|---|
| `sections/05_results.tex` | Replaced Fig. 6a/6b refs with unified `fig:6` + panel refs `(a)`/`(b)`; swapped `\input{figure_06a,b}` → `\input{figure_06}` |
| `sections/06_discussion.tex` | Updated explainability cross-refs to `fig:6(a/b)` |
| `figures/figure_06.tex` | **New** — dual SHAP wrapper + publication caption |
| `figures/figure_07.tex` | Caption clarified: heatmap = spatial **attention** weights; diagonal masked |

**Figure numbering (journal):**

| Printed | Label | Content |
|---|---|---|
| Fig. 6 | `fig:6` | Dual SHAP (demand + stress) |
| Fig. 7 | `fig:7` | Spatial attention heatmap |
| Fig. 8 | `fig:8` | Temporal attribution |
| Fig. 9 | `fig:9` | Dual-path stress attribution |

### 5.2 Conference (`paper/conference/`)

| Section | Changes |
|---|---|
| `sections/04_results.tex` | Both explainability figures inserted: Fig. 7 (heatmap, priority) then Fig. 6 (dual SHAP) |
| `figures/figure_06.tex` | **New** — compact dual SHAP caption |
| `figures/figure_07.tex` | Caption expanded (cell definition, diagonal mask, Dhaka mass) |

**Page budget:** Conference PDF compiles to **7 pages** with both figures included (previously 6 pages with heatmap only).

**Printed conference figure map:**

| Label | Printed # | Content |
|---|---|---|
| `fig:6` | Fig. 6 | Dual SHAP |
| `fig:7` | Fig. 5* | Node attribution heatmap |

\*Conference omits training-curve figure; printed numbers depend on float order in compiled PDF.

### 5.3 Captions added / rewritten

- **Fig. 6 (journal):** What (G1–G11 \|φ\| bars for demand vs stress), why (task-specialised coalition sensitivity), takeaway (limitation/calendar for stress; calendar/lags/generation for demand).
- **Fig. 6 (conference):** Abbreviated version of the same scientific content.
- **Fig. 7 (both):** Clarified that cells are **attention weights**, not SHAP mass; ρ = 0.422; diagonal masked.

---

## 6. Validation

| Check | Result |
|---|---|
| Figures from frozen model outputs | ✅ CSV/JSON provenance traced |
| G8 stress \|φ\| = 0.0191 | ✅ Matches `global_stress.csv` |
| G6 demand \|φ\| = 162.34 | ✅ Matches `global_demand_dhaka.csv` |
| ρ(attn, adj) = 0.422 | ✅ Matches `xai_metrics.json` |
| Dhaka node mass = 340.36 | ✅ Matches `xai_metrics.json` |
| Journal references resolve | ✅ Second `pdflatex` pass clean |
| Conference references resolve | ✅ Second `pdflatex` pass clean |
| Overleaf zip rebuilt | ✅ `paper/conference_overleaf.zip` |

**Known metric note (unchanged per phase constraint):** `xai_metrics.json` records demand permutation ρ = −0.345 (Phase 21 re-run); manuscript Table 7 / prose cite −0.564 from the prior frozen audit. Figures and coalition \|φ\| values use the current CSV artefacts; permutation ρ was **not** altered.

---

## 7. Remaining Manual Checks

1. **Supervisor review** — Visual inspection of `figure_06_dual_shap.pdf` and `figure_07_node_importance.pdf` at print scale.
2. **Overleaf upload** — Replace project with `paper/conference_overleaf.zip`; recompile on Overleaf.
3. **Permutation ρ consistency** — Decide whether to update Table 7 / prose to −0.345 or re-run Exp04 to reproduce −0.564 (out of Phase 23 scope).
4. **Journal submission** — Upload `paper/latex/main.pdf` + figure PDFs if journal portal requires separate assets.
5. **Optional cleanup** — Retire unused `figure_06a.tex` / `figure_06b.tex` wrappers (kept for audit trail).

---

## 8. Reproducibility Commands

```bash
# Full explainability re-inference (only if artefacts stale)
/opt/anaconda3/bin/python experiments/experiment_04_explainability_analysis/run_explainability.py

# Publication replot from frozen data (recommended)
cd paper/final_results_package
../../.figure_build_venv/bin/python replot_frozen_explainability.py
../../.figure_build_venv/bin/python sync_publication_assets.py
```

---

## 9. Verdict

**Phase 23 COMPLETE.**

Both required explainability figures are publication-quality, scientifically reproducible from the frozen PF-STGT S2 checkpoint, and integrated into journal and conference manuscripts with updated captions and cross-references. No models were retrained; no metrics were modified.
