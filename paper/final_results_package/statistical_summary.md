# Statistical Summary — Stage 05B Final Results Package

**Generated:** 2026-06-16  
**Scope:** Consolidated inferential statistics from frozen Experiments 02, 03, and 03B  
**Primary metric:** Per-sample macro demand MAE (MW) on test set (n=264 windows)

No new statistical tests were computed. All values are transcribed from frozen experiment reports.

---

## 1. Best-performing configuration

| Role | ID | Test demand MAE | Test demand R² | Test stress R² | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| **Final model (multi-task)** | **S2 / A6** | **88.65 MW** | **0.684** | **0.745** | Correlation graph; full transformer trunk |
| Best demand-only ablation | A4 | 86.89 MW | 0.731 | — | Single-task; no stress head |
| Historical reference | S1 / A1 / B07 | 93.31 MW | 0.674 | 0.585 | Hybrid graph PF-STGT W20 |
| Best classical baseline | B02 (RF) | 97.03 MW | 0.984 | 0.555 | Per-region R² inflated vs macro |

**Manuscript recommendation:** Report S2 as the proposed multi-task model. Note A4 as an upper bound on demand-only performance at the cost of stress forecasting capability.

---

## 2. Final model vs reference (S2 vs S1)

| Test | Comparison | Median ΔMAE (MW) | Mean ΔMAE (MW) | p (two-sided) | p (S2 better) | Bootstrap 95% CI | Bonferroni α | Significant? |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| Exp03 ablation | A1 vs A6 | −5.43 | −4.66 | 5.5×10⁻⁵ | ≈1.0 (A6 better) | [−7.17, −2.16] | 0.01 | Yes (A6 better) |
| Exp03B simplification | S1 vs S2 | −5.43 | −4.66 | 5.5×10⁻⁵ | 2.8×10⁻⁵ | [−7.17, −2.16] | 0.01 | Yes (S2 better) |

**Effect size (percent):** −5.0% demand MAE reduction (93.31 → 88.65 MW).

**Stress improvement:** Stress R² 0.585 → 0.745 (+0.160 absolute); stress MAE 0.0499 → 0.0371.

---

## 3. Benchmark significance (B07/S1 vs baselines)

Wilcoxon signed-rank; Bonferroni-adjusted α = 0.0083 (6 pairwise comparisons). Reference: B07 (PF-STGT W20).

| Comparison | Median ΔMAE (MW) | p (two-sided) | Cohen's d | Bootstrap 95% CI | Bonferroni sig. |
| --- | ---: | ---: | ---: | --- | --- |
| B07 vs B02 (RF) | −4.92 | 0.00135 | −0.077 | [−8.87, 2.62] | Yes |
| B07 vs B03 (XGB) | −14.13 | 6.68×10⁻¹² | −0.298 | [−22.76, −9.55] | Yes |
| B07 vs B06 (T-GCN) | −160.66 | 1.48×10⁻⁴⁰ | −1.296 | [−179.85, −148.85] | Yes |
| B07 vs B04 (LSTM) | −134.42 | 2.33×10⁻³⁹ | −1.224 | [−158.49, −129.48] | Yes |
| B07 vs B05 (GRU) | −128.94 | 1.92×10⁻³⁹ | −1.219 | [−154.54, −126.62] | Yes |
| B07 vs B01 (LR) | −58.98 | 1.72×10⁻³¹ | −0.491 | [−193.11, −120.58] | Yes |

**S2 vs B02 (derived, not independently tested):** Point estimate ΔMAE = −8.38 MW (97.03 − 88.65). Formal paired test not run in Exp02 (S2 evaluated in Exp03); use A6 vs A1 and S1 vs S2 Wilcoxon as primary evidence for deep model improvement.

---

## 4. Ablation significance (vs A1 reference)

Bonferroni-adjusted α = 0.01 for 5 comparisons.

| Comparison | Median ΔMAE (MW) | p (two-sided) | Interpretation | Bootstrap 95% CI | Bonferroni sig. (worse) |
| --- | ---: | ---: | --- | --- | --- |
| A1 vs A6 (S2) | −5.43 | 5.5×10⁻⁵ | **A6 improves demand** | [−7.17, −2.16] | No |
| A1 vs A4 | −5.25 | 0.00284 | A4 improves demand (single-task) | [−10.63, −2.40] | No |
| A1 vs A5 | +3.85 | 1.48×10⁻⁴ | A5 degrades demand | [2.19, 6.90] | **Yes** |
| A1 vs A2 | +2.81 | 0.301 | No graph ≈ hybrid | [−3.69, 4.93] | No |
| A1 vs A3 | −1.13 | 0.384 | No transformer ≈ full | [−2.35, 1.08] | No |

**Key ablation conclusions (frozen):**

1. Correlation graph (A6/S2) significantly beats hybrid (A1/S1) on demand.
2. Geographical-only graph (A5) significantly **worse** than hybrid on demand.
3. Removing graph (A2) or transformer (A3) does not significantly change demand MAE.
4. Single-task (A4) yields lowest demand MAE but removes stress forecasting.

---

## 5. Architecture simplification significance (Exp03B)

| Comparison | Median ΔMAE (MW) | p (two-sided) | p (variant better) | Bonferroni sig. (α=0.01) | Bootstrap 95% CI |
| --- | ---: | ---: | ---: | --- | --- |
| S1 vs S2 | −5.43 | 5.5×10⁻⁵ | 2.8×10⁻⁵ | **Yes** | [−7.17, −2.16] |
| S1 vs S3 | −1.13 | 0.384 | 0.192 | No | [−2.36, 1.10] |
| S1 vs S4 | +14.47 | <10⁻⁶ | 1.0 (S4 worse) | No (worse direction) | [16.47, 26.40] |

**Complexity trade-off:** S2 and S1 share 749,058 active parameters; S3/S4 reduce active params to 451,202 (~40%) but S3 is not significantly better than S1 and S4 significantly degrades demand.

---

## 6. Explainability cross-validation metrics (Exp04)

These are descriptive/consistency metrics, not hypothesis tests.

| Metric | Value | Interpretation |
| --- | ---: | --- |
| Attention–adjacency Spearman ρ | 0.422 | Moderate alignment of learned spatial attention with correlation graph |
| SHAP–permutation Spearman (demand) | −0.564 | Methods partially disagree on demand ranking |
| SHAP–permutation Spearman (stress) | 0.366 | Moderate agreement on stress drivers |
| OSI driver agreement (case studies) | 52.2% | SHAP top coalition matches OSI component driver in 13/24 cases |

---

## 7. Confidence intervals summary (primary claims)

| Claim | Point estimate | 95% CI (bootstrap, MAE diff) | p-value |
| --- | --- | --- | --- |
| S2 improves demand vs S1 | −4.66 MW (mean) | [−7.17, −2.16] | 5.5×10⁻⁵ |
| S1 beats RF (B07 vs B02) | −4.92 MW (median) | [−8.87, 2.62] | 0.00135 |
| S1 beats XGB (B07 vs B03) | −14.13 MW (median) | [−22.76, −9.55] | 6.68×10⁻¹² |
| Geo-only graph hurts (A1 vs A5) | +3.85 MW (median) | [2.19, 6.90] | 1.48×10⁻⁴ |
| S4 simplification hurts vs S1 | +21.32 MW (mean) | [16.47, 26.40] | <10⁻⁶ |

---

## 8. Source files

| Experiment | Statistical report |
| --- | --- |
| 02 | `experiments/experiment_02_benchmark_models/statistical_significance.md` |
| 03 | `experiments/experiment_03_ablation_studies/statistical_significance.md` |
| 03B | `experiments/experiment_03B_architecture_simplification/performance_vs_complexity.md` |

---

## 9. Manuscript reporting checklist

- [x] Primary metric defined (macro demand MAE, MW)
- [x] Test set size reported (n=264)
- [x] Multiple-comparison correction documented (Bonferroni)
- [x] Bootstrap CIs available for key comparisons
- [x] Final model (S2) distinguished from historical S1/B07
- [x] Single-task upper bound (A4) noted separately
- [x] Effect sizes reported (Cohen's d for benchmarks; % MAE change for S2)
