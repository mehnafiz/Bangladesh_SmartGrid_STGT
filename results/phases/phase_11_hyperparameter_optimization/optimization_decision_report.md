# Optimization Decision Report — Phase 11

Generated: 2026-06-24

## Key decisions

### 1. Random Search over 20 trials

| method                      |   total_score | selected   | verdict                                                                                            |
|:----------------------------|--------------:|:-----------|:---------------------------------------------------------------------------------------------------|
| Grid Search                 |            10 | False      | Full Cartesian product infeasible; overfits validation with 19k+ configs.                          |
| Random Search               |            21 | True       | Seeded sampling over constrained space; reproducible and adequate for ~1.3k train windows.         |
| Bayesian Optimization (TPE) |            17 | False      | Efficient but Optuna/version sensitivity; val set too small (277 rows) for surrogate overfit risk. |

Grid search rejected (19,683 combos). Bayesian rejected (small val set, reproducibility).

### 2. Realistic ranges for 9-node STGT

- d_model capped at 192 (not 256/512) given ~1,287 training windows.
- Layers L_s, L_t capped at 3 to limit over-smoothing and overfitting.
- Batch size 16–64 appropriate for ~40–80 steps/epoch.

### 3. Two-stage selection

20 exploratory trials → top-3 configs × 3 seeds → single test evaluation.

### 4. Fixed loss weights

λ1=1.0, λ2=0.5 not searched (Phase 10 frozen) to reduce validation overfitting.

### 5. Alignment with Phase 09 defaults

Phase 09 default (d=128, L_s=2, L_t=2, H=4, lr=5e-4, B=32) included as **trial #0** 
baseline in Stage 1 manifest for direct before/after comparison.
