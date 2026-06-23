# Phase 05A — Feature Formula Catalog

## Existing Features

### Date (temporal index)

- **Category:** Temporal
- **Formula:** t = parsed datetime index; preserved unscaled
- **Inputs:** Date
- **Output type:** datetime64[ns]
- **Priority:** High | **Difficulty:** Low

### Year, Month (calendar numerics)

- **Category:** Temporal
- **Formula:** Year(t), Month(t) from Date; StandardScaled in Phase 04
- **Inputs:** Year; Month
- **Output type:** float32 (scaled)
- **Priority:** High | **Difficulty:** Low

### National generation & peak demand metrics (7 cols)

- **Category:** Grid
- **Formula:** Raw national MW measurements; StandardScaled in Phase 04
- **Inputs:** Max. Demand at eve. peak (Generation end); Max. Demand at eve. peak (Sub-station end); Highest Generation (Generation end); Minimum Generation (Generation end); Day-peak Generation (Generation end); Evening-peak Generation (Generation end); Minimum Generation Forecast up to 8:00 hrs.
- **Output type:** float32 (scaled) × 7
- **Priority:** High | **Difficulty:** Low

### Operational limitation drivers (5 cols)

- **Category:** Operational
- **Formula:** Gas/LF, coal, water, shutdown MW limits; StandardScaled
- **Inputs:** Maximum Temperature in Dhaka was; Gas/LF limitation; Coal supply Limitation; Low water level in Kaptai lake; Plants under shut down/ maintenance
- **Output type:** float32 (scaled) × 5
- **Priority:** High | **Difficulty:** Low

### Regional demand per node (9 cols)

- **Category:** Regional
- **Formula:** D_r(t) MW for each division r; StandardScaled
- **Inputs:** Dhaka_demand; Chattogram_demand; Rajshahi_demand; Mymensingh_demand; Sylhet_demand; Barishal_demand; Rangpur_demand; Cumilla_demand; Khulna_demand
- **Output type:** float32 (scaled) × 9
- **Priority:** High | **Difficulty:** Low

### Regional supply per node (9 cols)

- **Category:** Regional
- **Formula:** S_r(t) MW; StandardScaled
- **Inputs:** Dhaka_supply; Chattogram_supply; Rajshahi_supply; Mymensingh_supply; Sylhet_supply; Barishal_supply; Rangpur_supply; Cumilla_supply; Khulna_supply
- **Output type:** float32 (scaled) × 9
- **Priority:** Medium | **Difficulty:** Low

### Regional load-shedding per node (9 cols)

- **Category:** Operational
- **Formula:** L_r(t) MW unmet demand; StandardScaled; sparse (mostly zero)
- **Inputs:** Dhaka_load; Chattogram_load; Rajshahi_load; Mymensingh_load; Sylhet_load; Barishal_load; Rangpur_load; Cumilla_load; Khulna_load
- **Output type:** float32 (scaled) × 9
- **Priority:** High | **Difficulty:** Low

### Day-of-week one-hot (7 cols)

- **Category:** Temporal
- **Formula:** OneHot(Day of the week); fitted on train in Phase 04
- **Inputs:** Day of the week
- **Output type:** float32 binary × 7
- **Priority:** Medium | **Difficulty:** Low

### Holiday name one-hot (~28 train categories)

- **Category:** Temporal
- **Formula:** OneHot(Holiday name); handle_unknown=ignore
- **Inputs:** Holiday name
- **Output type:** float32 binary × ~28
- **Priority:** Medium | **Difficulty:** Low

### Holiday category one-hot (4 cols)

- **Category:** Temporal
- **Formula:** OneHot(Holiday_cat) for categories 0–3
- **Inputs:** Holiday_cat
- **Output type:** float32 binary × 4
- **Priority:** Low | **Difficulty:** Low

## Proposed Features

### day_of_year_sin

- **Category:** Temporal
- **Formula:** sin(2π · doy(t) / 365.25) where doy = day-of-year from Date
- **Inputs:** Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### day_of_year_cos

- **Category:** Temporal
- **Formula:** cos(2π · doy(t) / 365.25)
- **Inputs:** Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### trend_index

- **Category:** Temporal
- **Formula:** t_idx = (Date - Date_min).days; optionally StandardScaled on train
- **Inputs:** Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### is_weekend

- **Category:** Temporal
- **Formula:** 1 if Day of the week ∈ {Friday, Saturday}; else 0 (Bangladesh weekend pattern)
- **Inputs:** Day of the week
- **Output type:** int8 / float32
- **Priority:** Medium | **Difficulty:** Low

### gap_days_since_previous_observation

- **Category:** Temporal
- **Formula:** Δt = (Date_t - Date_{t-1}).days; first row = NaN or 0
- **Inputs:** Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### demand_lag_1_Dhaka

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Dhaka_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Chattogram

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Chattogram_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Rajshahi

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Rajshahi_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Mymensingh

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Mymensingh_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Sylhet

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Sylhet_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Barishal

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Barishal_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Rangpur

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Rangpur_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Cumilla

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Cumilla_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_1_Khulna

- **Category:** Temporal
- **Formula:** D_r(t-1) using strictly past observed row (not calendar day if gap)
- **Inputs:** Khulna_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Dhaka

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Dhaka_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Chattogram

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Chattogram_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Rajshahi

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Rajshahi_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Mymensingh

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Mymensingh_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Sylhet

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Sylhet_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Barishal

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Barishal_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Rangpur

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Rangpur_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Cumilla

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Cumilla_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_lag_7_Khulna

- **Category:** Temporal
- **Formula:** D_r(t-7_obs) — 7th preceding observed row (gap-aware, not calendar D-7)
- **Inputs:** Khulna_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Dhaka

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Dhaka_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Chattogram

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Chattogram_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Rajshahi

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Rajshahi_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Mymensingh

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Mymensingh_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Sylhet

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Sylhet_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Barishal

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Barishal_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Rangpur

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Rangpur_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Cumilla

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Cumilla_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### load_lag_1_Khulna

- **Category:** Temporal
- **Formula:** L_r(t-1); past observed row only
- **Inputs:** Khulna_load; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Dhaka

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Dhaka_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Chattogram

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Chattogram_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Rajshahi

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Rajshahi_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Mymensingh

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Mymensingh_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Sylhet

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Sylhet_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Barishal

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Barishal_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Rangpur

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Rangpur_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Cumilla

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Cumilla_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_mean_7_Khulna

- **Category:** Statistical
- **Formula:** mean(D_r(t-k)) for k=1..7 observed rows; min_periods=7; train-only for any fill params
- **Inputs:** Khulna_demand; Date
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### demand_rolling_std_7_Dhaka

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Dhaka_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Chattogram

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Chattogram_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Rajshahi

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Rajshahi_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Mymensingh

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Mymensingh_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Sylhet

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Sylhet_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Barishal

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Barishal_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Rangpur

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Rangpur_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Cumilla

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Cumilla_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_rolling_std_7_Khulna

- **Category:** Statistical
- **Formula:** std(D_r(t-k)) for k=1..7 observed rows
- **Inputs:** Khulna_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Medium

### demand_zscore_30_Dhaka

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Dhaka_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Chattogram

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Chattogram_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Rajshahi

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Rajshahi_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Mymensingh

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Mymensingh_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Sylhet

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Sylhet_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Barishal

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Barishal_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Rangpur

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Rangpur_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Cumilla

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Cumilla_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### demand_zscore_30_Khulna

- **Category:** Statistical
- **Formula:** (D_r(t) - μ_roll30_train) / σ_roll30_train where μ,σ from trailing 30 observed rows; σ fit logic uses past only
- **Inputs:** Khulna_demand; Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** High

### regional_demand_share_Dhaka

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Dhaka_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Chattogram

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Chattogram_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Rajshahi

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Rajshahi_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Mymensingh

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Mymensingh_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Sylhet

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Sylhet_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Barishal

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Barishal_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Rangpur

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Rangpur_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Cumilla

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Cumilla_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_demand_share_Khulna

- **Category:** Regional
- **Formula:** share_r(t) = D_r(t) / Σ_{j∈R} D_j(t)
- **Inputs:** Khulna_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Dhaka

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Dhaka_load; Dhaka_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Chattogram

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Chattogram_load; Chattogram_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Rajshahi

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Rajshahi_load; Rajshahi_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Mymensingh

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Mymensingh_load; Mymensingh_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Sylhet

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Sylhet_load; Sylhet_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Barishal

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Barishal_load; Barishal_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Rangpur

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Rangpur_load; Rangpur_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Cumilla

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Cumilla_load; Cumilla_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_load_intensity_Khulna

- **Category:** Regional
- **Formula:** λ_r(t) = L_r(t) / max(D_r(t), ε); ε=1 MW
- **Inputs:** Khulna_load; Khulna_demand
- **Output type:** float32 [0,1]
- **Priority:** High | **Difficulty:** Low

### regional_accounting_residual_Dhaka

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Dhaka_demand; Dhaka_supply; Dhaka_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Chattogram

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Chattogram_demand; Chattogram_supply; Chattogram_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Rajshahi

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Rajshahi_demand; Rajshahi_supply; Rajshahi_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Mymensingh

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Mymensingh_demand; Mymensingh_supply; Mymensingh_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Sylhet

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Sylhet_demand; Sylhet_supply; Sylhet_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Barishal

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Barishal_demand; Barishal_supply; Barishal_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Rangpur

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Rangpur_demand; Rangpur_supply; Rangpur_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Cumilla

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Cumilla_demand; Cumilla_supply; Cumilla_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### regional_accounting_residual_Khulna

- **Category:** Regional
- **Formula:** δ_r(t) = D_r(t) - S_r(t) - L_r(t); 0 if identity holds
- **Inputs:** Khulna_demand; Khulna_supply; Khulna_load
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### total_regional_demand

- **Category:** Grid
- **Formula:** D_total(t) = Σ_r D_r(t)
- **Inputs:** all regional demand columns
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### total_regional_load

- **Category:** Grid
- **Formula:** L_total(t) = Σ_r L_r(t)
- **Inputs:** nan
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### generation_reserve

- **Category:** Grid
- **Formula:** GR(t) = Highest Generation(t) - Max Eve Peak Gen-end(t)
- **Inputs:** Highest Generation (Generation end); Max. Demand at eve. peak (Generation end)
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### generation_utilization

- **Category:** Grid
- **Formula:** GU(t) = Max Eve Peak Gen-end(t) / max(Highest Generation(t), ε)
- **Inputs:** Max. Demand at eve. peak (Generation end); Highest Generation (Generation end)
- **Output type:** float32 [0,1+]
- **Priority:** Medium | **Difficulty:** Low

### substation_generation_spread

- **Category:** Grid
- **Formula:** SGS(t) = Max Eve Peak Gen-end(t) - Max Eve Peak Sub-station end(t)
- **Inputs:** Max. Demand at eve. peak (Generation end); Max. Demand at eve. peak (Sub-station end)
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### forecast_min_generation_error

- **Category:** Grid
- **Formula:** FME(t) = Minimum Generation Forecast(t) - Minimum Generation(t)
- **Inputs:** Minimum Generation Forecast up to 8:00 hrs.; Minimum Generation (Generation end)
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### temperature_anomaly_month

- **Category:** Weather
- **Formula:** TA(t) = T(t) - μ_T,month; μ computed on train split only per calendar month
- **Inputs:** Maximum Temperature in Dhaka was; Month
- **Output type:** float32
- **Priority:** High | **Difficulty:** Medium

### cooling_degree_proxy

- **Category:** Weather
- **Formula:** CDD*(t) = max(0, T(t) - T_base); T_base = 28°C (Bangladesh cooling threshold)
- **Inputs:** Maximum Temperature in Dhaka was
- **Output type:** float32 ≥ 0
- **Priority:** Medium | **Difficulty:** Low

### total_operational_limitation

- **Category:** Operational
- **Formula:** TOL(t) = Gas/LF + Coal + Water + Shutdown MW
- **Inputs:** Gas/LF limitation; Coal supply Limitation; Low water level in Kaptai lake; Plants under shut down/ maintenance
- **Output type:** float32
- **Priority:** High | **Difficulty:** Low

### operational_stress_index

- **Category:** Operational
- **Formula:** OSI(t) = w1·(L_total/D_total) + w2·(1-GR/Highest Gen) + w3·TOL/Highest Gen; weights w from train-only normalisation (fixed after fit)
- **Inputs:** total_regional_load; total_regional_demand; generation_reserve; total_operational_limitation; Highest Generation (Generation end)
- **Output type:** float32
- **Priority:** High | **Difficulty:** High

### any_regional_shedding

- **Category:** Operational
- **Formula:** ARS(t) = 1 if ∃r: L_r(t) > 0 else 0
- **Inputs:** all regional load columns
- **Output type:** int8 / float32 binary
- **Priority:** High | **Difficulty:** Low

### shedding_region_count

- **Category:** Operational
- **Formula:** SRC(t) = |{r : L_r(t) > 0}|
- **Inputs:** all regional load columns
- **Output type:** int8 / float32 [0,9]
- **Priority:** Medium | **Difficulty:** Low

### spatial_demand_dispersion

- **Category:** Graph Candidate
- **Formula:** SDD(t) = std_r(D_r(t)) / mean_r(D_r(t))
- **Inputs:** all regional demand columns
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

### dhaka_dominance_index

- **Category:** Regional
- **Formula:** DDI(t) = D_Dhaka(t) / D_total(t)
- **Inputs:** Dhaka_demand; all regional demand columns
- **Output type:** float32 [0,1]
- **Priority:** Medium | **Difficulty:** Low

### rolling_demand_corr_90d

- **Category:** Graph Candidate
- **Formula:** ρ_ij(t) = corr(D_i, D_j) over trailing 90 observed days; computed per split without future leakage
- **Inputs:** regional demand columns for nodes i,j; Date
- **Output type:** float32 matrix (edge weights)
- **Priority:** Medium | **Difficulty:** High

### static_geographic_adjacency_prior

- **Category:** Graph Candidate
- **Formula:** A_ij = 1 if divisions i,j share a border (Bangladesh admin map); else 0; optionally row-normalised
- **Inputs:** region metadata (external lookup table, not in CSV)
- **Output type:** float32 adjacency matrix
- **Priority:** Low | **Difficulty:** Medium

### pairwise_demand_gradient

- **Category:** Graph Candidate
- **Formula:** G_ij(t) = |D_i(t) - D_j(t)| / max(D_total(t), ε)
- **Inputs:** regional demand columns; total_regional_demand
- **Output type:** float32 (edge feature)
- **Priority:** Low | **Difficulty:** Medium

### national_eve_peak_lag_1

- **Category:** Temporal
- **Formula:** ND(t-1) for Max Eve Peak Gen-end
- **Inputs:** Max. Demand at eve. peak (Generation end); Date
- **Output type:** float32
- **Priority:** Medium | **Difficulty:** Low

