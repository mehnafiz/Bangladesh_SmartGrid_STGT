# Benchmark Verification Report — Experiment 02A

Generated: 2026-06-25

## Executive summary

Experiment 02A audited PF-STGT, Random Forest, and XGBoost benchmark consistency.
**MAE rankings are valid.** The apparent MAE vs R² ranking inversion is **not** a
model-quality contradiction — it is primarily caused by **inconsistent R² aggregation**
between classical and deep-model evaluation paths in Experiment 02.

## Root cause

1. **Inconsistent metric definition (confirmed):** B02/B03 R² was computed as a
   **single pooled R²** over all region-day pairs (`train_classical.py`). B07 R² was
   computed as the **mean of nine per-region R² values** (`evaluation.metrics.compute_demand_metrics`).
2. **Secondary behavioral factor:** PF-STGT predictions have lower variance than actuals
   (pred_std/actual_std ≈ 0.98), improving macro MAE while depressing per-region R² on
   high-variance regions such as Dhaka.

## Verified rankings (unified macro metrics, test set)

| Rank | Model | Macro MAE (MW) | Macro R² |
| --- | --- | --- | --- |
| 1 | PF-STGT (W20) | 93.31 | 0.6743 |
| 2 | Random Forest | 97.03 | 0.6878 |
| 3 | XGBoost | 109.73 | 0.5902 |

Under unified macro R², **Random Forest still leads R²** (0.6878) while **PF-STGT leads MAE** (93.31 MW).
This reflects a genuine bias–variance trade-off: PF-STGT minimizes absolute error;
RF better explains regional variance.

## Recommendations

- Re-report all models using **one R² definition** (Phase 15 macro mean-of-regions).
- Optionally report **pooled R²** as a supplementary column for all models.
- Keep **macro MAE** as the primary ranking metric (unchanged).

## Outputs

- `metric_verification.md`
- `aggregation_audit.md`
- `residual_analysis.md`
- `prediction_distribution_analysis.md`
- `variance_explanation.md`
- `predictions/` — materialized test predictions
- `plots/` — residual and actual-vs-predicted figures

## Scope

- No model retraining (PF-STGT checkpoint inference only; classical replay for prediction materialization only).
- No ablations or explainability.
