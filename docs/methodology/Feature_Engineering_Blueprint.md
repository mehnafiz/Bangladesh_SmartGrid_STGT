# Feature Engineering Blueprint — Bangladesh Smart Grid STGT

**Phase:** 05A (Design Only)  
**Date:** 2026-06-16  
**Status:** Ready for Phase 05B implementation

---

## 1. Purpose

This document defines the complete feature engineering strategy for the Explainable Spatio-Temporal Graph Transformer (STGT) multi-task framework. It synthesises findings from Phases 01–04 and specifies every baseline and candidate feature with mathematical formulation, scientific motivation, STGT relevance, novelty assessment, and implementation priority.

**No features are created in Phase 05A.**

## 2. Research Context (from completed phases)

| finding | source | blueprint implication |
| --- | --- | --- |
| 1,850 daily rows, 9 regions, 45 raw cols | Phase 01 | 9 graph nodes with demand/supply/load triplets |
| Strong trend + month-9 seasonality | Phase 02 | Cyclical temporal + trend features (High priority) |
| Load-shedding sparse/imbalanced | Phase 01–02 | Separate task targets + event indicators |
| 17 calendar gaps | Phase 03 | Gap-aware lags, gap_days feature |
| Physical anomalies preserved | Phase 03 | regional_accounting_residual feature |
| Chronological 70/15/15 split | Phase 04 | Train-only fit for all rolling/stat params |
| 80 preprocessed features | Phase 04 | Baseline retained; engineer from clean/interim |

## 3. Existing Feature Review (Phase 04 baseline)

The processed train split contains **81 columns** (Date + 42 scaled numerics + 38 one-hot encoded categoricals). These are **retained as baseline inputs** and are not re-engineered in 05B unless supplemented by new features from the clean interim dataset.

### 3.1 Baseline inventory summary

| group | count | category | priority |
| --- | --- | --- | --- |
| Date (temporal index) | 1 | Temporal | High |
| Year, Month (calendar numerics) | 1 | Temporal | High |
| National generation & peak demand metrics (7 cols) | 7 | Grid | High |
| Operational limitation drivers (5 cols) | 5 | Operational | High |
| Regional demand per node (9 cols) | 9 | Regional | High |
| Regional supply per node (9 cols) | 9 | Regional | Medium |
| Regional load-shedding per node (9 cols) | 9 | Operational | High |
| Day-of-week one-hot (7 cols) | 7 | Temporal | Medium |
| Holiday name one-hot (~28 train categories) | ~28 | Temporal | Medium |
| Holiday category one-hot (4 cols) | 4 | Temporal | Low |

## 4. Proposed Engineered Features

**104 candidate features** (after per-region expansion) across 7 categories:

- **Temporal:** 33 features
- **Regional:** 28 features
- **Statistical:** 27 features
- **Grid:** 6 features
- **Operational:** 4 features
- **Graph Candidate:** 4 features
- **Weather:** 2 features

### 4.1 Implementation priority tiers

- **High (Batch 1):** Temporal cyclical, gap-aware lags, rolling means, regional shares/load intensity, national aggregates, generation reserve, operational limitation composite, OSI, shedding indicators.
- **Medium (Batch 2):** Rolling std, z-scores, accounting residuals, weather anomalies, generation ratios, spatial dispersion.
- **Low (Batch 3):** Graph candidate edge weights, geographic prior, pairwise gradients.

### 4.2 Leakage prevention (mandatory for 05B)

1. Compute all rolling/lag/statistical features using **past observations only**.
2. Fit any normalisation parameters (e.g., monthly temperature means, OSI weights) **on train split only**.
3. Apply identical transformations to validation/test without refitting.
4. Use observed-row lags across calendar gaps — never forward-fill across splits.

### 4.3 Multi-task target mapping

| task head | primary targets | auxiliary engineered |
| --- | --- | --- |
| Demand regression | `{r}_demand`, national eve peak | demand_lag_*, rolling_mean_7 |
| Load-shedding | `{r}_load` | load_lag_1, regional_load_intensity, any_regional_shedding |
| Operational stress | composite | operational_stress_index, generation_reserve, TOL |

## 5. Full Feature Registry

See `results/phases/phase_05A_feature_blueprint/feature_inventory.csv` for the complete registry with all 10 required fields per feature.

## 6. Novel Research Features

Priority novel candidates for manuscript contribution:

1. **operational_stress_index** — multi-constraint composite aligned with multi-task objective.
2. **gap_days_since_previous_observation** + **gap-aware demand_lag_7** — irregular calendar handling.
3. **regional_accounting_residual** — preserves Phase 03 metering anomalies for explainability.
4. **substation_generation_spread** — grid loss / metering divergence proxy.
5. **shedding_region_count** + **spatial_demand_dispersion** — spatial extent of stress events.

See `novelty_analysis.md` for full assessment.

## 7. Phase 05B Roadmap

| batch | features | estimated new columns |
| --- | --- | --- |
| 1 (High) | cyclical, lags, rolling mean, shares, grid aggregates, OSI | ~60–80 |
| 2 (Medium) | std, z-score, residuals, weather, ratios | ~30–40 |
| 3 (Low) | graph edge candidates (separate artifacts) | matrices |

## 8. References to deliverables

- `feature_inventory.csv` — full registry
- `feature_priority.csv` — implementation order
- `feature_formula_catalog.md` — detailed formulas
- `novelty_analysis.md` — generic vs novel assessment
- `blueprint_summary.md` — executive summary
