# Frozen Results Inventory — Publication Asset Freeze

**Freeze date:** 2026-06-25  
**Git commit:** `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa`  
**Version tag (designated):** `publication-freeze-2026-06-25`

Complete catalogue of frozen experimental results. **Do not regenerate or edit** these artefacts
during manuscript preparation.

---

## 1. Final architecture (S2)

| Item | Value |
| --- | --- |
| **Architecture ID** | S2 — Correlation-Aware Multi-Task Forecasting Framework |
| **Original (S1)** | PF-STGT W20 hybrid — historical reference only |
| **Implementation** | `PFSTGT` + `GraphVariant.CORR` |
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **Authority** | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
| **Specification** | `experiments/architecture_freeze_revision/final_model_specification.md` |

### Frozen test performance (S2 = A6, seed 42)

| Metric | Value |
| --- | --- |
| Demand MAE | **88.65 MW** |
| Demand R² | 0.684 |
| Stress MAE | 0.0371 |
| Stress R² | **0.745** |

---

## 2. Dataset & splits

| Artefact | Path | MD5 (locked) |
| --- | --- | --- |
| Clean timeline | `data/interim/bangladesh_smartgrid_clean.parquet` | `4255024d735a91a4b53b2edee203d0ca` |
| Train features | `data/features/train_features.parquet` | `b8b3bda95d0fd6cc65f4910d85a98e16` |
| Geographic adjacency | `graphs/adjacency_matrix.csv` | `dacb7ac3a827d00a4b61ea9400e75686` |
| Correlation graph | Built at runtime (`GraphVariant.CORR`, τ=0.65) | — |

### Split policy (frozen)

| Split | Samples | Date range |
| --- | --- | --- |
| Train | 1,281 windows | 2019-11-21 → 2023-06-15 |
| Validation | 263 windows | 2023-06-16 → 2024-03-19 |
| Test | 264 windows | 2024-03-20 → 2024-12-30 |
| Window T | 7 | Warm-up skip 7 rows per split |

Authority: `src/constants.py`, Phase 04 chronological split.

---

## 3. Training configuration (W20 — frozen)

| Setting | Value | Source |
| --- | --- | --- |
| Optimizer | Adam, lr = 5×10⁻⁴ | A6 `config.yaml` |
| Weight decay | 10⁻⁴ | same |
| λ₂ (stress) | **20.0** | Exp01B W20 |
| Demand loss norm | Huber ÷ 100 | Exp01B |
| Early stopping | 0.7·(val_MAE/100) + 0.3·val_stress_MAE | Exp01B |
| Batch size | 32 | checkpoint config |
| Seed | 42 | all reference runs |
| Max epochs | 200 (early stop ~70) | Exp03 A6 |

Authority: `experiments/experiment_01B_multitask_optimization_repair/best_configuration.md`

S1 checkpoint: `experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt`

---

## 4. Experiment 01 — Initial PF-STGT training

| Deliverable | Path |
| --- | --- |
| Metrics | `experiments/experiment_01_pf_stgt/metrics.json` |
| Training summary | `training_summary.md` |
| Loss plots | `train_loss.png`, `val_loss.png` |
| Checkpoint | `experiments/experiment_01_pf_stgt/B07/seed_42/` |

**Status:** Frozen (superseded by Exp01B W20 for S1 reference)

---

## 5. Experiment 01A — OSI failure investigation

| Deliverable | Path |
| --- | --- |
| Root cause | `root_cause_report.md` |
| OSI distribution | `osi_distribution_report.md` |
| Loss weight analysis | `loss_weight_analysis.md` |
| Correlation analysis | `correlation_analysis.md` |
| Prediction distribution | `prediction_distribution_report.md` |

**Status:** Frozen (diagnostic; informs Exp01B)

---

## 6. Experiment 01B — Multitask optimization repair

| Deliverable | Path |
| --- | --- |
| Results JSON | `results.json` |
| Best config | `best_configuration.md` |
| Repair summary | `repair_summary.md` |
| Gradient analysis | `gradient_analysis.md` |
| Root cause confirmation | `root_cause_confirmation.md` |
| W20 checkpoint (S1) | `checkpoints/W20/B07/seed_42/best.pt` |

**Status:** Frozen — defines W20 training protocol and S1 reference model

---

## 7. Experiment 02 — Benchmark models

| Deliverable | Path |
| --- | --- |
| **Primary results** | `benchmark_results.csv` |
| Summary | `benchmark_summary.md` |
| Rankings | `benchmark_rankings.md` |
| Performance tables | `performance_tables.md` |
| Statistical significance | `statistical_significance.md` |
| Checkpoints | `checkpoints/B01–B07/seed_42/` |

### Frozen benchmark test MAE (MW)

| ID | Model | Demand MAE |
| --- | --- | --- |
| B07 | PF-STGT W20 (S1) | 93.31 |
| B02 | Random Forest | 97.03 |
| B03 | XGBoost | 109.73 |
| B06 | T-GCN | 257.21 |
| B01 | Linear Regression | 247.79 |

**Status:** Frozen

---

## 8. Experiment 02A — Classical benchmark verification

| Deliverable | Path |
| --- | --- |
| Verification report | `benchmark_verification_report.md` |
| Metric verification | `metric_verification.md` |
| Aggregation audit | `aggregation_audit.md` |
| Variance explanation | `variance_explanation.md` |
| Residual analysis | `residual_analysis.md` |
| Prediction distribution | `prediction_distribution_analysis.md` |
| Predictions | `predictions/` |
| Plots | `plots/` |

**Status:** Frozen — R² aggregation discrepancy resolved; MAE rankings unchanged

---

## 9. Experiment 03 — Ablation studies

| Deliverable | Path |
| --- | --- |
| **Primary results** | `ablation_results.csv` |
| Raw JSON | `ablation_raw.json` |
| Summary | `ablation_summary.md` |
| Rankings | `ablation_rankings.md` |
| Component contribution | `component_contribution.md` |
| Statistical significance | `statistical_significance.md` |
| Checkpoints | `checkpoints/A2–A6/seed_42/best.pt` |

### Frozen ablation test demand MAE (MW)

| ID | Variant | MAE | Notes |
| --- | --- | --- | --- |
| A4 | Single-task | 86.89 | Demand-only |
| **A6 (= S2)** | Correlation graph | **88.65** | **Final model** |
| A3 | No transformer | 92.64 | |
| A1 (= S1) | Full W20 | 93.31 | Reference |
| A2 | No graph | 93.93 | |
| A5 | Geo only | 97.98 | |

**Status:** Frozen

---

## 10. Experiment 03A — Ablation failure investigation

| Deliverable | Path |
| --- | --- |
| Metrics JSON | `investigation_metrics.json` |
| Task interference | `task_interference_report.md` |
| Transformer utilization | `transformer_utilization_report.md` |
| Graph contribution | `graph_contribution_report.md` |
| Trade-off analysis | `tradeoff_analysis.md` |
| Root cause summary | `root_cause_summary.md` |
| Recommendations | `recommendation_report.md` |

**Status:** Frozen (interpretation layer; no new training)

---

## 11. Experiment 03B — Architecture simplification

| Deliverable | Path |
| --- | --- |
| **Primary results** | `simplification_results.csv` |
| Raw JSON | `simplification_raw.json` |
| Complexity analysis | `complexity_analysis.md` |
| Performance vs complexity | `performance_vs_complexity.md` |
| Architecture recommendation | `architecture_recommendation.md` |
| Final decision | `final_architecture_decision.md` |
| S4 checkpoint (analysis only) | `checkpoints/S4/seed_42/best.pt` |

**Status:** Frozen — **S2 selected** as final architecture

---

## 12. Experiment 04 — Explainability analysis

| Deliverable | Path |
| --- | --- |
| XAI summary | `xai_summary.md` |
| SHAP summary | `shap_summary.md` |
| Feature importance | `feature_importance.md` |
| Node attribution | `node_attribution.md` |
| Temporal attribution | `temporal_attribution.md` |
| Stress attribution | `stress_attribution.md` |
| Case studies | `case_studies.md` |
| Regional analysis | `regional_analysis.md` |
| Metrics JSON | `xai_metrics.json` |
| Figures | `figures/figure_*.png` |
| Runtime CSVs | `results/explainability/` |

### Frozen XAI headline findings

| Finding | Value |
| --- | --- |
| Top stress coalition | G8 (limitation_stack) |
| Top demand coalition (Dhaka) | G6 (calendar_trend), G4 (lags) |
| Attention–adjacency Spearman | 0.422 |
| Stress driver agreement | 52.2% |
| Case studies | 24 dates |

**Status:** Frozen

---

## 13. Architecture & publication freeze docs

| Document | Path |
| --- | --- |
| Architecture freeze decision | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
| Transition summary | `architecture_transition_summary.md` |
| Final model spec | `final_model_specification.md` |
| Decision log | `docs/decision_logs/architecture_freeze_2026-06-25.md` |
| Publication freeze | `paper/publication_freeze/Publication_Asset_Freeze.md` |
| This inventory | `paper/publication_freeze/frozen_results_inventory.md` |

---

## 14. Completeness verification

| Experiment | Primary numeric artefact | Reports | Status |
| --- | --- | --- | --- |
| 01 | metrics.json | Yes | Complete |
| 01A | — | 5 reports | Complete |
| 01B | results.json + W20 ckpt | Yes | Complete |
| 02 | benchmark_results.csv | Yes | Complete |
| 02A | predictions/ | 6 reports | Complete |
| 03 | ablation_results.csv | Yes | Complete |
| 03A | investigation_metrics.json | 6 reports | Complete |
| 03B | simplification_results.csv | Yes | Complete |
| 04 | xai_metrics.json + CSV tree | 8 reports + 8 figures | Complete |

**All publication assets finalized. Repository ready for manuscript development.**

---

## 15. Post-freeze workflow

1. Write manuscript in `manuscript/drafts/` or `manuscript/overleaf/`.
2. Import tables from paths in `frozen_tables_inventory.md`.
3. Include figures from `manuscript/overleaf/figures/`.
4. Cite S2 as proposed final model; disclose S1/B07 as original design benchmark.
5. Commit working tree and apply tag `publication-freeze-2026-06-25`.
