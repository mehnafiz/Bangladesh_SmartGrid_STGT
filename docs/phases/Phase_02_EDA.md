# Phase 02 — Exploratory Data Analysis (EDA)

## Objective

Perform a comprehensive exploratory data analysis (EDA) on the original dataset.

The objective is to understand the statistical properties, temporal behavior, regional characteristics, feature relationships, and target distributions without modifying the dataset.

This phase should generate publication-quality figures and scientific observations that may later be used in the manuscript.

---

## Input

data/raw/bangladesh_smartgrid_raw.csv

---

## Prerequisites

* Repository Foundation Locked
* Phase 01 (Data Audit) Locked

---

## Scope

### Allowed

* Descriptive statistics
* Distribution analysis
* Correlation analysis
* Time-series analysis
* Outlier analysis
* Regional comparison
* Missing-value visualization
* Feature interaction analysis
* Temporal trend analysis

### Not Allowed

* Cleaning
* Missing value imputation
* Encoding
* Normalization
* Feature engineering
* Model development
* Graph construction

---

## Deliverables

### Reports

results/phases/phase_02_eda/

* descriptive_statistics.csv
* feature_distribution_summary.md
* correlation_matrix.csv
* temporal_analysis.md
* regional_analysis.md
* outlier_analysis.md
* eda_summary_report.md

### Figures

results/figures/phase_02_eda/

* missing_values.png
* feature_distributions.png
* correlation_heatmap.png
* target_distribution.png
* temporal_trends.png
* regional_comparison.png
* boxplots.png

---

## Phase Report

Update this document after execution.

Include

* Key Findings
* Important Observations
* Potential Research Insights
* Dataset Risks
* Recommendations for Phase 03

---

## Definition of Done

* All required analyses completed
* Publication-quality figures generated
* Reports generated
* Dataset unchanged
* Phase document updated
* Ready for review

---

## Execution Record

### Completion Date

2026-06-16

### Integrity

* Read-only EDA confirmed.
* Source file MD5 unchanged before/after: `28d8594de1b60ba37892e56ae64a8262`
* No cleaning, imputation, encoding, normalization, feature engineering, modelling, or graph construction performed.
* Phase 01 (locked) outputs in `results/phases/phase_01_data_audit/` were not modified.

### Deliverables Generated

Reports — `results/phases/phase_02_eda/`:

* `descriptive_statistics.csv`
* `feature_distribution_summary.md`
* `correlation_matrix.csv`
* `temporal_analysis.md`
* `regional_analysis.md`
* `outlier_analysis.md`
* `eda_summary_report.md`

Figures — `results/figures/phase_02_eda/` (300 DPI):

* `missing_values.png`
* `feature_distributions.png`
* `correlation_heatmap.png`
* `target_distribution.png`
* `temporal_trends.png`
* `regional_comparison.png`
* `boxplots.png`

EDA script (read-only): `scripts/phase_02_eda.py`

### Key Findings

* **Strong multi-year growth trend:** National evening-peak demand rose from ~8,498 MW (2019) to ~12,899 MW (2024) — roughly +52% over the period.
* **Pronounced annual seasonality:** Mean demand peaks in the warm season, highest in **month 9 (September, ~13,470 MW)** and lowest in **month 12 (December, ~9,313 MW)**, driven by cooling load.
* **High spatial correlation:** All regional demand/supply pairs and inter-regional demand correlations exceed ~0.65 (most >0.9), reflecting shared national growth and seasonality.
* **Demand ≈ supply everywhere:** Each region's demand and supply track almost identically, confirming the Phase 01 collinearity observation.
* **Dominant load centre:** Dhaka accounts for ~35.7% of mean total regional demand; Khulna, Chattogram, and Cumilla follow.
* **Sparse, imbalanced load-shedding:** Regional `_load` is non-zero on only a minority of days (most frequent in Mymensingh, least in Barishal), so it behaves as rare-event data rather than a smooth regression target.
* **Complete data:** Zero missing cells and zero duplicates — completeness is not a modelling barrier.

### Important Observations

* Day-of-week effect is mild but consistent: Friday (weekly holiday) has the lowest mean demand and lowest mean load-shedding.
* IQR-based outliers in demand/generation features cluster at the upper tail (record-high demand days) and are genuine extremes, not errors.
* High `_load` "outlier" counts are an artifact of the zero-inflated distribution (rare shedding events), not anomalies.
* Several conceptually equivalent generation/demand fields differ in stored dtype (`int64` vs `float64`) — noted, not modified (read-only phase).

### Potential Research Insights

* The combination of a clear trend, strong seasonality, and high inter-node correlation is well-matched to a **Spatio-Temporal Graph Transformer**: regions as nodes with correlated dynamics plus a shared temporal driver.
* The near-equality of demand and supply suggests demand and supply targets carry largely redundant information; multi-task heads should focus on complementary targets (e.g., demand forecasting + load-shedding event detection).
* Load-shedding is best framed as a **separate, imbalanced task** (zero-inflated regression or event classification) rather than plain regression.

### Dataset Risks

* **Target imbalance** for `_load` (dominant zeros) — risk of a degenerate all-zero predictor; needs explicit handling in modelling phases.
* **Multicollinearity** among demand/supply/generation features may inflate naive feature-importance and destabilize unregularized models.
* **Temporal gaps** (~17 absent calendar days from Phase 01) must be respected when constructing fixed-length time windows.
* **Heteroscedastic regional scales** (Dhaka ≫ Barishal) imply per-node scaling will be needed later (deferred — not done here).

### Recommendations for Phase 03

* Proceed to preprocessing/data-preparation: build a continuous daily calendar index and explicitly flag the missing days (no imputation yet decided here).
* Define the multi-task target set: continuous regional/national demand (regression) + sparse load-shedding (event/zero-inflated task).
* Plan per-node normalization to handle large scale differences between divisions.
* Retain exogenous covariates (temperature, fuel/water/maintenance limitations, calendar, holidays) as conditioning inputs with a leakage-safe temporal split.
* Use the Phase 02 correlation structure to inform initial graph adjacency design in the graph-construction phase.

### Status

Ready for review.
