# Ablation Summary — Experiment 03

Generated: 2026-06-25

## Protocol

- Reference: **A1 PF-STGT W20** (Experiment 01B checkpoint, not retrained)
- Ablations A2–A6 trained with W20 settings (λ₂=20, demand÷100, balanced ES)
- Seed 42, identical chronological splits, Phase 15 metrics
- A5: geographical graph only; A6: correlation graph only (τ=0.65)

## Reference performance (A1, test)

- Demand MAE: 93.31 MW | R²: 0.6743
- Stress MAE: 0.0499 | R²: 0.5849

## Best ablation variant (demand MAE)

**Single-Task** (A4) — 86.89 MW

## Component contributions (ΔMAE vs A1)

| component                   | ablation_id   |   delta_mae_mw |   relative_degradation_pct | verdict               |
|:----------------------------|:--------------|---------------:|---------------------------:|:----------------------|
| Graph module                | A2            |           0.62 |                       0.66 | Supports component    |
| Transformer module          | A3            |          -0.66 |                      -0.71 | No measurable benefit |
| Multi-task learning         | A4            |          -6.42 |                      -6.88 | No measurable benefit |
| Hybrid graph (vs geo-only)  | A5            |           4.67 |                       5    | Supports component    |
| Hybrid graph (vs corr-only) | A6            |          -4.66 |                      -4.99 | No measurable benefit |

## Scope

- No explainability analyses
