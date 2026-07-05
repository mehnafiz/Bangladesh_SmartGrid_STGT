# Appendix A. Supplementary Materials

This appendix consolidates technical material supporting the main manuscript. All entries reference artefacts locked under publication freeze `publication-freeze-2026-06-25` (git commit `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa`). Numeric values in tables below are copied from frozen CSV/JSON outputs; no experiments were rerun for this document.

---

## A.1 Complete benchmark tables

### A.1.1 External benchmark comparison (test set)

Macro demand metrics are averaged over nine administrative divisions. **S2** is the final proposed model (Experiment 03, variant A6); **B07** is the historical PF-STGT W20 hybrid reference (S1). Stress columns apply only to models that emit graph-level OSI forecasts.

| ID | Model | Demand MAE (MW) | Demand RMSE (MW) | Demand MAPE (%) | Demand R² | Stress MAE | Stress R² |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **S2** | Correlation-Only PF-STGT (final) | 88.65 | 127.29 | 6.55 | 0.684 | 0.0371 | 0.745 |
| B07 | PF-STGT W20 hybrid (S1 ref.) | 93.31 | 128.81 | 6.76 | 0.674 | 0.0499 | 0.585 |
| B02 | Random Forest | 97.03 | 156.99 | 7.04 | 0.984 | 0.0481 | 0.555 |
| B03 | XGBoost | 109.73 | 178.53 | 7.99 | 0.979 | 0.0497 | 0.525 |
| B01 | Linear Regression | 247.79 | 597.01 | 17.32 | 0.770 | 0.1074 | −1.824 |
| B04 | LSTM | 237.03 | 278.67 | 14.35 | −0.242 | 0.0861 | −0.191 |
| B05 | GRU | 233.48 | 274.39 | 14.13 | −0.201 | 0.0863 | −0.214 |
| B06 | T-GCN | 257.21 | 301.06 | 15.72 | −0.483 | 0.0891 | −0.304 |

**Source:** `experiments/experiment_02_benchmark_models/benchmark_results.csv` (B01–B07); `experiments/experiment_03_ablation_studies/ablation_results.csv` (S2 = A6).

### A.1.2 Ablation study (test set)

Reference configuration **A1** = S1 (hybrid graph, multi-task W20). **A6 = S2** (final architecture).

| ID | Variant | Graph | Multi-task | Demand MAE (MW) | Demand R² | Stress MAE | Stress R² |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| A4 | Single-Task | hybrid | No | 86.89 | 0.731 | — | — |
| **A6** | **Correlation Graph Only (S2)** | corr | Yes | **88.65** | **0.684** | **0.0371** | **0.745** |
| A3 | No Transformer | hybrid | Yes | 92.64 | 0.671 | 0.0405 | 0.701 |
| A1 | PF-STGT W20 (S1 ref.) | hybrid | Yes | 93.31 | 0.674 | 0.0499 | 0.585 |
| A2 | No Graph | hybrid | Yes | 93.93 | 0.701 | 0.0405 | 0.701 |
| A5 | Geographical Graph Only | geo | Yes | 97.98 | 0.554 | 0.0340 | 0.764 |

**Source:** `experiments/experiment_03_ablation_studies/ablation_results.csv`, `ablation_raw.json`.

### A.1.3 Architecture simplification (test set)

| ID | Model | Graph | Transformer | Demand MAE (MW) | Demand R² | Stress R² | Active params |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| **S2** | Correlation-Only PF-STGT | corr | Yes | 88.65 | 0.684 | 0.745 | 749,058 |
| S3 | No-Transformer PF-STGT | hybrid | No | 92.64 | 0.671 | 0.701 | 451,202 |
| S1 | PF-STGT W20 (ref.) | hybrid | Yes | 93.31 | 0.674 | 0.585 | 749,058 |
| S4 | Corr + No-Transformer | corr | No | 114.63 | 0.362 | 0.747 | 451,202 |

**Source:** `experiments/experiment_03B_architecture_simplification/simplification_results.csv`.

### A.1.4 Per-region demand MAE — S2 (test set)

Per-division MAE for the final model is available in the frozen ablation record. Per-division R² for S2 is **not** tabulated in the frozen repository (macro demand R² only).

| Region | S2 demand MAE (MW) |
| --- | ---: |
| Barishal | 32.73 |
| Chattogram | 76.52 |
| Cumilla | 75.92 |
| Dhaka | 293.98 |
| Khulna | 88.62 |
| Mymensingh | 59.22 |
| Rajshahi | 76.25 |
| Rangpur | 53.97 |
| Sylhet | 40.62 |

**Source:** `experiments/experiment_03_ablation_studies/ablation_raw.json` (variant A6, `per_region_mae`).

### A.1.5 Per-region verification — B07 and B02 (test set)

Division-level MAE and R² for the historical hybrid reference (B07) and random forest (B02) were recomputed in Experiment 02A.

| Region | B07 MAE (MW) | B07 R² | B02 MAE (MW) | B02 R² |
| --- | ---: | ---: | ---: | ---: |
| Barishal | 30.85 | 0.4808 | 32.07 | 0.6936 |
| Chattogram | 75.04 | 0.6362 | 79.97 | 0.5941 |
| Cumilla | 71.83 | 0.7930 | 73.63 | 0.7688 |
| Dhaka | 299.78 | 0.5744 | 311.59 | 0.6666 |
| Khulna | 118.72 | 0.7353 | 92.06 | 0.7835 |
| Mymensingh | 58.74 | 0.7584 | 85.85 | 0.6126 |
| Rajshahi | 85.70 | 0.8270 | 83.13 | 0.8274 |
| Rangpur | 59.77 | 0.6928 | 68.41 | 0.6264 |
| Sylhet | 39.35 | 0.5707 | 46.54 | 0.6171 |

**Source:** `experiments/experiment_02A_classical_benchmark_verification/aggregation_audit.md`.

**Unavailable in frozen repository:** Per-region demand MAE and R² tables for B01, B04, B05, and B06; per-region R² for S2; materialised per-window prediction arrays for S2 (Experiment 02A stores predictions for B07, B02, and B03 only).

---

## A.2 Additional statistical summaries

### A.2.1 Benchmark Wilcoxon tests (demand MAE)

Paired Wilcoxon signed-rank tests \cite{Wilcoxon1945SignedRank} on per-window macro demand MAE (test set, n = 264). Reference model: **B07 (S1)**. Bonferroni-adjusted \cite{Dunn1961Bonferroni} α = 0.0083 (six comparisons).

| Comparison | Median ΔMAE (MW) | p (two-sided) | Cohen's d | Bonferroni sig. | Bootstrap 95% CI |
| --- | ---: | ---: | ---: | --- | --- |
| B07 vs B01 | −58.98 | 1.72×10⁻³¹ | −0.491 | Yes | [−193.11, −120.58] |
| B07 vs B02 | −4.92 | 0.00135 | −0.077 | Yes | [−8.87, 2.62] |
| B07 vs B03 | −14.13 | 6.68×10⁻¹² | −0.298 | Yes | [−22.76, −9.55] |
| B07 vs B04 | −134.42 | 2.33×10⁻³⁹ | −1.224 | Yes | [−158.49, −129.48] |
| B07 vs B05 | −128.94 | 1.92×10⁻³⁹ | −1.219 | Yes | [−154.54, −126.62] |
| B07 vs B06 | −160.66 | 1.48×10⁻⁴⁰ | −1.296 | Yes | [−179.85, −148.85] |

**Source:** `experiments/experiment_02_benchmark_models/statistical_significance.md`.

### A.2.2 Ablation Wilcoxon tests (demand MAE)

Paired Wilcoxon signed-rank tests \cite{Wilcoxon1945SignedRank} vs reference **A1**. Bonferroni-adjusted \cite{Dunn1961Bonferroni} α = 0.01 (five comparisons).

| Comparison | Median ΔMAE (MW) | p (two-sided) | Bonferroni sig. (worse) | Bootstrap 95% CI |
| --- | ---: | ---: | --- | --- |
| A1 vs A6 (S2) | −5.43 | 5.5×10⁻⁵ | No (A6 better) | [−7.17, −2.16] |
| A1 vs A4 | −5.25 | 0.00284 | No (A4 better demand) | [−10.63, −2.40] |
| A1 vs A5 | +3.85 | 1.48×10⁻⁴ | Yes (A5 worse demand) | [2.19, 6.90] |
| A1 vs A2 | +2.81 | 0.301 | No | [−3.69, 4.93] |
| A1 vs A3 | −1.13 | 0.384 | No | [−2.35, 1.08] |

**Source:** `experiments/experiment_03_ablation_studies/statistical_significance.md`.

### A.2.3 S2 vs S1 and R² aggregation note

| Item | Value / note | Source |
| --- | --- | --- |
| S2 vs S1 (A6 vs A1) | Median ΔMAE = −5.43 MW; p = 5.5×10⁻⁵; bootstrap 95% CI [−7.17, −2.16] | Exp03 statistical summary |
| B02/B03 reported R² in Exp02 | Equals **pooled** R², not macro R² | `aggregation_audit.md` |
| B07 reported R² | Equals **macro** R² (mean of nine per-region R²) | `metric_verification.md` |
| Unified macro R² (recomputed) | B02: 0.6878; B07: 0.6743; B03: 0.5902 | Exp02A |

**Unavailable in frozen repository:** Paired Wilcoxon test of S2 vs B02 (random forest); Wilcoxon tests, bootstrap confidence intervals, or Bonferroni-corrected hypothesis tests on OSI MAE or OSI R²; pooled signed-residual statistics or residual time-series store for S2; temporal error-segmentation outputs defined in the Phase 14 error-analysis protocol.

---

## A.3 Hyperparameter configuration

Frozen training configuration for the final model (S2 = A6, seed 42). Authority: Experiment 01B W20 repair protocol and A6 checkpoint config.

| Setting | Value |
| --- | --- |
| Architecture | `PFSTGT` + `GraphVariant.CORR` (τ = 0.65) |
| Tasks | Multi-task: regional demand + graph-level OSI |
| Loss | L = Huber(demand)/100 + λ₂ · MSE(OSI) |
| λ₂ (stress weight) | 20.0 |
| Optimiser | Adam, lr = 5×10⁻⁴, weight decay = 10⁻⁴ |
| Batch size | 32 |
| Max epochs | 200 (early stopping ~epoch 69 for A6) |
| Early stopping | Patience 15; score = 0.7·(val_demand_MAE/100) + 0.3·val_stress_MAE |
| Scheduler | ReduceLROnPlateau on validation demand MAE; factor 0.5, patience 5 |
| Gradient clipping | Max norm 1.0 |
| Seed | 42 |
| Parameters | 749,058 |
| S2 checkpoint | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| S1 reference checkpoint | `experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt` |

**Supporting documents:** `experiments/experiment_01B_multitask_optimization_repair/best_configuration.md`, `experiments/architecture_freeze_revision/final_model_specification.md`.

**Unavailable in frozen repository:** Multi-seed training sweeps (single seed 42 only); forecast uncertainty or probabilistic head configuration.

---

## A.4 Feature dictionary

### A.4.1 Model input tensors

| Tensor | Shape (per batch) | Channels | Description |
| --- | --- | ---: | --- |
| Node features | (T=7, N=9, F_n=9) | 9 per division | Contemporaneous demand/supply/load; lags and rolling mean; regional share and load intensity |
| Global features | (T=7, F_g=17) | 17 | Calendar/trend; grid aggregates; limitation stack; weather; generation scalars; shedding indicator |

**Leakage policy:** Same-day OSI(t) is excluded from model inputs when forecasting OSI(t+1). The engineered stress composite used in target construction is withheld from the global input tensor at inference.

### A.4.2 Node-level channels (F_n = 9 per division)

| Channel group | Contents |
| --- | --- |
| Power balance (contemporaneous) | Processed evening-peak demand, supply, and load (MW-scale, standardised) |
| Autoregressive temporal | Demand lag (1 obs.), demand lag (7 obs.), load lag (1 obs.), 7-observation demand rolling mean |
| Regional derived | Division demand share; load intensity (load / max(demand, ε)) |

### A.4.3 Global-level channels (F_g = 17)

| Channel group | Contents |
| --- | --- |
| Calendar and trend | Day-of-year sin/cos, monotonic trend index, inter-observation gap days, holiday-category ordinal |
| Grid aggregates | Total regional demand, total regional load, generation reserve |
| Operational | Total operational limitation (aggregated), any-division shedding indicator (binary) |
| Weather | Temperature anomaly (month-relative, train-fitted means) |
| Limitation stack | Gas, coal, water, and maintenance limitation scalars (preprocessed) |
| National generation | Two preprocessed generation-endpoint scalars |

### A.4.4 Coalition grouping (explainability)

Eleven coalitions support grouped attribution in Experiment 04:

| ID | Coalition name | Scope | Primary contents |
| --- | --- | --- | --- |
| G1 | regional_demand_block | Node | Contemporaneous division demand |
| G2 | regional_supply_block | Node | Contemporaneous division supply |
| G3 | regional_load_block | Node | Contemporaneous division load |
| G4 | engineered_lags_rolling | Node | Demand lags and rolling mean |
| G5 | regional_share_intensity | Node | Demand share and load intensity |
| G6 | calendar_trend | Global | Cyclical calendar, trend, gap, holiday summary |
| G7 | grid_aggregates | Global | Total demand, total load, generation reserve |
| G8 | limitation_stack | Global | Fuel, infrastructure, maintenance limitations |
| G9 | weather_anomaly | Global | Temperature anomaly |
| G10 | national_generation_scalars | Global | Generation-endpoint scalars |
| G11 | shedding_indicator | Global | Binary any-division shedding flag |

**Design registry:** `results/phases/phase_05A_feature_blueprint/feature_inventory.csv` (Phase 05A blueprint; implementation matches Section 6.4 of the manuscript).

**Unavailable in frozen repository:** A standalone column-name manifest exported from `data/features/*_features.parquet` is not included as a separate supplementary CSV; feature columns are defined in Section 6.4 and the coalition table above.

---

## A.5 Graph construction details

### A.5.1 Final model — correlation graph (S2)

| Property | Value |
| --- | --- |
| Construction rule | Undirected edge (i,j) retained when train-split Pearson ρ_ij ≥ τ on regional evening-peak demand |
| Threshold τ | 0.65 |
| Train rows for ρ | 1,295 daily records (training partition only) |
| Retained pairs | 33 of 36 undirected pairs (91.7% density) |
| Edge weight | w_ij = ρ_ij (zero diagonal; no self-loops) |
| Normalisation | Row-normalised adjacency A (outgoing weights sum to unity) |
| Temporal behaviour | Static: estimated once from training data; fixed for validation and test |
| Runtime variant | `GraphVariant.CORR` in `src/models/pf_stgt.py` |

**Attention bias:** Derived deterministically from A (log-scaled positive entries; masked absent edges) for additive spatial masking in the graph-transformer branch.

### A.5.2 Alternative graphs evaluated in ablations

| Variant | Rule | Undirected edges | Density | Notes |
| --- | --- | ---: | ---: | --- |
| Geographical | Border-adjacent divisions; uniform binary weights, row-normalised | 21 | 58.3% | Frozen geographic prior in `graphs/adjacency_matrix.csv` (MD5-locked) |
| Hybrid (S1) | Edge if geographic neighbour **or** ρ_ij ≥ 0.85; weight = ρ_ij | 24 | 66.7% | Historical reference graph for A1/B07 |
| Correlation (S2) | Edge if ρ_ij ≥ 0.65; weight = ρ_ij | 33 | 91.7% | Selected final prior |

**Design-phase report:** `graphs/graph_construction_report.md` documents the hybrid-graph design rationale (Phase 08); the publication freeze selects correlation-only adjacency for S2 per `experiments/architecture_freeze_revision/Final_Architecture_Decision.md`.

**Unavailable in frozen repository:** A persisted CSV of the full correlation adjacency matrix (built at runtime from training demand series); dynamic or rolling-window graph variants.

---

## A.6 Additional explainability outputs

Experiment 04 post-hoc analysis on frozen S2 checkpoint (`A6/seed_42/best.pt`).

### A.6.1 Summary reports

| Report | Path |
| --- | --- |
| XAI summary | `experiments/experiment_04_explainability_analysis/xai_summary.md` |
| SHAP summary | `experiments/experiment_04_explainability_analysis/shap_summary.md` |
| Permutation importance | `experiments/experiment_04_explainability_analysis/feature_importance.md` |
| Node attribution | `experiments/experiment_04_explainability_analysis/node_attribution.md` |
| Temporal attribution | `experiments/experiment_04_explainability_analysis/temporal_attribution.md` |
| Stress dual-path attribution | `experiments/experiment_04_explainability_analysis/stress_attribution.md` |
| Case studies (24 dates) | `experiments/experiment_04_explainability_analysis/case_studies.md` |
| Machine-readable metrics | `experiments/experiment_04_explainability_analysis/xai_metrics.json` |

### A.6.2 Tabular and figure artefacts

| Label | Content | Path |
| --- | --- | --- |
| Table S2 | Global grouped SHAP (stress) | `results/explainability/shap/global_stress.csv` |
| Table S2 | Global grouped SHAP (Dhaka demand) | `results/explainability/shap/global_demand_dhaka.csv` |
| Table S3 | Permutation ΔMAE (demand) | `results/explainability/permutation/demand_importance.csv` |
| Table S3 | Permutation Δ (stress) | `results/explainability/permutation/stress_importance.csv` |
| Table S4 | Case-study records | `results/explainability/case_studies/<date>/` (24 date folders) |
| Figure S1 | Signed stress SHAP bar | `experiments/experiment_04_explainability_analysis/figures/figure_shap_bar_stress.png` |
| Figures 3–9 | Manuscript explainability figures | `manuscript/overleaf/figures/` (copies from Exp04) |

### A.6.3 Cross-method headline metrics (S2)

| Metric | Value |
| --- | ---: |
| Attention–adjacency Spearman ρ | 0.422 |
| SHAP–permutation Spearman (demand) | −0.564 |
| SHAP–permutation Spearman (stress) | 0.366 |
| OSI driver agreement (case studies) | 52.2% (13/24) |
| Global demand SHAP sample | n = 20 validation windows |
| Case-study dates on test split | 4 of 24 |

**Unavailable in frozen repository:** Independent Captum attribution export separate from the integrated-gradient SHAP-style pipeline; prospective operator-in-the-loop evaluation records; explainability outputs for ablation variants other than S2.

---

## A.7 Reproducibility checklist

### A.7.1 Freeze metadata

| Item | Value |
| --- | --- |
| Freeze date | 2026-06-25 |
| Designated tag | `publication-freeze-2026-06-25` |
| Git commit (freeze HEAD) | `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa` |
| Final model ID | S2 — Correlation-Aware Multi-Task Forecasting Framework |
| Freeze authority | `paper/publication_freeze/Publication_Asset_Freeze.md` |

### A.7.2 MD5-locked data artefacts

| File | MD5 |
| --- | --- |
| `data/interim/bangladesh_smartgrid_clean.parquet` | `4255024d735a91a4b53b2edee203d0ca` |
| `data/features/train_features.parquet` | `b8b3bda95d0fd6cc65f4910d85a98e16` |
| `graphs/adjacency_matrix.csv` | `dacb7ac3a827d00a4b61ea9400e75686` |

### A.7.3 Chronological split policy

| Split | Date range | Valid windows (T = 7) |
| --- | --- | ---: |
| Train | 2019-11-21 → 2023-06-15 | 1,281 |
| Validation | 2023-06-16 → 2024-03-19 | 263 |
| Test | 2024-03-20 → 2024-12-30 | 264 |

Model selection on validation only; test partition held out until final evaluation. Warm-up skip: seven rows per split.

### A.7.4 Experiment completeness (frozen)

| Experiment | Primary artefact | Status |
| --- | --- | --- |
| 01 / 01A / 01B | W20 protocol + S1 checkpoint | Complete |
| 02 | `benchmark_results.csv` | Complete |
| 02A | Verification reports + B07/B02/B03 predictions | Complete |
| 03 | `ablation_results.csv` + A6 checkpoint | Complete |
| 03A / 03B | Investigation reports + simplification CSV | Complete |
| 04 | `xai_metrics.json` + figures + CSV tree | Complete |

### A.7.5 Artefacts not included in the frozen repository

The following items referenced in the manuscript or design documentation are **not** present as executed outputs in the frozen record:

1. Per-region demand R² table for S2.
2. Pooled signed-residual diagnostics, residual histograms, or residual time-series store for S2.
3. Materialised per-window prediction arrays for S2 (B07/B02/B03 only in Exp02A).
4. OSI-specific Wilcoxon tests, bootstrap intervals, or multiple-comparison correction on stress metrics.
5. Direct paired inferential test of S2 vs random forest (B02).
6. Temporal error-segmentation bins or monthly residual profiles for S2 (Phase 14 protocol defined but not executed for the final checkpoint).
7. Forecast prediction intervals, ensemble spread, or conformal uncertainty bounds.
8. Persisted correlation-adjacency matrix file (runtime construction from training demand).
9. Multi-seed result tables (seed 42 only).
10. Field deployment, shadow-mode, or operator-in-the-loop trial records.

Reproduction of reported results should use the checkpoint, data MD5 hashes, split policy, and experiment scripts referenced in `paper/publication_freeze/frozen_results_inventory.md` without modifying frozen CSV, JSON, or figure artefacts.
