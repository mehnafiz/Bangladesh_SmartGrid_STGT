# Explainability Integration Report — Phase 22

**Date:** 7 July 2026  
**Authority:** `paper/prompts/22_Explainability_Manuscript_Integration.md`  
**Inputs:** `Explainability_Results_Report.md`, `Explainability_Publication_Mapping_Report.md`, Phase 21 verified figures  
**Constraint:** Manuscript integration only — no metric changes, no experiment reruns, no reference changes

---

## 1. Executive Summary

Phase 22 integrated frozen Experiment 04 explainability outputs into the **journal** (`paper/latex/`) and **conference** (`paper/conference/`) manuscripts. Integration comprised:

- Enhanced publication captions for Figs. 6a–9 (journal) and Fig. 7 (conference)
- Cross-reference and prose updates in Results, Discussion, and Experimental Setup
- Real spatial-attention matrix for Fig. 7 (from `mean_spatial_matrix.csv`, not PNG extraction)
- New explainability protocol subsection in journal Experimental Setup

**Metrics unchanged:** All numerical values preserved from frozen `xai_metrics.json` and Table 7 (e.g., G8 |φ| = 0.0191, Dhaka mass = 340.36, ρ = 0.422, demand perm ρ = −0.564, agreement = 52.2%).

**Compile verification:** Journal `main.pdf` — 28 pages ✓; Conference `main.pdf` — 6 pages ✓.

---

## 2. Journal Changes

### 2.1 Modified files

| File | Change type |
|---|---|
| `paper/latex/sections/04_experimental_setup.tex` | **New** §Explainability Protocol |
| `paper/latex/sections/05_results.tex` | Cross-refs to Figs. 6a–9; scope paragraph |
| `paper/latex/sections/06_discussion.tex` | Figure citations in explainability contribution |
| `paper/latex/figures/figure_06a.tex` | Enhanced caption |
| `paper/latex/figures/figure_06b.tex` | Enhanced caption |
| `paper/latex/figures/figure_07.tex` | Enhanced caption |
| `paper/latex/figures/figure_08.tex` | Enhanced caption |
| `paper/latex/figures/figure_09.tex` | Enhanced caption |
| `paper/latex/tables/table_07_explainability.tex` | Enhanced table caption |
| `paper/latex/figures/figure_06_shap_summary_*.pdf` | Re-synced from Phase 21 pipeline |
| `paper/latex/figures/figure_07_node_importance.pdf` | **Real** spatial matrix heatmap |
| `paper/latex/figures/figure_08_temporal_attribution.pdf` | Re-synced |
| `paper/latex/figures/figure_09_stress_attribution.pdf` | Re-synced |
| `paper/final_results_package/replot_frozen_explainability.py` | Uses `mean_spatial_matrix.csv` |

### 2.2 Section updates

| Section | Update |
|---|---|
| **§4 Experimental Setup** | Added `\subsection{Explainability Protocol}` — methods, scope (n=20 global, 24 cases), artefact paths, non-causal disclaimer |
| **§5.5 Error Analysis** | Unchanged structure; Figs. 6a/6b already cited in coalition-level paragraph |
| **§5.6 Explainability Analysis** | Scope cites §4 protocol + Figs. 6a–9; coalition/spatial/dual-path paragraphs cite specific figures |
| **§6 Discussion** | Explainability contribution now cites Figs. 6a, 6b, 7, 9 explicitly |
| **§7 Conclusion** | No change (already references post-hoc attribution) |

### 2.3 Figure integration (journal)

| Fig | Caption takeaway | First citation | Placement |
|---|---|---|---|
| **6a** | G8/G6 dominate stress \|φ\|; validates OSI supervision alignment | §5.5 coalition error structure | After §5.5 text; paired with 6b |
| **6b** | G6/G4/G10 dominate Dhaka demand; contrasts with 6a | §5.5 + §5.6 coalition attribution | Paired with 6a |
| **7** | Spatial attention heatmap; Dhaka mass; ρ=0.422 | §5.6 Spatial node attribution | Before temporal subsection |
| **8** | Near-uniform α_t; honest null lag selectivity | §5.6 Temporal attribution | After Fig. 7 |
| **9** | Dual-path on 2024-09-08; 52.2% agreement | §5.6 OSI dual-path | Before cross-method paragraph |
| **Table 7** | Headline cross-method metrics | §5.6 scope + cross-method | End of §5.6 float block |

---

## 3. Conference Changes

### 3.1 Modified files

| File | Change |
|---|---|
| `paper/conference/sections/04_results.tex` | Enhanced Explainability subsection; Fig. 7 takeaway |
| `paper/conference/figures/figure_07.tex` | Enhanced caption |
| `paper/conference/figures/figure_07_node_importance.pdf` | Real spatial matrix (synced) |
| `paper/conference_overleaf.zip` | Regenerated |

### 3.2 Conference strategy (per mapping report)

| Element | Decision |
|---|---|
| **Figures included** | Fig. 7 only (spatial attention heatmap) |
| **Figures excluded** | SHAP bars, temporal, dual-path (prose metrics only) |
| **Page budget** | 6 pages preserved |
| **Metrics in prose** | G8/G6 stress φ, G6/G4/G10 demand φ, ρ=0.422, 52.2% agreement, ρ=−0.564 demand discordance |

---

## 4. Updated Captions (summary)

### Journal

- **Fig. 6a:** What (stress \|φ\| by coalition) → Why (OSI supervision alignment) → Takeaway (G8/G6 dominate)
- **Fig. 6b:** What (Dhaka demand \|φ\|) → Why (task contrast) → Takeaway (calendar/lag vs limitation)
- **Fig. 7:** What (9×9 spatial attention) → Why (graph-XAI core result) → Takeaway (Dhaka + ρ=0.422)
- **Fig. 8:** What (α_t bars) → Why (temporal window usage) → Takeaway (near-uniform; null result)
- **Fig. 9:** What (dual-path panels) → Why (validation of stress head) → Takeaway (52.2% agreement; report both views)

### Conference

- **Fig. 7:** Condensed journal caption; emphasises highest-impact XAI visual for page budget

### Table 7

- Caption now states data sources (validation n=20, 24 cases) without changing cell values

---

## 5. Asset Pipeline Fix

`replot_frozen_explainability.py` now loads Fig. 7 from:

```
results/explainability/attention/mean_spatial_matrix.csv
```

This replaces the Phase 20 PNG pixel-extraction fallback, aligning manuscript figures with Phase 21 verified model outputs.

**Rebuild command:**

```bash
cd paper/final_results_package
../../.figure_build_venv/bin/python replot_frozen_explainability.py
../../.figure_build_venv/bin/python sync_publication_assets.py
```

---

## 6. Remaining Manual Checks

| Check | Status | Action |
|---|---|---|
| Journal PDF compile | ✅ 28 pages | Author review of caption line breaks |
| Conference PDF compile | ✅ 6 pages | Verify Fig. 7 readable at column width |
| Overleaf upload | ✅ Zip regenerated | Upload `conference_overleaf.zip` |
| Metric consistency | ✅ Unchanged | Spot-check Table 7 vs §5.6 prose |
| Appendix cross-refs | ⚠️ Not modified | Verify §8 appendix still cites supplementary Figs. S1/S4/S5 |
| Markdown source (`paper/sections/`) | ⚠️ Not synced | LaTeX is authoritative; sync markdown if dual-track maintained |
| Stress perm ρ (0.366) | ℹ️ Prose only | In §5.6 but not Table 7 — intentional per mapping |
| Captum vs custom IG wording | ✅ Preserved | "Captum-compatible" language retained |

---

## 7. What Was NOT Changed

- No experiment reruns
- No metric or numerical value modifications
- No bibliography / reference changes
- No methodology equations or coalition registry definitions
- No new figures added to conference (page limit preserved)
- No manuscript prose claiming causal attribution

---

## 8. Visual Consistency Checklist

| Criterion | Status |
|---|---|
| Journal Figs. 6–9 use PDF vector assets | ✅ |
| Fig. 7 from real `mean_spatial` matrix | ✅ |
| Captions state what / why / takeaway | ✅ |
| Cross-refs in Results match figure labels | ✅ |
| Conference single-figure XAI strategy | ✅ |
| Table 7 values match frozen JSON | ✅ |
| Compile clean (no missing figures) | ✅ |

---

**Phase 22 status: COMPLETE**
