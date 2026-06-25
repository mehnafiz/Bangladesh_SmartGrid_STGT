# Evaluation Decision Report — Phase 15

Generated: 2026-06-24

## Design rationale

### Unified evaluation (Phases 10–14 → 15)

Phase 15 consolidates disparate design artefacts into one execution-ready framework.
Each dimension maps to a research gap from Phase 07C:

| Dimension | Gap | Evidence type |
| --- | --- | --- |
| D2 Benchmark | GAP-04, GAP-08 | Table 1, Fig 1–2 |
| D3 Ablation | GAP-02, GAP-04, GAP-05 | Table 2 |
| D4 Explainability | GAP-05, GAP-06 | Fig 3–5, Table S2 |
| D5 Robustness | GAP-06 | Table S3, Fig S1–S2 |
| D6 Statistics | GAP-08 | Table 4 |

### Benchmark evaluation (D2)

Seven frozen models (Phase 10) with fair T=7, h=1 protocol.
Primary claim: B07 beats B06 (graph-temporal) on macro MAE with significance.
Deep models report mean ± std over 3 seeds.

### Ablation evaluation (D3)

Six core variants vs A1 (Phase 13). Component contributions quantified as
ΔMAE with Bonferroni-corrected Wilcoxon tests. A5-CORR supplementary only.

### Explainability evaluation (D4)

Phase 12 hybrid XAI evaluated on quality gates, not accuracy:
SHAP stability, attention–adjacency alignment, permutation concordance,
stress driver agreement. Figures 3–5 are the manuscript interpretability evidence.

### Robustness evaluation (D5)

Phase 14 error taxonomy segments reused: extreme events (E4), high stress (E3),
regional variability (E2), temporal (E5). Test-period shedding density (~63%)
makes robustness evaluation operationally critical for Bangladesh context.

### Statistical significance (D6)

Wilcoxon on daily macro MAE (~278 pairs) with Bonferroni:
- Benchmark: 6 comparisons, α_adj = 0.0083
- Ablation: 5 comparisons, α_adj = 0.0100
Bootstrap 95% CI and Cohen's d mandatory companions to p-values.

## Claim verification matrix (post-training)

| # | Claim | Primary evidence | Pass criterion |
| --- | --- | --- | --- |
| C1 | PF-STGT best demand forecaster | Table 1 | B07 rank 1 macro MAE |
| C2 | Graph-temporal beats T-GCN | Table 1, 4 | B07 < B06, p_adj < α |
| C3 | Multi-task stress viable | Table 3 | B07 OSI MAE < persistence |
| C4 | Graph module contributes | Table 2 | A2 ΔMAE > 0 significant |
| C5 | Transformer contributes | Table 2 | A3 ΔMAE > 0 significant |
| C6 | Multi-task helps demand | Table 2 | A4 ΔMAE ≥ 0 or stress N/A |
| C7 | Hybrid graph optimal | Table 2 | A5-GEO ΔMAE > 0 |
| C8 | XAI quality acceptable | Table S2 | All 4 gates pass |
| C9 | Robust under extremes | Table S3 | Event ratio < 1.5× |
| C10 | Results statistically valid | Table 4 | Corrected p-values reported |

## Dependency chain

```
Phase 10/11 Training → Phase 13 Ablations → Phase 12 XAI → Phase 14 Errors → Phase 15 Tables/Figures
```

## Benchmark registry

| benchmark_id   | model_name        | family              | tasks         |
|:---------------|:------------------|:--------------------|:--------------|
| B01            | Linear Regression | Classical ML        | demand        |
| B02            | Random Forest     | Classical ML        | demand        |
| B03            | XGBoost           | Classical ML        | demand        |
| B04            | LSTM              | Deep Learning       | demand        |
| B05            | GRU               | Deep Learning       | demand        |
| B06            | T-GCN             | Spatio-Temporal GNN | demand        |
| B07            | PF-STGT           | Proposed            | demand;stress |
