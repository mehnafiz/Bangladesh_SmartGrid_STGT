# Final Results Package

## Objective

Prepare all publication-ready tables, figures, and statistical summaries for the manuscript.

This stage does not generate new experimental results.

It organizes validated results into publication-quality assets.

---

## Execution Record — Stage 05B

| Field | Value |
| --- | --- |
| **Stage** | 05B — Final Results Package |
| **Executed** | 2026-06-16 |
| **Freeze reference** | `paper/publication_freeze/` (2026-06-25) |
| **Final model** | S2 — Correlation-Only PF-STGT (A6, seed 42) |
| **Experiments rerun** | None |
| **Experimental outputs modified** | None |

### Deliverables status

| Deliverable | Path | Status |
| --- | --- | --- |
| Publication tables | `publication_tables.md` | ✅ Complete (Tables 1–7) |
| Publication figures | `publication_figures.md` | ✅ Complete (Figures 1–9) |
| Statistical summary | `statistical_summary.md` | ✅ Complete |
| Asset inventory | `manuscript_assets_inventory.md` | ✅ Complete |
| Figure assets | `figures/` (11 PNG files) | ✅ Complete |
| Build script | `build_publication_assets.py` | ✅ Complete |

### Figure generation summary

| Figure | Method |
| --- | --- |
| 1–2 | Schematic diagrams from frozen architecture documentation |
| 3 | Combined panel from Exp01 frozen loss PNGs |
| 4–5 | Bar charts from frozen Exp02/Exp03 CSV (no model inference) |
| 6–9 | Copied from Exp04 frozen figure outputs |

---

## Final Tables

| ID | Title | Document section |
| --- | --- | --- |
| **Table 1** | Dataset Summary | `publication_tables.md` §1 |
| **Table 2** | Training Configuration | `publication_tables.md` §2 |
| **Table 3** | Benchmark Comparison | `publication_tables.md` §3 |
| **Table 4** | Benchmark Statistical Significance | `publication_tables.md` §4 |
| **Table 5** | Ablation Study Results | `publication_tables.md` §5 |
| **Table 6** | Architecture Comparison | `publication_tables.md` §6 |
| **Table 7** | Explainability Summary | `publication_tables.md` §7 |

---

## Final Figures

| ID | Title | File |
| --- | --- | --- |
| **Figure 1** | Overall Framework | `figures/figure_01_framework.png` |
| **Figure 2** | Final S2 Architecture | `figures/figure_02_s2_architecture.png` |
| **Figure 3** | Training Curves | `figures/figure_03_training_curves.png` |
| **Figure 4** | Benchmark Comparison | `figures/figure_04_benchmark_comparison.png` |
| **Figure 5** | Ablation Comparison | `figures/figure_05_ablation_comparison.png` |
| **Figure 6** | SHAP Summary | `figures/figure_06_shap_summary_stress.png`, `figure_06_shap_summary_demand.png` |
| **Figure 7** | Node Importance | `figures/figure_07_node_importance.png` |
| **Figure 8** | Temporal Attribution | `figures/figure_08_temporal_attribution.png` |
| **Figure 9** | Stress Attribution | `figures/figure_09_stress_attribution.png` |

---

## Statistical Summary

Consolidated in `statistical_summary.md`:

* Final p-values (Wilcoxon, Bonferroni-corrected)
* Bootstrap 95% confidence intervals
* Effect sizes (Cohen's d, % MAE change)
* Best-performing configuration summary (S2 final; A4 demand-only bound)

---

## Key Results (frozen)

| Metric | S2 (final) | S1 (reference) |
| --- | ---: | ---: |
| Test demand MAE (MW) | **88.65** | 93.31 |
| Test demand R² | **0.684** | 0.674 |
| Test stress R² | **0.745** | 0.585 |
| S2 vs S1 p-value | 5.5×10⁻⁵ | — |
| S2 vs S1 ΔMAE | −4.66 MW (−5.0%) | — |

---

## Deliverables

| File | Purpose |
| --- | --- |
| `publication_tables.md` | All publication tables with frozen numbers |
| `publication_figures.md` | Figure catalogue, captions, provenance |
| `statistical_summary.md` | Inferential statistics for Results section |
| `manuscript_assets_inventory.md` | Master index for Overleaf export |

---

## Definition of Done

✔ Publication tables finalized  
✔ Publication figures finalized  
✔ Statistical summary finalized  
✔ Asset inventory completed  

**Ready for manuscript outlining.**

---

## Constraints observed

- No experiments rerun
- No modification to files under `experiments/` result CSVs, JSON, checkpoints, or figure outputs
- Only documentation and publication packaging in `paper/final_results_package/`

---

## Regeneration

To rebuild Figures 1–5 only:

```bash
python paper/final_results_package/build_publication_assets.py
```

Figures 6–9 are frozen Exp04 copies and must not be regenerated without rerunning Experiment 04.
