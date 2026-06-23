# Phase 05A — Feature Engineering Blueprint

## Objective

Design the complete feature engineering strategy before implementation.

The goal is to define every candidate feature, its mathematical formulation, scientific justification, expected impact, and implementation priority.

No features should be created in this phase.

---

## Input

data/processed/

* train.parquet
* validation.parquet
* test.parquet

---

## Scope

### Allowed

* Review existing features
* Design new engineered features
* Define mathematical formulas
* Categorize feature types
* Estimate feature importance
* Identify novel research features
* Create implementation roadmap

### Not Allowed

* Generate new features
* Modify datasets
* Train models
* Perform feature selection
* Build graphs

---

## Required Categories

For every proposed feature include:

1. Feature Name

2. Feature Category

Examples

* Temporal
* Statistical
* Grid
* Regional
* Weather
* Operational
* Graph Candidate

3. Mathematical Definition

4. Required Input Columns

5. Expected Output Type

6. Scientific Motivation

7. Why useful for STGT

8. Generic or Novel

9. Implementation Difficulty

10. Priority

High

Medium

Low

---

## Deliverables

docs/methodology/

Feature_Engineering_Blueprint.md

results/phases/

phase_05A_feature_blueprint/

* feature_inventory.csv
* feature_priority.csv
* feature_formula_catalog.md
* novelty_analysis.md
* blueprint_summary.md

---

## Definition of Done

✔ Existing features reviewed

✔ Candidate features defined

✔ Mathematical formulas documented

✔ Novelty identified

✔ Implementation priorities assigned

✔ Ready for Phase 05B

---

## Execution Record

### Completion Date

2026-06-16

### Processed Dataset Review

* Reviewed `data/processed/train.parquet` (1,295 × 81): `Date` + 42 scaled numerics + 38 one-hot categoricals.
* **10 baseline feature groups** documented (existing Phase 04 outputs — retained, not re-engineered).
* All 45 original clean-dataset columns represented in the preprocessed schema.

### Candidate Features Defined

* **104 proposed engineered features** (after per-region expansion across 9 divisions).
* **32 unique feature templates** spanning 7 categories: Temporal, Statistical, Grid, Regional, Weather, Operational, Graph Candidate.
* Every entry includes all 10 required fields: name, category, formula, inputs, output type, motivation, STGT relevance, generic/novel, difficulty, priority.

### Priority Distribution (proposed only)

| priority | count | Phase 05B batch |
| --- | --- | --- |
| High | 65 | Batch 1 — Core |
| Medium | 37 | Batch 2 — Extended |
| Low | 2 | Batch 3 — Graph/auxiliary |

### Novelty Assessment

* **25 novel** research-motivated features (e.g., `operational_stress_index`, gap-aware lags, `regional_accounting_residual`, `substation_generation_spread`, spatial stress extent indicators).
* **79 generic** features for literature comparability and ablation baselines.
* Full analysis in `results/phases/phase_05A_feature_blueprint/novelty_analysis.md`.

### Key Blueprint Decisions

1. Engineer from `data/interim/bangladesh_smartgrid_clean.parquet` (unscaled) in Phase 05B; apply train-only scaling after feature creation.
2. Use **observed-row lags** (not calendar-day lags) to respect 17 calendar gaps from Phase 03.
3. Preserve Phase 03 physical anomalies via `regional_accounting_residual` — do not discard rows.
4. Graph Candidate features (correlation adjacency, geographic prior, pairwise gradients) are specified for Phase 06+ graph construction, not implemented as node tensors in 05B.
5. Multi-task targets: regional/national demand (regression), `{r}_load` (sparse/zero-inflated), operational stress (composite/binary).

### Deliverables Generated

Master blueprint — `docs/methodology/Feature_Engineering_Blueprint.md`

Reports — `results/phases/phase_05A_feature_blueprint/`:

* `feature_inventory.csv` (114 entries)
* `feature_priority.csv`
* `feature_formula_catalog.md`
* `novelty_analysis.md`
* `blueprint_summary.md`

Script (design only): `scripts/phase_05A_feature_blueprint.py`

### Scope Compliance

* **No features created.** No datasets modified. No models trained. No feature selection. No graphs built.
* Locked phase outputs (Phases 01–04) untouched.

### Recommendations for Phase 05B

* Implement Batch 1 (High priority) first: cyclical temporal, gap-aware lags, rolling means, regional shares/load intensity, grid aggregates, `operational_stress_index`.
* Fit all rolling/statistical parameters on train split only (2019-11-21 → 2023-06-15).
* Save engineered features to `data/processed/` or a new `data/features/` path per project convention, keeping split boundaries intact.
* Run ablation plan outlined in `novelty_analysis.md` during later model phases.

### Status

Ready for Phase 05B.
