# Phase 05A — Blueprint Summary

- Completion date: 2026-06-16
- Processed train schema reviewed: **81 columns** in `train.parquet`
- Existing baseline groups documented: **10**
- Proposed engineered features: **104** (expanded per-region where applicable)
- High-priority proposed features: **65**

## Scope compliance

- Design-only phase: **no features created**, no datasets modified.
- Locked phase outputs (Phases 01–04) untouched.

## Phase 05B implementation rules (derived from Phases 03–04)

1. Engineer on `data/interim/bangladesh_smartgrid_clean.parquet` (unscaled raw values) then apply scaling with train-only fit — OR engineer on clean data before Phase 04-style scaling.
2. All rolling/lag/statistical features: **past-only windows**, no future leakage.
3. Gap-aware lags use **observed-row offsets**, not calendar days (17 gaps documented).
4. Do not remove Phase 03 preserved anomalies; encode via `regional_accounting_residual`.
5. Graph Candidate features feed Phase 06+ graph construction — not node tensors in 05B.

## Target formulation (for 05B alignment)

| task | target columns | type |
| --- | --- | --- |
| Regional demand forecast | `{r}_demand` | continuous regression |
| National peak forecast | `Max. Demand at eve. peak (Generation end)` | continuous regression |
| Load-shedding intensity | `{r}_load`, `regional_load_intensity` | sparse / zero-inflated |
| Operational stress | `operational_stress_index`, `any_regional_shedding` | composite / binary |

## Deliverables

- `docs/methodology/Feature_Engineering_Blueprint.md`
- `results/phases/phase_05A_feature_blueprint/feature_inventory.csv`
- `results/phases/phase_05A_feature_blueprint/feature_priority.csv`
- `results/phases/phase_05A_feature_blueprint/feature_formula_catalog.md`
- `results/phases/phase_05A_feature_blueprint/novelty_analysis.md`
- `results/phases/phase_05A_feature_blueprint/blueprint_summary.md`
