# Benchmark Summary — Experiment 02

Generated: 2026-06-25

## Protocol

- Identical chronological train/validation/test splits (Sprint 01)
- Identical targets and features
- Seed 42 for all models
- Classical models (B01–B03) trained without PyTorch loaded
- PF-STGT uses Experiment 01B W20 checkpoint (not retrained)

## Best model (demand MAE): **PF-STGT (W20)** (B07)

- Test demand MAE: 93.31 MW
- Test demand R²: 0.6743

## PF-STGT (B07 W20)

- Demand MAE: 93.31 MW, R²: 0.6743
- Stress MAE: 0.0499, R²: 0.5849

## Scope

- No ablations or explainability
