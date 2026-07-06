# Explainability Audit Report — Phase 17

**Audit date:** 6 July 2026  
**Scope:** Full repository read-only audit  
**Authority:** `paper/prompts/17_Explainability_Audit.md`  
**Freeze reference:** `paper/publication_freeze/` (2026-06-25)  
**Constraint:** No experiments executed; no figures generated; no manuscript modified

---

## 1. Executive Summary

The explainability framework is **scientifically complete and publication-frozen** for the final model **S2 (A6, seed 42)**. Experiment 04 (`experiments/experiment_04_explainability_analysis/`) executed all designed attribution pipelines on the frozen checkpoint without retraining. Outputs exist as CSV artefacts, JSON metrics, eight manuscript figures, eight markdown reports, and unit tests.

**Critical finding:** Attribution is implemented as a **custom PyTorch integrated-gradients loop** (`src/explainability/shap_engine.py`), described in papers as a GradientSHAP approximation. The `shap` and `captum` packages are listed in `requirements.txt` but **never imported** in application code. This is documented in the journal appendix; it is not a silent omission.

| Status | Count |
|---|---|
| Fully implemented & executed | 6 methods (GradientSHAP/IG, permutation, attention, temporal, node, stress) |
| Partially implemented | 2 (train-background SHAP, stability bootstraps — config only) |
| Missing / not used | 3 (exact SHAP, `shap` library, Captum API) |
| Deprecated / superseded | 2 folders (`experiment_04_explainability/`, `src/explainability/README.md`) |

**Publication readiness:** Journal manuscript requirements are **met**. Conference manuscript requirements are **met** (distilled subset). **No regeneration is scientifically required** unless reproducibility audit, dependency alignment, or optional robustness extensions are desired.

---

## 2. Final Model & Checkpoint

| Property | Value |
|---|---|
| **Architecture** | S2 — Correlation-Only PF-STGT |
| **Ablation ID** | A6 |
| **Seed** | 42 |
| **Graph variant** | `GraphVariant.CORR` (τ = 0.65) |
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **Size** | ~9.1 MB (present on disk) |
| **Companion files** | `config.yaml`, `metrics_val.json` in same directory |
| **Loader** | `FoundationCoordinator(verify_md5=True, graph_variant=GraphVariant.CORR)` + `PFSTGT.load_state_dict()` |
| **Authority docs** | `experiments/architecture_freeze_revision/final_model_specification.md`, `checkpoints/README.md` |

**Compatibility:** `run_explainability.py` loads S2 with `return_attention=True` via `PFSTGT` forward pass. Model supports attention export in `src/models/pf_stgt.py`, `graph_transformer.py`, `temporal_transformer.py`.

**Out of scope:** Explainability on S1 (B07), ablation variants A1–A5, or benchmark models B01–B06.

---

## 3. Dataset Pipeline & Evaluation Context

### 3.1 Splits (chronological, frozen)

| Split | Windows | Date range |
|---|---|---|
| Train | 1,281 | 2019-11-21 → 2023-06-15 |
| Validation | 263 | 2023-06-16 → 2024-03-19 |
| Test | 264 | 2024-03-20 → 2024-12-30 |
| Lookback T | 7 days | Horizon H = 1 |

Authority: `paper/publication_freeze/frozen_results_inventory.md`, `src/constants.py`

### 3.2 Explainability data usage (Exp04)

| Analysis | Split | Sample scope |
|---|---|---|
| Global GradientSHAP (stress) | Validation | ≤ 20 batches (batch size 8) |
| Global GradientSHAP (Dhaka demand) | Validation | ≤ 20 batches |
| Regional demand φ averages | Validation | 10 samples × 9 regions |
| Permutation importance | Validation | 8 batches, 5 repeats |
| Case studies | Validation + test | 20 + 4 = 24 stratified dates |
| Attention / node / temporal / stress | Per case-study sample | 24 folders |

**Note:** Full test split (264 windows) is **not** used for global SHAP aggregation. Case studies include 4 representative test days. This is by design (Phase 12 protocol).

### 3.3 Normalization & leakage

| Component | Policy |
|---|---|
| Input features | Raw engineered values (no global StandardScaler in DL pipeline) |
| OSI target | Train-split min–max via `OSITargetBuilder` (`src/targets/osi.py`) |
| Stress Path B (OSI components) | Same train bounds in `stress_attribution.decompose_components` |
| Adjacency | Row-normalised correlation graph at runtime (`src/graph/adjacency.py`) |
| Leakage guard | `operational_stress_index` excluded from inputs (`src/features/leakage_guard.py`) |

### 3.4 Feature names & coalitions

**Node features (9 per region):** `{region}_demand`, `{region}_supply`, `{region}_load`, `demand_lag_1_{region}`, `demand_lag_7_{region}`, `load_lag_1_{region}`, `demand_rolling_mean_7_{region}`, `regional_demand_share_{region}`, `regional_load_intensity_{region}`

**Global features (17):** Defined in `GLOBAL_INPUT_FEATURE_NAMES` (`src/features/specs.py`)

**Coalition registry (G1–G11):** `src/explainability/coalitions.py` — masks node/global features into interpretable groups for grouped attribution.

---

## 4. Method-by-Method Audit

### 4.1 SHAP (exact / TreeSHAP / KernelSHAP)

| Aspect | Status |
|---|---|
| Implementation | **Missing** |
| Library usage | `shap==0.45.1` in `requirements.txt`; **zero Python imports** |
| Rationale | Coalition-grouped attributions use custom IG loop instead of exact Shapley enumeration |
| Paper disclosure | Journal appendix notes no independent `shap` package export |

### 4.2 GradientSHAP

| Aspect | Status |
|---|---|
| Implementation | **Complete** — `src/explainability/shap_engine.py` (`ShapEngine`) |
| Algorithm | Integrated-gradients loop over coalition-masked inputs; described as GradientSHAP approximation |
| Config default | 50 steps (`ExplainabilityConfig.gradient_shap_steps`) |
| Exp04 runtime | **25 steps** (override in `run_explainability.py`) |
| Baseline | **Zero baseline** (`_zero_baseline`); config `background_samples=100` **not used** |
| Outputs | `results/explainability/shap/global_stress.csv`, `global_demand_dhaka.csv` |
| Tests | `tests/test_shap_engine.py` |

**Partial gap:** Train-background SHAP (100 samples in config) designed but not executed.

### 4.3 Integrated Gradients

| Aspect | Status |
|---|---|
| Implementation | **Complete** — same engine as GradientSHAP (`_integrated_gradients` in `shap_engine.py`) |
| Baseline | Zero tensor baseline |
| Citation | Sundararajan et al. cited in both manuscripts |

Functionally identical to GradientSHAP path in this codebase (single implementation, dual naming in docs/papers).

### 4.4 Captum

| Aspect | Status |
|---|---|
| Implementation | **Missing in code** |
| Dependency | `captum==0.7.0` in `requirements.txt`; **zero Python imports** |
| Paper language | "Captum-compatible integrated-gradients loop" (journal `05_results.tex`) |
| Disclosure | Journal appendix: no independent Captum export run |

**Recommendation (optional, not required for publication):** Either run Captum `IntegratedGradients` as cross-validation or remove Captum from environment claims in future revisions.

### 4.5 Permutation Importance

| Aspect | Status |
|---|---|
| Implementation | **Complete** — `src/explainability/permutation.py` |
| Method | Coalition-mask ablation; MAE degradation on validation batches |
| Config | 5 repeats (`permutation_repeats=5`); 8 batches in Exp04 |
| Outputs | `results/explainability/permutation/demand_importance.csv`, `stress_importance.csv` |
| Cross-check | Spearman ρ vs GradientSHAP: demand −0.564, stress 0.366 |
| Tests | `tests/test_permutation_importance.py` |

### 4.6 Attention Analysis

| Aspect | Status |
|---|---|
| Implementation | **Complete** — `src/explainability/attention_extractor.py` |
| Model hook | `PFSTGT(..., return_attention=True)` exports spatial + temporal attention |
| Metrics | Spearman ρ(attention, correlation adjacency) = 0.422 |
| Top-level export dir | `results/explainability/attention/` — **empty** (attention embedded in case-study + node pipeline, not standalone CSV export) |
| Tests | `tests/test_attention_extractor.py` |

### 4.7 Temporal Attribution

| Aspect | Status |
|---|---|
| Implementation | **Complete** — `src/explainability/temporal_attribution.py` |
| Method | Mean temporal attention weights α_t over T = 7 lags |
| Key finding | Near-uniform weights; t−6 highest (α = 0.1622) |
| Outputs | Per-case `temporal_alpha.csv` in 24 case-study folders; figure `figure_temporal_importance.png` |
| Report | `experiments/experiment_04_explainability_analysis/temporal_attribution.md` |
| Tests | `tests/test_attribution_modules.py` |

### 4.8 Node Attribution

| Aspect | Status |
|---|---|
| Implementation | **Complete** — `src/explainability/node_attribution.py` |
| Method | Combined GradientSHAP node mass + spatial attention inflow/outflow |
| Key finding | Dhaka mass 340.36; Rajshahi 110.32; Khulna 108.91 |
| Outputs | Per-case `node_importance.csv`; figure `figure_node_importance_heatmap.png` |
| Report | `experiments/experiment_04_explainability_analysis/node_attribution.md` |
| Tests | `tests/test_attribution_modules.py` |

### 4.9 Stress Attribution (dual-path)

| Aspect | Status |
|---|---|
| Implementation | **Complete** — `src/explainability/stress_attribution.py` |
| Path A | Grouped GradientSHAP stress coalitions |
| Path B | OSI component decomposition (c1 shedding, c2 reserve, c3 limitation) |
| Agreement | 13/24 cases (52.2%) |
| Outputs | Per-case `stress_shap.csv`, `osi_components.csv`; figure `figure_stress_attribution.png` |
| Report | `experiments/experiment_04_explainability_analysis/stress_attribution.md`, `case_studies.md` |
| Tests | `tests/test_attribution_modules.py` |

### 4.10 SHAP Stability Bootstraps

| Aspect | Status |
|---|---|
| Config | `shap_stability_bootstraps=10`, threshold 0.7 in `ExplainabilityConfig` |
| Execution | **Not run** — no bootstrap stability artefacts in `results/explainability/` |

---

## 5. Implementation Inventory

### 5.1 Core modules (`src/explainability/`)

| File | Role | Status |
|---|---|---|
| `config.py` | Frozen XAI defaults | Complete |
| `types.py` | Typed result containers | Complete |
| `coalitions.py` | G1–G11 registry + masks | Complete |
| `shap_engine.py` | Grouped GradientSHAP / IG | Complete |
| `permutation.py` | Coalition permutation importance | Complete |
| `attention_extractor.py` | Spatial/temporal attention aggregation | Complete |
| `node_attribution.py` | Regional node mass | Complete |
| `temporal_attribution.py` | α_t temporal weights | Complete |
| `stress_attribution.py` | Dual-path stress | Complete |
| `__init__.py` | Public API | Complete |
| `README.md` | Placeholder "Future Contents" | **Deprecated / stale** |

### 5.2 Experiments

| Path | Status |
|---|---|
| `experiments/experiment_04_explainability_analysis/` | **PRIMARY — executed** |
| `experiments/experiment_04_explainability/` | **Deprecated scaffold** ("Prepared — no execution") |

### 5.3 Scripts

| Path | Role | Status |
|---|---|---|
| `experiments/experiment_04_explainability_analysis/run_explainability.py` | End-to-end Exp04 runner | Complete |
| `scripts/sprint_04_explainability.py` | Sprint design report (no XAI run) | Complete |
| `scripts/phase_12_explainability_design.py` | Phase 12 design doc generator | Complete |
| `paper/final_results_package/replot_frozen_explainability.py` | Replot from frozen CSV/JSON | Complete (no model) |

### 5.4 Design documentation

| Path | Content |
|---|---|
| `explainability/explainability_protocol.md` | Frozen execution workflow |
| `explainability/xai_strategy.md` | Toolkit selection |
| `explainability/shap_design.md` | SHAP/IG design |
| `explainability/attention_analysis_design.md` | Attention export |
| `explainability/node_importance_design.md` | Node attribution |
| `explainability/stress_attribution_design.md` | Dual-path stress |
| `architecture/explainability_design.md` | Architecture-level XAI |
| `docs/phases/Phase_12_Explainability_Design_Framework.md` | Phase 12 framework |
| `docs/sprints/Sprint_04_Explainability_System.md` | Sprint 04 spec |

### 5.5 Tests

| File | Coverage |
|---|---|
| `tests/test_shap_engine.py` | SHAP engine shapes |
| `tests/test_permutation_importance.py` | Permutation scoring |
| `tests/test_attention_extractor.py` | Attention aggregation |
| `tests/test_attribution_modules.py` | Node/temporal/stress |
| `tests/test_explainability_coalitions.py` | Coalition masks |

### 5.6 Configs

No dedicated explainability YAML in `configs/`. All defaults live in `ExplainabilityConfig` dataclass; Exp04 overrides `gradient_shap_steps=25` and `device` at runtime.

---

## 6. Existing Outputs

### 6.1 Machine-readable artefacts

```
results/explainability/
├── shap/
│   ├── global_stress.csv
│   ├── global_demand_dhaka.csv
│   └── global_stress_bar.png
├── permutation/
│   ├── demand_importance.csv
│   └── stress_importance.csv
└── case_studies/          # 24 date folders
    └── <YYYY-MM-DD>/
        ├── stress_shap.csv
        ├── node_importance.csv
        ├── temporal_alpha.csv
        └── osi_components.csv
```

**Empty / unused config directories:** `results/explainability/attention/`, `nodes/`, `stress/` (defined in config helpers but not written by Exp04).

### 6.2 Experiment reports (`experiments/experiment_04_explainability_analysis/`)

| File | Status |
|---|---|
| `xai_metrics.json` | Real — headline metrics (device: mps) |
| `xai_summary.md` | Real |
| `shap_summary.md` | Real |
| `feature_importance.md` | Real |
| `node_attribution.md` | Real |
| `temporal_attribution.md` | Real |
| `stress_attribution.md` | Real |
| `case_studies.md` | Real |
| `regional_analysis.md` | Real |
| `Experiment_04_Explainability_Analysis.md` | Real — execution record |

### 6.3 Figures (Exp04 — all **real, frozen**)

| File | Manuscript mapping (journal) |
|---|---|
| `figure_shap_summary_stress.png` | Fig. 6a (SHAP stress) |
| `figure_shap_summary_demand.png` | Fig. 6b (SHAP demand Dhaka) |
| `figure_shap_bar_stress.png` | Fig. S1 (supplementary bar) |
| `figure_feature_importance_ranking.png` | Permutation ranking |
| `figure_node_importance_heatmap.png` | Fig. 7 (node heatmap) |
| `figure_temporal_importance.png` | Fig. 8 (temporal α_t) |
| `figure_stress_attribution.png` | Fig. 9 (dual-path stress) |
| `figure_regional_contribution.png` | Regional SHAP panel |

Copies also in: `manuscript/overleaf/figures/`, `paper/latex/figures/`, `paper/final_results_package/figures/`.

### 6.4 Headline metrics (frozen, `xai_metrics.json`)

| Metric | Value |
|---|---|
| Top stress coalition | G8 \|φ\| = 0.0191 |
| Top Dhaka demand | G6 = 162.34, G4 = 101.26, G10 = 91.44 |
| Attention–adjacency Spearman ρ | 0.422 |
| SHAP–permutation ρ (demand) | −0.564 |
| SHAP–permutation ρ (stress) | 0.366 |
| OSI dual-path agreement | 52.2% (13/24) |
| Dhaka mean node mass | 340.36 |

### 6.5 Reproducibility assessment

| Check | Verdict |
|---|---|
| Checkpoint present | Yes |
| CSV/JSON artefacts present | Yes |
| Figures match metrics | Yes (cross-checked against `xai_metrics.json`) |
| MD5-locked data pipeline | Yes (`FoundationCoordinator(verify_md5=True)`) |
| Deterministic seed | Seed 42 in Exp04 |
| Device dependency | Original run on MPS; CPU/CUDA should reproduce rankings (not re-verified in this audit) |

**Regeneration required?** **No** for publication freeze. Optional only for robustness extensions or environment parity checks.

---

## 7. Missing, Partial, and Deprecated Items

### 7.1 Missing

| Item | Impact |
|---|---|
| Exact SHAP / `shap` library execution | Low — disclosed; custom IG used |
| Captum API execution | Low — disclosed in appendix |
| SHAP stability bootstraps | Medium for robustness claims; not in manuscript |
| Train-background SHAP (100 samples) | Medium — config vs runtime mismatch |
| Standalone attention CSV export | Low — data in case studies |
| Explainability on non-S2 models | Out of scope |
| Operator-in-the-loop validation | Out of scope (future work) |

### 7.2 Partial

| Item | Gap |
|---|---|
| `ExplainabilityConfig.background_samples` | Configured (100) but zero baseline used |
| `ExplainabilityConfig.gradient_shap_steps` | Default 50; Exp04 uses 25 |
| `results/explainability/attention/` | Directory unused |
| `src/explainability/README.md` | Stale placeholder |

### 7.3 Deprecated

| Item | Replacement |
|---|---|
| `experiments/experiment_04_explainability/` | `experiment_04_explainability_analysis/` |
| Legacy PNG symlinks in `paper/conference/figures/` | TikZ (Figs 1–2) + PDF (Figs 3–4); real PNG for Fig. 7 |

---

## 8. Publication Requirements

### 8.1 Journal Paper (`paper/latex/`, `paper/sections/`)

**Scientifically required (per frozen manuscript):**

| Deliverable | Required | Present | Location |
|---|---|---|---|
| Grouped GradientSHAP (stress + demand) | Yes | Yes | Figs 6a/6b; `shap_summary.md` |
| Permutation cross-check | Yes | Yes | `feature_importance.md`; Table 7 |
| Node attribution heatmap | Yes | Yes | Fig. 7 |
| Temporal attribution | Yes | Yes | Fig. 8 |
| Dual-path stress attribution | Yes | Yes | Fig. 9 |
| Case-study stratification (24) | Yes | Yes | `case_studies.md` |
| Explainability summary table | Yes | Yes | Table 7 (`table_07_explainability.tex`) |
| Cross-method discordance reporting | Yes | Yes | Results §5.6; Discussion |
| Limitations (no causation) | Yes | Yes | Discussion + Results scope |

**Supplementary (frozen inventory):**

| Item | Table/Figure | Present |
|---|---|---|
| Global SHAP CSVs | Table S2 | Yes |
| Permutation CSVs | Table S3 | Yes |
| Case-study summary | Table S4 | Yes |
| SHAP bar stress | Fig. S1 | Yes |

**Journal status: REQUIREMENTS MET — no additional explainability outputs required.**

### 8.2 Conference Paper (`paper/conference/`)

**Scientifically required (per distillation):**

| Deliverable | Required | Present | Notes |
|---|---|---|---|
| Node attribution heatmap | Yes | Yes | `figure_07_node_importance.png` |
| Coalition rankings in prose | Yes | Yes | G8, G6, G4, G10 cited |
| Cross-method metrics in prose | Yes | Yes | ρ = 0.422, −0.564, 52.2% |
| SHAP coalition figures | No | Removed | Distilled to text |
| Temporal attribution figure | No | Removed | Near-uniform; low density |
| Dual-path stress figure | No | Removed | Agreement in text |
| Table 7 | No | Removed | Metrics inlined |

**Conference status: REQUIREMENTS MET — no additional explainability outputs required.**

---

## 9. Required Manuscript Changes

**Per audit mandate: no manuscript modifications were made.**

| Manuscript | Explainability changes needed |
|---|---|
| Journal (`paper/latex/`) | **None** — Section 5.6, Table 7, Figs 6–9 aligned with Exp04 freeze |
| Conference (`paper/conference/`) | **None** — distilled explainability paragraph + Fig. 7 sufficient |

**Optional future clarifications (not blocking):**

1. Harmonise environment section: state custom IG implementation vs `shap`/`captum` package usage.
2. Document Exp04 override (`gradient_shap_steps=25` vs config default 50).
3. Conference Fig. 7 remains raster PNG — visual quality only, not scientific gap.

---

## 10. Recommended Execution Order (If Regeneration Ever Needed)

*Not required for current publication freeze. Provided for reproducibility maintenance only.*

1. Verify checkpoint: `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt`
2. Verify data MD5 locks: `FoundationCoordinator(verify_md5=True)`
3. Run: `python experiments/experiment_04_explainability_analysis/run_explainability.py`
4. Validate: `xai_metrics.json` headline values against frozen inventory
5. Optional replot (no model): `python paper/final_results_package/replot_frozen_explainability.py`
6. Copy figures to `manuscript/overleaf/figures/` and `paper/latex/figures/`
7. Run unit tests: `pytest tests/test_shap_engine.py tests/test_permutation_importance.py tests/test_attention_extractor.py tests/test_attribution_modules.py tests/test_explainability_coalitions.py`

**Optional extensions (not in current manuscripts):**

8. SHAP stability bootstraps (config already defined)
9. Train-background SHAP (100 samples)
10. Independent Captum `IntegratedGradients` cross-check
11. Full test-split global SHAP (currently validation-only for global aggregates)

---

## 11. Audit Conclusions

| Question | Answer |
|---|---|
| Is explainability implemented? | **Yes** — full custom pipeline in `src/explainability/` |
| Was it executed on S2? | **Yes** — Experiment 04 complete |
| Are outputs real and frozen? | **Yes** — CSV, JSON, 8 figures, 8 reports |
| Are outputs reproducible? | **Yes** — checkpoint + MD5-locked pipeline + seed 42 |
| Journal requirements met? | **Yes** |
| Conference requirements met? | **Yes** |
| Regeneration required? | **No** |
| Blocking gaps? | **None** |

### Final verdict

**The explainability framework is scientifically complete, internally consistent with the publication freeze, and publication-ready for both journal and conference manuscripts. No explainability experiments or figure generation are required before submission.**

---

*Audit performed read-only. No code, data, figures, or manuscripts were modified.*
