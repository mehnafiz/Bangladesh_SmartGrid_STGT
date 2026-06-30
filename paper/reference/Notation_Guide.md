# Notation Guide

**Revised:** 2026-06-30  
**Purpose:** Standard symbols and dimensions for Methods, Results, and tables  
**Authority:** `final_model_specification.md`, `publication_tables.md`, Paper Outline §6.1  
**First use:** Section 6.1 (`06_Methodology.md`)

---

## Index sets and dimensions

| Symbol | Meaning | Frozen value |
| --- | --- | ---: |
| \(N\) | Number of regions (nodes) | 9 |
| \(T\) | Input lookback window (days) | 7 |
| \(H\) | Forecast horizon (days) | 1 |
| \(F_n\) | Node features per region | 9 |
| \(F_g\) | Global features | 17 |
| \(B\) | Batch size | 32 |
| \(\tau\) | Correlation graph threshold | 0.65 |

---

## Input tensors

| Symbol | Shape | Description |
| --- | --- | --- |
| \(\mathbf{X}^{node}\) | \((B, T, N, F_n)\) | Regional node feature tensor |
| \(\mathbf{X}^{global}\) | \((B, T, F_g)\) | National/system context features |
| \(\mathbf{A}\) | \((N, N)\) | Row-normalised adjacency (correlation graph for S2) |
| \(\mathbf{B}^{attn}\) | \((N, N)\) | Optional attention bias from adjacency |

---

## Output tensors

| Symbol | Shape | Range | Task |
| --- | --- | --- | --- |
| \(\hat{\mathbf{y}}^{demand}\) | \((B, N)\) | MW | Task 1 — regional demand |
| \(\hat{y}^{osi}\) | \((B, 1)\) | \([0, 1]\) | Task 2 — operational stress index |
| \(\boldsymbol{\alpha}^{spatial}\) | \((N, N)\) | \([0,1]\) | Spatial attention (explainability) |
| \(\boldsymbol{\alpha}^{temporal}\) | \((T,)\) | \([0,1]\) | Temporal attention weights |
| \(\mathbf{h}^{shared}\) | \((B, N, 128)\) | — | Shared representation |

---

## Graph notation

| Symbol | Meaning |
| --- | --- |
| \(\mathcal{G} = (\mathcal{V}, \mathcal{E})\) | Graph with \(|\mathcal{V}| = N\) regions |
| \(|\mathcal{E}|\) | Undirected edges in S2 correlation graph = **33** |
| \(\rho_{ij}\) | Pearson correlation between regional demand series |
| \(\mathbf{A}^{corr}\) | Correlation graph adjacency (S2) |
| \(\mathbf{A}^{geo}\) | Geographical adjacency from `adjacency_matrix.csv` |
| \(\mathbf{A}^{hybrid}\) | Combined geo + corr adjacency (S1) |

---

## Loss and training notation

| Symbol | Meaning | S2 value |
| --- | --- | ---: |
| \(\mathcal{L}_{demand}\) | Huber loss on demand (normalised ÷100 in total loss) | — |
| \(\mathcal{L}_{osi}\) | MSE on OSI | — |
| \(\lambda_2\) | Stress task weight | **20.0** |
| \(\mathcal{L}\) | \(\mathcal{L}_{demand}/100 + \lambda_2 \cdot \mathcal{L}_{osi}\) | W20 protocol |
| \(\eta\) | Learning rate | \(5 \times 10^{-4}\) |
| \(\lambda_{wd}\) | Weight decay | \(10^{-4}\) |

**Early stopping score:**

\[
s_{val} = 0.7 \cdot \frac{MAE_{demand}^{val}}{100} + 0.3 \cdot MAE_{osi}^{val}
\]

---

## Evaluation metrics

### Task 1 — Demand (macro over regions)

| Metric | Symbol | Primary? | Unit |
| --- | --- | --- | --- |
| Mean Absolute Error | \(MAE\) | **Yes** | MW |
| Root Mean Square Error | \(RMSE\) | Yes | MW |
| Mean Absolute Percentage Error | \(MAPE\) | Yes | % |
| Coefficient of determination | \(R^2\) | Yes (macro) | — |

**Macro aggregation:** Average metric across \(N=9\) regions (not pooled samples).

### Task 2 — Stress (OSI)

| Metric | Symbol | Unit |
| --- | --- | --- |
| MAE | \(MAE_{osi}\) | — |
| RMSE | \(RMSE_{osi}\) | — |
| \(R^2\) | \(R^2_{osi}\) | — |

---

## Statistical testing notation

| Symbol | Meaning | Frozen value |
| --- | --- | --- |
| \(n\) | Test windows | 264 |
| \(W\) | Wilcoxon signed-rank statistic | Per comparison |
| \(p\) | Two-sided p-value | Report with Bonferroni context |
| \(d\) | Cohen's d effect size | Benchmark comparisons |
| \(\Delta MAE\) | Median or mean paired MAE difference | Sign negative if reference worse |
| CI\(_{95\%}\) | Bootstrap confidence interval | B=10000 (frozen reports) |
| \(\alpha_B\) | Bonferroni-adjusted significance level | 0.0083 (Exp02), 0.01 (Exp03) |

---

## Explainability notation

| Symbol | Meaning | Frozen value (S2) |
| --- | --- | ---: |
| \(\phi_g\) | Grouped SHAP value for coalition \(g\) | See Table 7 |
| \(|\phi_g|\) | Absolute grouped SHAP magnitude | — |
| \(\rho_{att,adj}\) | Spearman(attention, adjacency) | 0.422 |
| \(\rho_{SHAP,perm}^{demand}\) | Spearman(SHAP, permutation) demand | −0.564 |
| \(\rho_{SHAP,perm}^{stress}\) | Spearman(SHAP, permutation) stress | 0.366 |
| \(\alpha_t\) | Mean temporal attention at lag \(t\) | Peak at \(t{-}6\) = 0.162 |
| Agreement rate | OSI driver agreement in case studies | 52.2% (13/24) |

**Temporal lag indexing:** \(t{-}0\) = current day in window; \(t{-}6\) = oldest day (7-day window).

---

## Model ID subscripts (results tables)

Use roman labels in tables; avoid overloading math symbols:

| Label | Meaning |
| --- | --- |
| S2, S1, S3, S4 | Architecture simplification variants (Exp03B) |
| A1–A6 | Ablation variants (Exp03) |
| B01–B07 | Benchmark models (Exp02) |

---

## Leakage policy (notation in Methods)

When predicting \(\hat{y}^{osi}_{t+1}\), exclude \(OSI_t\) from input features at time \(t\). Demand lags may include historical demand through \(t\).

---

## Checkpoint path convention

```
experiments/<experiment_dir>/checkpoints/<variant_id>/seed_42/best.pt
```

Canonical S2: `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt`
