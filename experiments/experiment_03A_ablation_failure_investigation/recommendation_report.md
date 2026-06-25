# Recommendation Report — Experiment 03A

Generated: 2026-06-25

## For paper / thesis reporting

1. **Do not claim** PF-STGT full model (A1) is the best demand forecaster — report A4/A6 as
   demand-strong baselines and A1 as the **multi-task reference**.
2. **Report hybrid graph value conditionally:** beats geography-only; correlation-only may
   outperform hybrid on demand — discuss edge-density and noise from border links.
3. **Frame transformer contribution as modest** for this dataset (A3 ≈ A1); emphasize graph-temporal
   encoding as the primary temporal mechanism.

## For methodology fixes (future experiments, no retraining here)

1. **Retrain A1 under identical Exp03 protocol** (same seed, same stopping rule variant) before
   component claims — current A1/A4 comparison mixes checkpoint provenance.
2. **Report two A1 rows:** demand-optimal ES vs W20 balanced ES.
3. **Use unified R² definition** (macro per-region) across all models (see Experiment 02A).
4. **Graph ablation:** compare hybrid, geo, corr with **matched training** and consider
   correlation-only or threshold-tuned hybrid for demand-focused deployment.

## Model selection guidance

| Deployment goal | Recommended variant |
| --- | --- |
| Demand-only accuracy | A4 or A6 (corr graph) |
| Joint demand + OSI (paper claim) | A1 W20 with explicit trade-off disclosure |
| Stress accuracy | A5/A6 (lower stress MAE than A1) |
| Interpretability / graph edges | Hybrid A1 (Phase 08 design intent) |

## Scope

- No benchmark retraining
- No Sprint 04 explainability pipeline
- Diagnostics from saved Exp03 checkpoints only
