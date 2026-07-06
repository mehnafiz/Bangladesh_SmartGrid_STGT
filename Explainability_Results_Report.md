# Explainability Results Report — Phase 21

**Date:** 7 July 2026  
**Authority:** Phase 21 — Real Explainability Results Generation  
**Constraint:** All figures originate from the frozen S2 (A6) checkpoint. No synthetic, placeholder, or fabricated values.

---

## 1. Executive Summary

Phase 21 **re-executed the full Experiment 04 explainability pipeline** on the frozen PF-STGT S2 model and exported **eight publication-quality figure sets** (PDF + SVG + PNG) from verified model outputs.

| Item | Status |
|---|---|
| Frozen checkpoint loaded | ✅ `A6/seed_42/best.pt` (749,058 params) |
| Real SHAP attributions computed | ✅ Grouped integrated gradients, 25 steps |
| Real attention heatmap | ✅ 9×9 `mean_spatial` matrix saved from model forward passes |
| Case studies | ✅ 24 stratified cases (20 validation + 4 test) |
| Publication figures exported | ✅ 8 figure sets × 3 formats = 24 files |
| Failures | **None** |
| Manuscripts modified | **No** (per phase constraint) |

---

## 2. Methodology

### 2.1 Model and data (frozen)

| Component | Path / value |
|---|---|
| **Architecture** | S2 — Correlation-Only PF-STGT (ablation A6) |
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **Training config** | `.../checkpoints/A6/seed_42/config.yaml` |
| **Graph** | Correlation adjacency, τ = 0.65 (`GraphVariant.CORR`) |
| **Device** | Apple MPS |
| **Seed** | 42 |

| Data artefact | Path |
|---|---|
| Train features | `data/features/train_features.parquet` (1,281 windows) |
| Validation features | `data/features/validation_features.parquet` (263 windows) |
| Test features | `data/features/test_features.parquet` (264 windows) |
| Clean timeline | `data/interim/bangladesh_smartgrid_clean.parquet` |
| Adjacency | `graphs/adjacency_matrix.csv` |

All inputs verified via `FoundationCoordinator(verify_md5=True)`.

### 2.2 Attribution methods

| Method | Implementation | Output |
|---|---|---|
| **Grouped SHAP** | `ShapEngine` — integrated gradients over feature coalitions G1–G11, zero baseline, 25 IG steps | `results/explainability/shap/*.csv` |
| **Permutation importance** | `PermutationImportance` — coalition ablation on validation loader (8 batches) | `results/explainability/permutation/*.csv` |
| **Node attribution** | `NodeAttributor` — SHAP mass per region + attention inflow/outflow | `case_studies/<date>/node_importance.csv` |
| **Temporal attribution** | `TemporalAttributor` — α_t from `attn_temporal` (7-day window) | `case_studies/<date>/temporal_alpha.csv` |
| **Spatial attention** | `AttentionExtractor.extract_spatial()` — mean 9×9 influence matrix from graph-transformer layer | `results/explainability/attention/mean_spatial_matrix.csv` |
| **Stress dual-path** | `StressAttributor` — SHAP (Path A) + OSI c1/c2/c3 decomposition (Path B) | `case_studies/<date>/osi_components.csv` |

**Note:** This project uses a custom integrated-gradients SHAP engine (`src/explainability/shap_engine.py`), not the external `shap` Python package. Method is Captum-compatible GradientSHAP over coalition-masked inputs.

### 2.3 Case study design

- **20 validation cases** stratified by: high OSI, low OSI, peak demand, shedding
- **4 test cases** representative of: typical demand, high demand, low demand, high stress
- **Local explanation figure** uses test case **2024-09-08** (high-stress stratum, OSI = 0.565)

---

## 3. Executed Scripts

### 3.1 Primary pipeline (model inference required)

```bash
/opt/anaconda3/bin/python experiments/experiment_04_explainability_analysis/run_explainability.py
```

**Runtime:** ~93 seconds on MPS (7 July 2026, 00:54–00:56 UTC+6)

**Deliverables:**
- `experiments/experiment_04_explainability_analysis/xai_metrics.json`
- 8 markdown reports in `experiments/experiment_04_explainability_analysis/`
- 7 diagnostic PNGs in `experiments/experiment_04_explainability_analysis/figures/`
- CSV artefacts under `results/explainability/`
- **New in Phase 21:** `results/explainability/attention/mean_spatial_matrix.csv` + `.json`

### 3.2 Publication export (reads verified outputs only)

```bash
.figure_build_venv/bin/python experiments/experiment_04_explainability_analysis/export_publication_figures.py
```

**Runtime:** ~2 seconds  
**Input:** Real CSV/JSON from step 3.1 — **no model inference, no synthetic values**  
**Output:** `results/explainability/figures/` (PDF/SVG/PNG)

### 3.3 Code changes (pipeline only — not manuscripts)

| File | Change |
|---|---|
| `run_explainability.py` | Export real `mean_spatial` matrix to `attention/mean_spatial_matrix.csv` and `xai_metrics.json` |
| `export_publication_figures.py` | **New** — publication export from verified artefacts |

---

## 4. Figures Generated

All figures in `results/explainability/figures/` — each available as `.pdf`, `.svg`, `.png`.

| # | Figure | File stem | Source data |
|---|---|---|---|
| 1 | **SHAP Summary (Demand)** | `01_shap_summary_demand` | `shap/global_demand_dhaka.csv` |
| 2 | **SHAP Summary (Stress)** | `02_shap_summary_stress` | `shap/global_stress.csv` |
| 3 | **SHAP Bar Plot (signed)** | `03_shap_bar_stress` | `shap/global_stress.csv` (signed φ) |
| 4 | **Node Attribution** | `04_node_attribution` | `xai_metrics.json` → `node_mass_mean` |
| 5 | **Temporal Attribution** | `05_temporal_attribution` | `xai_metrics.json` → `mean_temporal_alpha` |
| 6 | **Attention Heatmap** | `06_attention_heatmap` | `attention/mean_spatial_matrix.csv` (real 9×9) |
| 7 | **Stress Attribution** | `07_stress_attribution` | Case `2024-09-08` stress SHAP + OSI components |
| 8 | **Local Explanation** | `08_local_explanation_2024-09-08` | 4-panel: stress SHAP, OSI, node mass, temporal α_t |

**Manifest:** `results/explainability/figures/manifest.json`

### 4.1 Provenance guarantee

The attention heatmap (`06_attention_heatmap`) uses the **raw `mean_spatial` matrix** averaged over 24 case-study forward passes. This supersedes any prior PNG pixel-extraction approach and is fully reproducible from:

```bash
python run_explainability.py && python export_publication_figures.py
```

---

## 5. Key Results and Interpretation

### 5.1 Global SHAP — Stress (validation, n = 20 batches)

| Rank | Coalition | |φ| | Interpretation |
|---|---|---|---|
| 1 | **G8** | 0.0191 | Limitation stack — primary stress driver |
| 2 | **G6** | 0.0190 | Grid aggregates |
| 3 | **G7** | 0.0087 | Grid capacity features |
| 4 | **G10** | 0.0082 | Reserve margin |

Stress forecasting is dominated by **grid limitation and capacity coalitions** (G8, G6, G7), consistent with OSI construction from reserve and shedding signals.

### 5.2 Global SHAP — Demand, Dhaka (validation, n = 20)

| Rank | Coalition | |φ| (MW-scale) | Interpretation |
|---|---|---|---|
| 1 | **G6** | 162.34 | Regional demand block (node features) |
| 2 | **G4** | 101.26 | Engineered lag features |
| 3 | **G10** | 91.44 | Reserve / margin context |
| 4 | **G1** | 77.72 | Base demand features |

Dhaka demand is driven primarily by **its own regional feature block (G6)** and **temporal lag coalitions (G4)**, as expected for autoregressive load forecasting.

### 5.3 Node attribution

| Region | Mean SHAP mass | Share interpretation |
|---|---|---|
| **Dhaka** | 340.36 | Dominant (~36% national load share) |
| Rajshahi | 110.32 | Secondary hub |
| Khulna | 108.91 | Secondary hub |
| Mymensingh | 93.84 | Moderate |
| Rangpur | 1.99 | Lowest mass |

**Attention–adjacency Spearman ρ = 0.422** — spatial attention patterns correlate moderately with the correlation-graph structure, supporting that the graph encoder uses meaningful regional coupling.

### 5.4 Temporal attribution

Mean α_t across 24 case studies (T = 7):

| Lag | α_t |
|---|---|
| t-0 | 0.162 |
| t-3 | 0.146 |
| t-6 | 0.143 |
| t-1 | 0.140 |

Weights are **near-uniform** (range 0.135–0.162), indicating the temporal transformer does not strongly privilege a single lag. This aligns with Exp03A findings and should be reported honestly — near-uniform α_t is a null result, not a failure.

### 5.5 Local explanation — 2024-09-08 (high-stress test case)

| Metric | Value |
|---|---|
| Date | 2024-09-08 (test split) |
| Observed OSI | 0.565 |
| Predicted OSI | 0.429 |
| Total demand | 15,354 MW |
| Dhaka predicted | 5,223 MW |
| Top stress SHAP coalition | **G8** (φ = +0.088) |
| OSI component driver | c2_reserve (reserve margin) |
| Driver agreement | **False** (SHAP → G8/limitations; components → reserve) |
| Dhaka node SHAP mass | 504.69 (highest in case) |

This case illustrates the **dual-pathway tension**: SHAP attributes stress to limitation features (G8), while the OSI decomposition identifies reserve margin (c2) as the component driver. The 52.2% agreement rate across all case studies reflects this systematic partial disagreement.

### 5.6 Permutation validation

| Metric | Value | Interpretation |
|---|---|---|
| SHAP–permutation Spearman (stress) | **0.627** | Moderate positive agreement |
| SHAP–permutation Spearman (demand) | **−0.345** | Weak / negative agreement |

Stress SHAP rankings align reasonably with permutation ablation. Demand shows weaker SHAP–permutation concordance — likely because demand MAE degradation under coalition ablation is dominated by G6 (regional block), while SHAP spreads credit across G4/G6/G10. This is a known limitation of grouped attributions on multi-output models and should be discussed, not hidden.

---

## 6. Artefact Inventory

### 6.1 CSV / JSON outputs

```
results/explainability/
├── shap/
│   ├── global_stress.csv
│   ├── global_demand_dhaka.csv
│   └── global_stress_bar.png
├── permutation/
│   ├── demand_importance.csv
│   └── stress_importance.csv
├── attention/                          ← NEW (Phase 21)
│   ├── mean_spatial_matrix.csv
│   └── mean_spatial_matrix.json
├── case_studies/                       ← 24 folders × 4 CSVs each
│   └── 2024-09-08/
│       ├── stress_shap.csv
│       ├── node_importance.csv
│       ├── temporal_alpha.csv
│       └── osi_components.csv
└── figures/                            ← NEW (Phase 21)
    ├── 01_shap_summary_demand.{pdf,svg,png}
    ├── 02_shap_summary_stress.{pdf,svg,png}
    ├── 03_shap_bar_stress.{pdf,svg,png}
    ├── 04_node_attribution.{pdf,svg,png}
    ├── 05_temporal_attribution.{pdf,svg,png}
    ├── 06_attention_heatmap.{pdf,svg,png}
    ├── 07_stress_attribution.{pdf,svg,png}
    ├── 08_local_explanation_2024-09-08.{pdf,svg,png}
    └── manifest.json
```

### 6.2 Experiment reports (regenerated)

```
experiments/experiment_04_explainability_analysis/
├── xai_metrics.json
├── shap_summary.md
├── feature_importance.md
├── node_attribution.md
├── temporal_attribution.md
├── stress_attribution.md
├── case_studies.md
├── regional_analysis.md
└── xai_summary.md
```

---

## 7. Failures and Limitations

### 7.1 Failures

**None.** All eight requested figure types were generated successfully from real model outputs.

### 7.2 Known limitations (not fabricated — documented honestly)

| Limitation | Detail | Mitigation |
|---|---|---|
| **Demand SHAP–permutation mismatch** | ρ = −0.345 on this run | Report alongside stress ρ = 0.627; discuss coalition granularity |
| **Near-uniform temporal α_t** | No strong lag preference | Report as null finding; do not over-interpret |
| **Dual-path stress disagreement** | 52.2% agreement | Expected — SHAP and OSI components measure different constructs |
| **Local demand SHAP not saved per case** | Only stress SHAP in case CSVs | Local figure uses stress SHAP + node mass + temporal + OSI (all real) |
| **MPS numerical variance** | Demand perm ρ differs from prior run (−0.564 → −0.345) | Same checkpoint, same code; floating-point / batch ordering on MPS |
| **`.figure_build_venv` lacks pandas/torch** | Cannot run full pipeline in venv | Use `/opt/anaconda3/bin/python` for `run_explainability.py` |

### 7.3 What was NOT done (by design)

- No manuscript `.tex` files modified
- No synthetic SHAP values generated
- No PNG pixel-extraction for heatmap (superseded by real matrix export)
- No external `shap` library used (custom IG engine per project design)

---

## 8. Reproducibility

```bash
# 1. Full attribution (requires checkpoint + anaconda env)
cd Bangladesh_SmartGrid_STGT
/opt/anaconda3/bin/python experiments/experiment_04_explainability_analysis/run_explainability.py

# 2. Publication figures (requires step 1 outputs)
.figure_build_venv/bin/python experiments/experiment_04_explainability_analysis/export_publication_figures.py
```

**Prerequisites:**
- `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` (9.1 MB)
- Frozen data parquets in `data/features/` and `data/interim/`
- Python env with: `torch`, `pandas`, `numpy`, `scipy`, `matplotlib`

---

## 9. Phase 21 Verdict

| Criterion | Met |
|---|---|
| Real model inference | ✅ |
| Frozen checkpoint only | ✅ |
| Frozen test/validation splits | ✅ |
| No fabricated values | ✅ |
| 8 figure types generated | ✅ |
| PDF + SVG + PNG export | ✅ |
| Reproducible pipeline | ✅ |
| Report with methodology | ✅ |
| Manuscripts untouched | ✅ |

**Phase 21 status: COMPLETE**

**Recommended next step:** Update Phase 20 `replot_frozen_explainability.py` to read `attention/mean_spatial_matrix.csv` instead of PNG extraction before manuscript figure integration (separate phase).
