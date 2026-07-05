# Publication Tables — Stage 05B Final Results Package

**Generated:** 2026-06-16  
**Source:** Frozen experimental outputs (publication freeze 2026-06-25)  
**Final model:** S2 — Correlation-Only PF-STGT (A6, seed 42)

All numeric values are copied from frozen CSV/JSON artefacts. No experiments were rerun.

---

## Table 1 — Dataset Summary

| Property | Value |
| --- | --- |
| **Domain** | Bangladesh national power grid (9 administrative divisions) |
| **Timeline source** | `data/interim/bangladesh_smartgrid_clean.parquet` |
| **Feature store** | `data/features/*_features.parquet` |
| **Regions (N=9)** | Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet |
| **Input window (T)** | 7 days |
| **Forecast horizon** | 1 day (next-day prediction) |
| **Node features per region** | 9 |
| **Global features** | 17 |
| **Warm-up skip** | 7 rows per split |

### Chronological splits

| Split | Date range | Raw rows | Valid windows (T=7) |
| --- | --- | --- | --- |
| Train | 2019-11-21 → 2023-06-15 | 1,295 | **1,281** |
| Validation | 2023-06-16 → 2024-03-19 | 277 | **263** |
| Test | 2024-03-20 → 2024-12-30 | 278 | **264** |

### MD5-locked artefacts

| File | MD5 |
| --- | --- |
| `data/interim/bangladesh_smartgrid_clean.parquet` | `4255024d735a91a4b53b2edee203d0ca` |
| `data/features/train_features.parquet` | `b8b3bda95d0fd6cc65f4910d85a98e16` |
| `graphs/adjacency_matrix.csv` | `dacb7ac3a827d00a4b61ea9400e75686` |

**Primary evaluation split:** Test (264 windows). Model selection on validation only.

---

## Table 2 — Training Configuration (S2 / A6 frozen)

| Setting | Value |
| --- | --- |
| **Architecture** | `PFSTGT` + `GraphVariant.CORR` (τ = 0.65) |
| **Tasks** | Multi-task: regional demand + graph-level OSI |
| **Loss** | `L = Huber(demand)/100 + λ₂ · MSE(OSI)` |
| **Demand loss scaling** | Huber demand term ÷ 100 MW |
| **λ₂ (stress weight)** | 20.0 |
| **Optimiser** | Adam, lr = 5×10⁻⁴, weight decay = 10⁻⁴ |
| **Batch size** | 32 |
| **Max epochs** | 200 |
| **Early stopping** | Patience 15; score = 0.7·(val_demand_MAE/100) + 0.3·val_stress_MAE |
| **Scheduler** | ReduceLROnPlateau on validation demand MAE; factor 0.5, patience 5 |
| **Gradient clipping** | Max norm 1.0 |
| **Seed** | 42 |
| **Parameters** | 749,058 (all active) |
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **Training time (ref.)** | ~393 s |

---

## Table 3 — Benchmark Comparison (test set)

Macro demand metrics over 9 regions. **S2** is the final proposed model; **B07** is the historical S1 reference (PF-STGT W20 hybrid).

| ID | Model | Demand MAE (MW) | Demand RMSE (MW) | Demand MAPE (%) | Demand R² | Stress MAE | Stress R² |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **S2 ★** | **Correlation-Only PF-STGT (final)** | **88.65** | **127.29** | **6.55** | **0.684** | **0.0371** | **0.745** |
| B07 | PF-STGT W20 hybrid (S1 ref.) | 93.31 | 128.81 | 6.76 | 0.674 | 0.0499 | 0.585 |
| B02 | Random Forest | 97.03 | 156.99 | 7.04 | 0.984 | 0.0481 | 0.555 |
| B03 | XGBoost | 109.73 | 178.53 | 7.99 | 0.979 | 0.0497 | 0.525 |
| B01 | Linear Regression | 247.79 | 597.01 | 17.32 | 0.770 | 0.1074 | −1.824 |
| B04 | LSTM | 237.03 | 278.67 | 14.35 | −0.242 | 0.0861 | −0.191 |
| B05 | GRU | 233.48 | 274.39 | 14.13 | −0.201 | 0.0863 | −0.214 |
| B06 | T-GCN | 257.21 | 301.06 | 15.72 | −0.483 | 0.0891 | −0.304 |

**Source:** `experiments/experiment_02_benchmark_models/benchmark_results.csv` (B01–B07); S2 from `experiments/experiment_03_ablation_studies/ablation_results.csv` (A6).

---

## Table 4 — Benchmark Statistical Significance

Wilcoxon signed-rank test on per-sample macro demand MAE (test set, n=264). Reference: **B07 (S1)**. Bonferroni-adjusted α = 0.0083 (6 comparisons).

| Comparison | Median ΔMAE (MW) | p (two-sided) | p (B07 better) | Cohen's d | Bonferroni sig. | Bootstrap 95% CI |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| B07 vs B01 | −58.98 | 1.72×10⁻³¹ | 8.62×10⁻³² | −0.491 | Yes | [−193.11, −120.58] |
| B07 vs B02 | −4.92 | 0.00135 | 0.000677 | −0.077 | Yes | [−8.87, 2.62] |
| B07 vs B03 | −14.13 | 6.68×10⁻¹² | 3.34×10⁻¹² | −0.298 | Yes | [−22.76, −9.55] |
| B07 vs B04 | −134.42 | 2.33×10⁻³⁹ | 1.16×10⁻³⁹ | −1.224 | Yes | [−158.49, −129.48] |
| B07 vs B05 | −128.94 | 1.92×10⁻³⁹ | 9.62×10⁻⁴⁰ | −1.219 | Yes | [−154.54, −126.62] |
| B07 vs B06 | −160.66 | 1.48×10⁻⁴⁰ | 7.42×10⁻⁴¹ | −1.296 | Yes | [−179.85, −148.85] |

**S2 vs S1 (A6 vs A1):** median ΔMAE = −5.43 MW, p = 5.5×10⁻⁵, bootstrap 95% CI [−7.17, −2.16] (see Table 5 / statistical summary).

**Source:** `experiments/experiment_02_benchmark_models/statistical_significance.md`

---

## Table 5 — Ablation Study Results (test set)

Reference ablation: **A1** (S1, hybrid graph, multi-task). **A6 = S2** (final architecture).

| ID | Variant | Graph | Multi-task | Demand MAE (MW) | Demand R² | Stress MAE | Stress R² |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| A4 | Single-Task | hybrid | No | **86.89** | **0.731** | — | — |
| **A6 ★** | **Correlation Graph Only (S2)** | **corr** | **Yes** | **88.65** | **0.684** | **0.0371** | **0.745** |
| A3 | No Transformer | hybrid | Yes | 92.64 | 0.671 | 0.0405 | 0.701 |
| A1 | PF-STGT W20 (S1 ref.) | hybrid | Yes | 93.31 | 0.674 | 0.0499 | 0.585 |
| A2 | No Graph | hybrid | Yes | 93.93 | 0.701 | 0.0405 | 0.701 |
| A5 | Geographical Graph Only | geo | Yes | 97.98 | 0.554 | 0.0340 | 0.764 |

### Wilcoxon vs A1 (Bonferroni α = 0.01)

| Comparison | Median ΔMAE (MW) | p (two-sided) | Bonferroni sig. (worse) | Bootstrap 95% CI |
| --- | ---: | ---: | --- | --- |
| A1 vs A6 (S2) | −5.43 | 5.5×10⁻⁵ | No (A6 better) | [−7.17, −2.16] |
| A1 vs A4 | −5.25 | 0.00284 | No (A4 better demand) | [−10.63, −2.40] |
| A1 vs A5 | +3.85 | 1.48×10⁻⁴ | **Yes** (A5 worse demand) | [2.19, 6.90] |
| A1 vs A2 | +2.81 | 0.301 | No | [−3.69, 4.93] |
| A1 vs A3 | −1.13 | 0.384 | No | [−2.35, 1.08] |

**Source:** `experiments/experiment_03_ablation_studies/ablation_results.csv`, `statistical_significance.md`

---

## Table 6 — Architecture Comparison (S1–S4, test set)

Experiment 03B simplification study. **S2 selected** as final production architecture.

| ID | Model | Graph | Transformer | Demand MAE (MW) | Demand R² | Stress R² | Active params | Train (s) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| **S2 ★** | **Correlation-Only PF-STGT** | corr | Yes | **88.65** | **0.684** | **0.745** | 749,058 | 393 |
| S3 | No-Transformer PF-STGT | hybrid | No | 92.64 | 0.671 | 0.701 | 451,202 | 367 |
| S1 | PF-STGT W20 (ref.) | hybrid | Yes | 93.31 | 0.674 | 0.585 | 749,058 | 413 |
| S4 | Corr + No-Transformer | corr | No | 114.63 | 0.362 | 0.747 | 451,202 | 309 |

### ΔMAE vs S1

| Variant | ΔMAE (MW) | % change |
| --- | ---: | ---: |
| S2 | **−4.66** | **−5.0%** |
| S3 | −0.66 | −0.7% |
| S4 | +21.32 | +22.9% |

**S1 vs S2 Wilcoxon:** median ΔMAE = −5.43 MW, p = 5.5×10⁻⁵, Bonferroni significant at α = 0.01.

**Source:** `experiments/experiment_03B_architecture_simplification/simplification_results.csv`

---

## Table 7 — Explainability Summary (S2, Experiment 04)

Model: frozen S2 checkpoint (A6/seed_42). Methods: grouped integrated gradients (SHAP), permutation importance, attention export, case studies (n=24).

### Global grouped SHAP — top coalitions

| Task | Rank | Group | Name | \|φ\| |
| --- | ---: | --- | --- | ---: |
| Stress | 1 | G8 | limitation_stack | 0.0191 |
| Stress | 2 | G6 | calendar_trend | 0.0190 |
| Stress | 3 | G7 | grid_aggregates | 0.0087 |
| Demand (Dhaka) | 1 | G6 | calendar_trend | 162.34 |
| Demand (Dhaka) | 2 | G4 | engineered_lags_rolling | 101.26 |
| Demand (Dhaka) | 3 | G10 | national_generation_scalars | 91.44 |

### Cross-method validation

| Metric | Value |
| --- | ---: |
| Attention–adjacency Spearman ρ | 0.422 |
| SHAP–permutation Spearman (demand) | −0.564 |
| SHAP–permutation Spearman (stress) | 0.366 |
| OSI driver agreement (case studies) | 52.2% (13/24) |
| Dominant stress coalition (cases) | G8 (limitation_stack) |
| Dominant demand coalition (Dhaka) | G6, G4 |
| Peak temporal lag | t−6 (near-uniform α_t) |

### Node SHAP mass (Dhaka demand, mean)

| Region | Mass |
| --- | ---: |
| Dhaka | 340.36 |
| Rajshahi | 110.32 |
| Khulna | 108.91 |
| Mymensingh | 93.84 |

**Source:** `experiments/experiment_04_explainability_analysis/xai_metrics.json`, `shap_summary.md`, `case_studies.md`

---

## Overleaf export paths (recommended)

| Table | Suggested file |
| --- | --- |
| Table 1 | `manuscript/overleaf/tables/table_01_dataset.tex` |
| Table 2 | `manuscript/overleaf/tables/table_02_training.tex` |
| Table 3 | `manuscript/overleaf/tables/table_03_benchmarks.tex` |
| Table 4 | `manuscript/overleaf/tables/table_04_benchmark_stats.tex` |
| Table 5 | `manuscript/overleaf/tables/table_05_ablations.tex` |
| Table 6 | `manuscript/overleaf/tables/table_06_architecture.tex` |
| Table 7 | `manuscript/overleaf/tables/table_07_explainability.tex` |
