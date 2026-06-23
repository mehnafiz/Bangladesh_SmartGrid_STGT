"""Phase 05A — Feature Engineering Blueprint (DESIGN ONLY).

Reviews existing preprocessed features and documents the complete feature
engineering strategy for Phase 05B. Does NOT create features, modify datasets,
train models, perform selection, or build graphs.

Reads processed splits only to validate column inventory.
Writes blueprint deliverables to docs/methodology/ and
results/phases/phase_05A_feature_blueprint/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_TRAIN = ROOT / "data" / "processed" / "train.parquet"
METHODOLOGY_DIR = ROOT / "docs" / "methodology"
REPORT_DIR = ROOT / "results" / "phases" / "phase_05A_feature_blueprint"

REGIONS = [
    "Dhaka", "Chattogram", "Rajshahi", "Mymensingh", "Sylhet",
    "Barishal", "Rangpur", "Cumilla", "Khulna",
]

NATIONAL = [
    "Max. Demand at eve. peak (Generation end)",
    "Max. Demand at eve. peak (Sub-station end)",
    "Highest Generation (Generation end)",
    "Minimum Generation (Generation end)",
    "Day-peak Generation (Generation end)",
    "Evening-peak Generation (Generation end)",
    "Minimum Generation Forecast up to 8:00 hrs.",
]

EXOGENOUS = [
    "Maximum Temperature in Dhaka was",
    "Gas/LF limitation",
    "Coal supply Limitation",
    "Low water level in Kaptai lake",
    "Plants under shut down/ maintenance",
]

# ---------------------------------------------------------------------------
# Existing baseline feature groups (Phase 04 — retained, not re-engineered)
# ---------------------------------------------------------------------------
EXISTING_GROUPS = [
    {
        "feature_name": "Date (temporal index)",
        "feature_category": "Temporal",
        "mathematical_definition": "t = parsed datetime index; preserved unscaled",
        "required_input_columns": "Date",
        "expected_output_type": "datetime64[ns]",
        "scientific_motivation": "Anchors all time-series and windowing operations.",
        "stgt_relevance": "Required for spatio-temporal sequence construction and chronological batching.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Existing",
    },
    {
        "feature_name": "Year, Month (calendar numerics)",
        "feature_category": "Temporal",
        "mathematical_definition": "Year(t), Month(t) from Date; StandardScaled in Phase 04",
        "required_input_columns": "Year; Month",
        "expected_output_type": "float32 (scaled)",
        "scientific_motivation": "Captures long-term growth and coarse seasonality.",
        "stgt_relevance": "Global context signal for transformer temporal attention.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Existing",
    },
    {
        "feature_name": "National generation & peak demand metrics (7 cols)",
        "feature_category": "Grid",
        "mathematical_definition": "Raw national MW measurements; StandardScaled in Phase 04",
        "required_input_columns": "; ".join(NATIONAL),
        "expected_output_type": "float32 (scaled) × 7",
        "scientific_motivation": "System-wide supply-demand balance at generation and sub-station ends.",
        "stgt_relevance": "Graph-level (global) conditioning vector for multi-node STGT.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Existing",
    },
    {
        "feature_name": "Operational limitation drivers (5 cols)",
        "feature_category": "Operational",
        "mathematical_definition": "Gas/LF, coal, water, shutdown MW limits; StandardScaled",
        "required_input_columns": "; ".join(EXOGENOUS),
        "expected_output_type": "float32 (scaled) × 5",
        "scientific_motivation": "Fuel, water, and maintenance constraints drive supply shortfalls and stress.",
        "stgt_relevance": "Exogenous global stress covariates modulating attention across all nodes.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Existing",
    },
    {
        "feature_name": "Regional demand per node (9 cols)",
        "feature_category": "Regional",
        "mathematical_definition": "D_r(t) MW for each division r; StandardScaled",
        "required_input_columns": "; ".join(f"{r}_demand" for r in REGIONS),
        "expected_output_type": "float32 (scaled) × 9",
        "scientific_motivation": "Primary node-level load signal; dominant predictor of future demand.",
        "stgt_relevance": "Core node feature for graph transformer message passing.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Existing",
    },
    {
        "feature_name": "Regional supply per node (9 cols)",
        "feature_category": "Regional",
        "mathematical_definition": "S_r(t) MW; StandardScaled",
        "required_input_columns": "; ".join(f"{r}_supply" for r in REGIONS),
        "expected_output_type": "float32 (scaled) × 9",
        "scientific_motivation": "Delivered power; closely tracks demand in this dataset.",
        "stgt_relevance": "Node feature; collinear with demand — informs supply-side stress.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Existing",
    },
    {
        "feature_name": "Regional load-shedding per node (9 cols)",
        "feature_category": "Operational",
        "mathematical_definition": "L_r(t) MW unmet demand; StandardScaled; sparse (mostly zero)",
        "required_input_columns": "; ".join(f"{r}_load" for r in REGIONS),
        "expected_output_type": "float32 (scaled) × 9",
        "scientific_motivation": "Direct measure of operational stress / load shedding at node r.",
        "stgt_relevance": "Primary sparse multi-task target and node-level stress indicator.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Existing",
    },
    {
        "feature_name": "Day-of-week one-hot (7 cols)",
        "feature_category": "Temporal",
        "mathematical_definition": "OneHot(Day of the week); fitted on train in Phase 04",
        "required_input_columns": "Day of the week",
        "expected_output_type": "float32 binary × 7",
        "scientific_motivation": "Weekly demand cycle; Friday holiday effect observed in EDA.",
        "stgt_relevance": "Calendar conditioning for temporal attention patterns.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Existing",
    },
    {
        "feature_name": "Holiday name one-hot (~28 train categories)",
        "feature_category": "Temporal",
        "mathematical_definition": "OneHot(Holiday name); handle_unknown=ignore",
        "required_input_columns": "Holiday name",
        "expected_output_type": "float32 binary × ~28",
        "scientific_motivation": "Public/religious holidays alter industrial and commercial load.",
        "stgt_relevance": "Event-based calendar conditioning; reduces Friday-only confounding.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Existing",
    },
    {
        "feature_name": "Holiday category one-hot (4 cols)",
        "feature_category": "Temporal",
        "mathematical_definition": "OneHot(Holiday_cat) for categories 0–3",
        "required_input_columns": "Holiday_cat",
        "expected_output_type": "float32 binary × 4",
        "scientific_motivation": "Compact holiday severity/type encoding.",
        "stgt_relevance": "Lower-dimensional calendar signal vs full holiday name.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Low",
        "status": "Existing",
    },
]

# ---------------------------------------------------------------------------
# Proposed engineered features (Phase 05B — NOT created in 05A)
# ---------------------------------------------------------------------------
def _region_template(base: dict, suffix: str) -> dict:
    """Expand a per-region feature template across 9 nodes."""
    rows = []
    for r in REGIONS:
        row = base.copy()
        row["feature_name"] = f"{base['feature_name']}_{r}"
        row["required_input_columns"] = base["required_input_columns"].replace("{r}", r)
        row["mathematical_definition"] = base["mathematical_definition"].replace("{r}", r)
        row["stgt_relevance"] = base["stgt_relevance"].replace("{r}", r)
        rows.append(row)
    return rows


PROPOSED = [
    {
        "feature_name": "day_of_year_sin",
        "feature_category": "Temporal",
        "mathematical_definition": "sin(2π · doy(t) / 365.25) where doy = day-of-year from Date",
        "required_input_columns": "Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Continuous cyclic encoding of annual seasonality (summer peak month 9 in EDA).",
        "stgt_relevance": "Smooth seasonal inductive bias for temporal self-attention without one-hot month.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "day_of_year_cos",
        "feature_category": "Temporal",
        "mathematical_definition": "cos(2π · doy(t) / 365.25)",
        "required_input_columns": "Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Complementary seasonal phase to day_of_year_sin.",
        "stgt_relevance": "Pairs with sin term for full annual cycle representation.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "trend_index",
        "feature_category": "Temporal",
        "mathematical_definition": "t_idx = (Date - Date_min).days; optionally StandardScaled on train",
        "required_input_columns": "Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Captures ~52% demand growth 2019→2024 observed in Phase 02 EDA.",
        "stgt_relevance": "Explicit trend channel for long-horizon forecasting in transformer.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "is_weekend",
        "feature_category": "Temporal",
        "mathematical_definition": "1 if Day of the week ∈ {Friday, Saturday}; else 0 (Bangladesh weekend pattern)",
        "required_input_columns": "Day of the week",
        "expected_output_type": "int8 / float32",
        "scientific_motivation": "Friday shows lowest mean demand and load-shedding in temporal EDA.",
        "stgt_relevance": "Compact weekly effect complementing one-hot day features.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "gap_days_since_previous_observation",
        "feature_category": "Temporal",
        "mathematical_definition": "Δt = (Date_t - Date_{t-1}).days; first row = NaN or 0",
        "required_input_columns": "Date",
        "expected_output_type": "float32",
        "scientific_motivation": "17 calendar gaps exist (Phase 03); lag windows must respect irregular spacing.",
        "stgt_relevance": "Gap-aware temporal modelling; flags when past lag spans missing days.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "demand_lag_1",
        "feature_category": "Temporal",
        "mathematical_definition": "D_r(t-1) using strictly past observed row (not calendar day if gap)",
        "required_input_columns": "{r}_demand; Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Strong autoregressive structure in daily demand series.",
        "stgt_relevance": "Primary node-level autoregressive input for one-step STGT forecasting.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Medium",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "demand_lag_7",
        "feature_category": "Temporal",
        "mathematical_definition": "D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)",
        "required_input_columns": "{r}_demand; Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Weekly periodicity in daily load profiles.",
        "stgt_relevance": "Weekly cycle channel for temporal attention at node {r}.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Medium",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "load_lag_1",
        "feature_category": "Temporal",
        "mathematical_definition": "L_r(t-1); past observed row only",
        "required_input_columns": "{r}_load; Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Load-shedding events may persist across consecutive stress days.",
        "stgt_relevance": "Autoregressive channel for sparse load-shedding task head.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Medium",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "demand_rolling_mean_7",
        "feature_category": "Statistical",
        "mathematical_definition": "mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params",
        "required_input_columns": "{r}_demand; Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Smooths daily noise; captures short-term level.",
        "stgt_relevance": "Low-frequency node state for message passing.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Medium",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "demand_rolling_std_7",
        "feature_category": "Statistical",
        "mathematical_definition": "std(D_r(t-k)) for k=1..7 observed rows",
        "required_input_columns": "{r}_demand; Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Elevated volatility precedes operational stress.",
        "stgt_relevance": "Node uncertainty signal for stress-assessment task.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Medium",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "demand_zscore_30",
        "feature_category": "Statistical",
        "mathematical_definition": "(D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only",
        "required_input_columns": "{r}_demand; Date",
        "expected_output_type": "float32",
        "scientific_motivation": "Normalised deviation from recent local level; highlights anomaly days.",
        "stgt_relevance": "Node anomaly score feeding operational stress assessment.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "High",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "regional_demand_share",
        "feature_category": "Regional",
        "mathematical_definition": "share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)",
        "required_input_columns": "{r}_demand; all regional demand columns",
        "expected_output_type": "float32 [0,1]",
        "scientific_motivation": "Dhaka ~35.7% of mean demand (Phase 02); spatial allocation of national load.",
        "stgt_relevance": "Normalised node identity for heterogeneous regional scales in STGT.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "regional_load_intensity",
        "feature_category": "Regional",
        "mathematical_definition": "λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW",
        "required_input_columns": "{r}_load; {r}_demand",
        "expected_output_type": "float32 [0,1]",
        "scientific_motivation": "Fraction of demand unmet; sparse but interpretable stress ratio.",
        "stgt_relevance": "Direct normalised target proxy for load-shedding task at node {r}.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "regional_accounting_residual",
        "feature_category": "Regional",
        "mathematical_definition": "δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds",
        "required_input_columns": "{r}_demand; {r}_supply; {r}_load",
        "expected_output_type": "float32",
        "scientific_motivation": "Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting signal.",
        "stgt_relevance": "Diagnostic node feature for explainable stress assessment (not an error to drop).",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "total_regional_demand",
        "feature_category": "Grid",
        "mathematical_definition": "D_total(t) = Σ_r D_r(t)",
        "required_input_columns": "all regional demand columns",
        "expected_output_type": "float32",
        "scientific_motivation": "Aggregate load; tracks national evening-peak trend.",
        "stgt_relevance": "Global graph-level feature broadcast to all nodes.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "total_regional_load",
        "feature_category": "Grid",
        "mathematical_definition": "L_total(t) = Σ_r L_r(t)",
        "expected_output_type": "float32",
        "scientific_motivation": "System-wide load-shedding severity.",
        "stgt_relevance": "Global stress scalar for multi-task heads.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "generation_reserve",
        "feature_category": "Grid",
        "mathematical_definition": "GR(t) = Highest Generation(t) - Max Eve Peak Gen-end(t)",
        "required_input_columns": "Highest Generation (Generation end); Max. Demand at eve. peak (Generation end)",
        "expected_output_type": "float32",
        "scientific_motivation": "Headroom between peak capability and evening demand.",
        "stgt_relevance": "Global supply margin modulating predicted shedding risk.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "generation_utilization",
        "feature_category": "Grid",
        "mathematical_definition": "GU(t) = Max Eve Peak Gen-end(t) / max(Highest Generation(t), ε)",
        "required_input_columns": "Max. Demand at eve. peak (Generation end); Highest Generation (Generation end)",
        "expected_output_type": "float32 [0,1+]",
        "scientific_motivation": "Fraction of available capacity utilised at peak.",
        "stgt_relevance": "Capacity stress ratio for operational assessment.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "substation_generation_spread",
        "feature_category": "Grid",
        "mathematical_definition": "SGS(t) = Max Eve Peak Gen-end(t) - Max Eve Peak Sub-station end(t)",
        "required_input_columns": "Max. Demand at eve. peak (Generation end); Max. Demand at eve. peak (Sub-station end)",
        "expected_output_type": "float32",
        "scientific_motivation": "Transmission/distribution losses and metering differences (16 anomalous rows in Phase 03).",
        "stgt_relevance": "Grid loss proxy for explainable stress decomposition.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "forecast_min_generation_error",
        "feature_category": "Grid",
        "mathematical_definition": "FME(t) = Minimum Generation Forecast(t) - Minimum Generation(t)",
        "required_input_columns": "Minimum Generation Forecast up to 8:00 hrs.; Minimum Generation (Generation end)",
        "expected_output_type": "float32",
        "scientific_motivation": "Dispatch forecast accuracy; under-forecast may precede stress.",
        "stgt_relevance": "Operational intelligence signal for day-ahead stress prediction.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "temperature_anomaly_month",
        "feature_category": "Weather",
        "mathematical_definition": "TA(t) = T(t) - μ_T,month; μ computed on train split only per calendar month",
        "required_input_columns": "Maximum Temperature in Dhaka was; Month",
        "expected_output_type": "float32",
        "scientific_motivation": "Cooling load drives month-9 peak; anomaly vs monthly norm isolates heat waves.",
        "stgt_relevance": "Weather shock covariate for national and Dhaka-proximal nodes.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Medium",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "cooling_degree_proxy",
        "feature_category": "Weather",
        "mathematical_definition": "CDD*(t) = max(0, T(t) - T_base); T_base = 28°C (Bangladesh cooling threshold)",
        "required_input_columns": "Maximum Temperature in Dhaka was",
        "expected_output_type": "float32 ≥ 0",
        "scientific_motivation": "Non-linear temperature effect on air-conditioning-driven demand.",
        "stgt_relevance": "Non-linear exogenous driver for summer peak prediction.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "total_operational_limitation",
        "feature_category": "Operational",
        "mathematical_definition": "TOL(t) = Gas/LF + Coal + Water + Shutdown MW",
        "required_input_columns": "Gas/LF limitation; Coal supply Limitation; Low water level in Kaptai lake; Plants under shut down/ maintenance",
        "expected_output_type": "float32",
        "scientific_motivation": "Combined supply-side constraint magnitude.",
        "stgt_relevance": "Single global stress index input to transformer.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "operational_stress_index",
        "feature_category": "Operational",
        "mathematical_definition": "OSI(t) = w1·(L_total/D_total) + w2·(1-GR/Highest Gen) + w3·TOL/Highest Gen; weights w from train-only normalisation (fixed after fit)",
        "required_input_columns": "total_regional_load; total_regional_demand; generation_reserve; total_operational_limitation; Highest Generation (Generation end)",
        "expected_output_type": "float32",
        "scientific_motivation": "Composite stress aligned with multi-task objective (shedding + operational assessment).",
        "stgt_relevance": "Novel research feature unifying demand, supply margin, and constraints for STGT.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "High",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "any_regional_shedding",
        "feature_category": "Operational",
        "mathematical_definition": "ARS(t) = 1 if ∃r: L_r(t) > 0 else 0",
        "required_input_columns": "all regional load columns",
        "expected_output_type": "int8 / float32 binary",
        "scientific_motivation": "Binary system-level shedding event indicator.",
        "stgt_relevance": "Event-level target/auxiliary for imbalanced load-shedding classification head.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "High",
        "status": "Proposed",
    },
    {
        "feature_name": "shedding_region_count",
        "feature_category": "Operational",
        "mathematical_definition": "SRC(t) = |{r : L_r(t) > 0}|",
        "required_input_columns": "all regional load columns",
        "expected_output_type": "int8 / float32 [0,9]",
        "scientific_motivation": "Spatial extent of load-shedding events.",
        "stgt_relevance": "Multi-node stress breadth signal for graph-level prediction.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "spatial_demand_dispersion",
        "feature_category": "Graph Candidate",
        "mathematical_definition": "SDD(t) = std_r(D_r(t)) / mean_r(D_r(t))",
        "required_input_columns": "all regional demand columns",
        "expected_output_type": "float32",
        "scientific_motivation": "Heterogeneity of load across divisions; high when spatially uneven stress.",
        "stgt_relevance": "Graph-level summary informing adaptive attention over nodes.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "dhaka_dominance_index",
        "feature_category": "Regional",
        "mathematical_definition": "DDI(t) = D_Dhaka(t) / D_total(t)",
        "required_input_columns": "Dhaka_demand; all regional demand columns",
        "expected_output_type": "float32 [0,1]",
        "scientific_motivation": "Capital region concentration; largest single-node share.",
        "stgt_relevance": "Hub-node importance weight for graph transformer.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "rolling_demand_corr_90d",
        "feature_category": "Graph Candidate",
        "mathematical_definition": "ρ_ij(t) = corr(D_i, D_j) over trailing 90 observed days; computed per split without future leakage",
        "required_input_columns": "regional demand columns for nodes i,j; Date",
        "expected_output_type": "float32 matrix (edge weights)",
        "scientific_motivation": "Phase 02 showed >0.65 inter-regional demand correlation; dynamic coupling.",
        "stgt_relevance": "Time-varying edge weights for spatio-temporal graph construction (Phase 06+).",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "High",
        "priority": "Medium",
        "status": "Proposed",
    },
    {
        "feature_name": "static_geographic_adjacency_prior",
        "feature_category": "Graph Candidate",
        "mathematical_definition": "A_ij = 1 if divisions i,j share a border (Bangladesh admin map); else 0; optionally row-normalised",
        "required_input_columns": "region metadata (external lookup table, not in CSV)",
        "expected_output_type": "float32 adjacency matrix",
        "scientific_motivation": "Physical grid topology prior independent of data correlation.",
        "stgt_relevance": "Structural inductive bias for graph transformer message passing.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Medium",
        "priority": "Low",
        "status": "Proposed",
    },
    {
        "feature_name": "pairwise_demand_gradient",
        "feature_category": "Graph Candidate",
        "mathematical_definition": "G_ij(t) = |D_i(t) - D_j(t)| / max(D_total(t), ε)",
        "required_input_columns": "regional demand columns; total_regional_demand",
        "expected_output_type": "float32 (edge feature)",
        "scientific_motivation": "Instantaneous spatial load imbalance between neighbours.",
        "stgt_relevance": "Dynamic edge feature complementing correlation-based weights.",
        "generic_or_novel": "Novel",
        "implementation_difficulty": "Medium",
        "priority": "Low",
        "status": "Proposed",
    },
    {
        "feature_name": "national_eve_peak_lag_1",
        "feature_category": "Temporal",
        "mathematical_definition": "ND(t-1) for Max Eve Peak Gen-end",
        "required_input_columns": "Max. Demand at eve. peak (Generation end); Date",
        "expected_output_type": "float32",
        "scientific_motivation": "National autoregressive structure complements regional lags.",
        "stgt_relevance": "Global autoregressive channel for graph-level demand forecasting.",
        "generic_or_novel": "Generic",
        "implementation_difficulty": "Low",
        "priority": "Medium",
        "status": "Proposed",
    },
]

# Expand per-region templates
REGIONAL_TEMPLATES = [
    "demand_lag_1", "demand_lag_7", "load_lag_1",
    "demand_rolling_mean_7", "demand_rolling_std_7", "demand_zscore_30",
    "regional_demand_share", "regional_load_intensity", "regional_accounting_residual",
]
TEMPLATE_MAP = {f["feature_name"]: f for f in PROPOSED if f["feature_name"] in REGIONAL_TEMPLATES}

PROPOSED_EXPANDED: list[dict] = []
for feat in PROPOSED:
    if feat["feature_name"] in REGIONAL_TEMPLATES:
        PROPOSED_EXPANDED.extend(_region_template(feat, feat["feature_name"]))
    else:
        PROPOSED_EXPANDED.append(feat)

INVENTORY_COLS = [
    "feature_name", "feature_category", "mathematical_definition",
    "required_input_columns", "expected_output_type", "scientific_motivation",
    "stgt_relevance", "generic_or_novel", "implementation_difficulty",
    "priority", "status",
]


def build_inventory_df() -> pd.DataFrame:
    rows = EXISTING_GROUPS + PROPOSED_EXPANDED
    return pd.DataFrame(rows, columns=INVENTORY_COLS)


def build_priority_df(inventory: pd.DataFrame) -> pd.DataFrame:
    proposed = inventory[inventory["status"] == "Proposed"].copy()
    order = {"High": 0, "Medium": 1, "Low": 2}
    proposed["priority_rank"] = proposed["priority"].map(order)
    proposed = proposed.sort_values(["priority_rank", "implementation_difficulty"])
    proposed["implementation_order"] = range(1, len(proposed) + 1)
    batch_map = {"High": "Batch 1 — Core", "Medium": "Batch 2 — Extended", "Low": "Batch 3 — Graph/auxiliary"}
    proposed["phase_05B_batch"] = proposed["priority"].map(batch_map)
    return proposed[
        ["feature_name", "feature_category", "priority", "implementation_difficulty",
         "implementation_order", "phase_05B_batch", "generic_or_novel", "status"]
    ]


def write_formula_catalog(inventory: pd.DataFrame) -> None:
    lines = ["# Phase 05A — Feature Formula Catalog", ""]
    for status in ("Existing", "Proposed"):
        subset = inventory[inventory["status"] == status]
        lines += [f"## {status} Features", ""]
        for _, r in subset.iterrows():
            lines += [
                f"### {r['feature_name']}",
                "",
                f"- **Category:** {r['feature_category']}",
                f"- **Formula:** {r['mathematical_definition']}",
                f"- **Inputs:** {r['required_input_columns']}",
                f"- **Output type:** {r['expected_output_type']}",
                f"- **Priority:** {r['priority']} | **Difficulty:** {r['implementation_difficulty']}",
                "",
            ]
    (REPORT_DIR / "feature_formula_catalog.md").write_text("\n".join(lines) + "\n")


def write_novelty_analysis(inventory: pd.DataFrame) -> None:
    novel = inventory[inventory["generic_or_novel"] == "Novel"]
    generic = inventory[inventory["generic_or_novel"] == "Generic"]
    lines = [
        "# Phase 05A — Novelty Analysis",
        "",
        "## Summary",
        "",
        f"- Total inventory entries: **{len(inventory)}**",
        f"- Existing (Phase 04 baseline groups): **{len(inventory[inventory['status']=='Existing'])}**",
        f"- Proposed engineered features: **{len(inventory[inventory['status']=='Proposed'])}**",
        f"- Novel research features: **{len(novel[novel['status']=='Proposed'])}**",
        f"- Generic / literature-standard features: **{len(generic[generic['status']=='Proposed'])}**",
        "",
        "## Novel Features (research contribution candidates)",
        "",
        "These features are specifically motivated by Bangladesh grid characteristics "
        "and the multi-task STGT framework:",
        "",
        "| feature | category | priority | motivation |",
        "| --- | --- | --- | --- |",
    ]
    for _, r in novel[novel["status"] == "Proposed"].iterrows():
        mot = r["scientific_motivation"][:80] + ("…" if len(r["scientific_motivation"]) > 80 else "")
        lines.append(f"| {r['feature_name']} | {r['feature_category']} | {r['priority']} | {mot} |")
    lines += [
        "",
        "## Generic Features (baseline comparability)",
        "",
        "Standard temporal, statistical, and grid features ensure comparability with "
        "prior load-forecasting literature and ablation against the novel components.",
        "",
        "## Recommended ablation in later phases",
        "",
        "- Remove `operational_stress_index` to test composite vs decomposed constraints.",
        "- Remove gap-aware lags (`gap_days_since_previous_observation`, `demand_lag_7`) "
        "to quantify calendar-gap handling benefit.",
        "- Remove `regional_accounting_residual` to test Phase 03 anomaly preservation value.",
    ]
    (REPORT_DIR / "novelty_analysis.md").write_text("\n".join(lines) + "\n")


def write_blueprint_summary(inventory: pd.DataFrame, train_cols: list[str]) -> None:
    n_existing = len(inventory[inventory["status"] == "Existing"])
    n_proposed = len(inventory[inventory["status"] == "Proposed"])
    n_high = len(inventory[(inventory["status"] == "Proposed") & (inventory["priority"] == "High")])
    lines = [
        "# Phase 05A — Blueprint Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Processed train schema reviewed: **{len(train_cols)} columns** in `train.parquet`",
        f"- Existing baseline groups documented: **{n_existing}**",
        f"- Proposed engineered features: **{n_proposed}** (expanded per-region where applicable)",
        f"- High-priority proposed features: **{n_high}**",
        "",
        "## Scope compliance",
        "",
        "- Design-only phase: **no features created**, no datasets modified.",
        "- Locked phase outputs (Phases 01–04) untouched.",
        "",
        "## Phase 05B implementation rules (derived from Phases 03–04)",
        "",
        "1. Engineer on `data/interim/bangladesh_smartgrid_clean.parquet` (unscaled raw values) "
        "then apply scaling with train-only fit — OR engineer on clean data before Phase 04-style scaling.",
        "2. All rolling/lag/statistical features: **past-only windows**, no future leakage.",
        "3. Gap-aware lags use **observed-row offsets**, not calendar days (17 gaps documented).",
        "4. Do not remove Phase 03 preserved anomalies; encode via `regional_accounting_residual`.",
        "5. Graph Candidate features feed Phase 06+ graph construction — not node tensors in 05B.",
        "",
        "## Target formulation (for 05B alignment)",
        "",
        "| task | target columns | type |",
        "| --- | --- | --- |",
        "| Regional demand forecast | `{r}_demand` | continuous regression |",
        "| National peak forecast | `Max. Demand at eve. peak (Generation end)` | continuous regression |",
        "| Load-shedding intensity | `{r}_load`, `regional_load_intensity` | sparse / zero-inflated |",
        "| Operational stress | `operational_stress_index`, `any_regional_shedding` | composite / binary |",
        "",
        "## Deliverables",
        "",
        "- `docs/methodology/Feature_Engineering_Blueprint.md`",
        "- `results/phases/phase_05A_feature_blueprint/feature_inventory.csv`",
        "- `results/phases/phase_05A_feature_blueprint/feature_priority.csv`",
        "- `results/phases/phase_05A_feature_blueprint/feature_formula_catalog.md`",
        "- `results/phases/phase_05A_feature_blueprint/novelty_analysis.md`",
        "- `results/phases/phase_05A_feature_blueprint/blueprint_summary.md`",
    ]
    (REPORT_DIR / "blueprint_summary.md").write_text("\n".join(lines) + "\n")


def write_master_blueprint(inventory: pd.DataFrame, train_cols: list[str]) -> None:
    n_prop = inventory[inventory["status"] == "Proposed"]
    cats = n_prop["feature_category"].value_counts()
    lines = [
        "# Feature Engineering Blueprint — Bangladesh Smart Grid STGT",
        "",
        "**Phase:** 05A (Design Only)  ",
        f"**Date:** {datetime.now(timezone.utc).date().isoformat()}  ",
        "**Status:** Ready for Phase 05B implementation",
        "",
        "---",
        "",
        "## 1. Purpose",
        "",
        "This document defines the complete feature engineering strategy for the "
        "Explainable Spatio-Temporal Graph Transformer (STGT) multi-task framework. "
        "It synthesises findings from Phases 01–04 and specifies every baseline and "
        "candidate feature with mathematical formulation, scientific motivation, STGT "
        "relevance, novelty assessment, and implementation priority.",
        "",
        "**No features are created in Phase 05A.**",
        "",
        "## 2. Research Context (from completed phases)",
        "",
        "| finding | source | blueprint implication |",
        "| --- | --- | --- |",
        "| 1,850 daily rows, 9 regions, 45 raw cols | Phase 01 | 9 graph nodes with demand/supply/load triplets |",
        "| Strong trend + month-9 seasonality | Phase 02 | Cyclical temporal + trend features (High priority) |",
        "| Load-shedding sparse/imbalanced | Phase 01–02 | Separate task targets + event indicators |",
        "| 17 calendar gaps | Phase 03 | Gap-aware lags, gap_days feature |",
        "| Physical anomalies preserved | Phase 03 | regional_accounting_residual feature |",
        "| Chronological 70/15/15 split | Phase 04 | Train-only fit for all rolling/stat params |",
        "| 80 preprocessed features | Phase 04 | Baseline retained; engineer from clean/interim |",
        "",
        "## 3. Existing Feature Review (Phase 04 baseline)",
        "",
        f"The processed train split contains **{len(train_cols)} columns** "
        "(Date + 42 scaled numerics + 38 one-hot encoded categoricals). "
        "These are **retained as baseline inputs** and are not re-engineered in 05B unless "
        "supplemented by new features from the clean interim dataset.",
        "",
        "### 3.1 Baseline inventory summary",
        "",
        "| group | count | category | priority |",
        "| --- | --- | --- | --- |",
    ]
    for _, r in inventory[inventory["status"] == "Existing"].iterrows():
        cnt = r["expected_output_type"].split("×")[-1].strip().rstrip(")") if "×" in r["expected_output_type"] else "1"
        lines.append(f"| {r['feature_name']} | {cnt} | {r['feature_category']} | {r['priority']} |")

    lines += [
        "",
        "## 4. Proposed Engineered Features",
        "",
        f"**{len(n_prop)} candidate features** (after per-region expansion) across "
        f"{len(cats)} categories:",
        "",
    ]
    for cat, cnt in cats.items():
        lines.append(f"- **{cat}:** {cnt} features")

    lines += [
        "",
        "### 4.1 Implementation priority tiers",
        "",
        "- **High (Batch 1):** Temporal cyclical, gap-aware lags, rolling means, "
        "regional shares/load intensity, national aggregates, generation reserve, "
        "operational limitation composite, OSI, shedding indicators.",
        "- **Medium (Batch 2):** Rolling std, z-scores, accounting residuals, "
        "weather anomalies, generation ratios, spatial dispersion.",
        "- **Low (Batch 3):** Graph candidate edge weights, geographic prior, pairwise gradients.",
        "",
        "### 4.2 Leakage prevention (mandatory for 05B)",
        "",
        "1. Compute all rolling/lag/statistical features using **past observations only**.",
        "2. Fit any normalisation parameters (e.g., monthly temperature means, OSI weights) "
        "**on train split only**.",
        "3. Apply identical transformations to validation/test without refitting.",
        "4. Use observed-row lags across calendar gaps — never forward-fill across splits.",
        "",
        "### 4.3 Multi-task target mapping",
        "",
        "| task head | primary targets | auxiliary engineered |",
        "| --- | --- | --- |",
        "| Demand regression | `{r}_demand`, national eve peak | demand_lag_*, rolling_mean_7 |",
        "| Load-shedding | `{r}_load` | load_lag_1, regional_load_intensity, any_regional_shedding |",
        "| Operational stress | composite | operational_stress_index, generation_reserve, TOL |",
        "",
        "## 5. Full Feature Registry",
        "",
        "See `results/phases/phase_05A_feature_blueprint/feature_inventory.csv` for the "
        "complete registry with all 10 required fields per feature.",
        "",
        "## 6. Novel Research Features",
        "",
        "Priority novel candidates for manuscript contribution:",
        "",
        "1. **operational_stress_index** — multi-constraint composite aligned with multi-task objective.",
        "2. **gap_days_since_previous_observation** + **gap-aware demand_lag_7** — irregular calendar handling.",
        "3. **regional_accounting_residual** — preserves Phase 03 metering anomalies for explainability.",
        "4. **substation_generation_spread** — grid loss / metering divergence proxy.",
        "5. **shedding_region_count** + **spatial_demand_dispersion** — spatial extent of stress events.",
        "",
        "See `novelty_analysis.md` for full assessment.",
        "",
        "## 7. Phase 05B Roadmap",
        "",
        "| batch | features | estimated new columns |",
        "| --- | --- | --- |",
        "| 1 (High) | cyclical, lags, rolling mean, shares, grid aggregates, OSI | ~60–80 |",
        "| 2 (Medium) | std, z-score, residuals, weather, ratios | ~30–40 |",
        "| 3 (Low) | graph edge candidates (separate artifacts) | matrices |",
        "",
        "## 8. References to deliverables",
        "",
        "- `feature_inventory.csv` — full registry",
        "- `feature_priority.csv` — implementation order",
        "- `feature_formula_catalog.md` — detailed formulas",
        "- `novelty_analysis.md` — generic vs novel assessment",
        "- `blueprint_summary.md` — executive summary",
    ]
    (METHODOLOGY_DIR / "Feature_Engineering_Blueprint.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    METHODOLOGY_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    train = pd.read_parquet(PROCESSED_TRAIN)
    train_cols = list(train.columns)

    inventory = build_inventory_df()
    priority = build_priority_df(inventory)

    inventory.to_csv(REPORT_DIR / "feature_inventory.csv", index=False)
    priority.to_csv(REPORT_DIR / "feature_priority.csv", index=False)
    write_formula_catalog(inventory)
    write_novelty_analysis(inventory)
    write_blueprint_summary(inventory, train_cols)
    write_master_blueprint(inventory, train_cols)

    n_exist = len(inventory[inventory["status"] == "Existing"])
    n_prop = len(inventory[inventory["status"] == "Proposed"])
    n_novel = len(inventory[(inventory["status"] == "Proposed") & (inventory["generic_or_novel"] == "Novel")])

    print("Phase 05A blueprint complete (design only).")
    print(f"Processed columns reviewed: {len(train_cols)}")
    print(f"Inventory entries: {len(inventory)} (existing groups: {n_exist}, proposed: {n_prop})")
    print(f"Novel proposed features: {n_novel}")
    print(f"Master blueprint -> {METHODOLOGY_DIR / 'Feature_Engineering_Blueprint.md'}")
    print(f"Reports -> {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
