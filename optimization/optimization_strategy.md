# Optimization Strategy — Phase 11

Generated: 2026-06-24
Status: **FROZEN**

## Method comparison

| method                      |   trials_needed |   reproducibility |   val_efficiency |   implementation_complexity |   small_data_suitability |   total_score | selected   | verdict                                                                                            |
|:----------------------------|----------------:|------------------:|-----------------:|----------------------------:|-------------------------:|--------------:|:-----------|:---------------------------------------------------------------------------------------------------|
| Grid Search                 |           19683 |                 5 |                1 |                           2 |                        2 |            10 | False      | Full Cartesian product infeasible; overfits validation with 19k+ configs.                          |
| Random Search               |              20 |                 5 |                4 |                           4 |                        4 |            21 | True       | Seeded sampling over constrained space; reproducible and adequate for ~1.3k train windows.         |
| Bayesian Optimization (TPE) |              15 |                 3 |                5 |                           3 |                        3 |            17 | False      | Efficient but Optuna/version sensitivity; val set too small (277 rows) for surrogate overfit risk. |

## Selected: **Random Search (seeded, validation-only)** (score 21/25)

Seeded sampling over constrained space; reproducible and adequate for ~1.3k train windows.

## Two-stage protocol

### Stage 1 — Exploration (HPO)

| Setting | Value |
| --- | --- |
| Trials | 20 |
| Seed | 42 (trial sampler) |
| Data | Train split only for fitting; **validation for scoring** |
| Epochs | Up to 200 with early stopping (patience 15) |
| Metric | validation_macro_demand_MAE |

Procedure:

1. Sample 20 valid hyperparameter vectors uniformly from discrete candidates.
2. Train PF-STGT from scratch per trial (single seed 42).
3. Record validation macro demand MAE and stress MAE.
4. Rank trials; select **top-3** configs as finalists.

### Stage 2 — Confirmation (finalist stability)

| Setting | Value |
| --- | --- |
| Configs | Top 3 from Stage 1 |
| Seeds | [42, 123, 456] per config |
| Runs | 3 × 3 = 9 training runs |
| Selection | Best config by mean val validation_macro_demand_MAE across seeds |

### Stage 3 — Test (implementation phase, not HPO)

- Load best Stage-2 config + best seed checkpoint.
- Evaluate **once** on test split (Phase 10 protocol).

## Why not Grid or Bayesian?

- **Grid:** 19,683 combos with 277 validation rows → severe multiple-comparison overfitting.
- **Bayesian:** Surrogate models unstable on small val sets; less reproducible across library versions.
- **Random:** Standard for moderate-dimensional DL HPO (Bergstra & Bengio, 2012); fully logged and replayable.

## Reproducibility requirements

```
optimization/trial_manifest.csv   # all 20 Stage-1 configs + val scores
optimization/finalist_configs.yaml
optimization/hpo_log_seed42.json
```
