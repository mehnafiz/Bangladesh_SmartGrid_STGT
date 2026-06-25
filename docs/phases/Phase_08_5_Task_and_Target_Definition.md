# Phase 08.5 — Task & Target Definition

## Objective

Define all prediction targets before STGT architecture design.

This phase freezes:

* Forecasting target
* Forecast horizon
* Operational stress definition
* Multi-task formulation

---

## Input

* Cleaned Dataset
* Engineered Features
* Research Gap Outputs
* Graph Construction Outputs

---

## Required Decisions

### Forecasting Task

Determine:

* Target variable
* Prediction horizon
* Single-step or multi-step forecasting

---

### Operational Stress Task

Investigate:

* Available stress-related variables
* Reserve margin behaviour
* Demand-supply imbalance
* Load shedding indicators

Evaluate candidate stress formulations.

---

### Candidate Stress Formulations

1. Binary Stress

Normal / Stress

---

2. Multi-Class Stress

Low / Medium / High

---

3. Continuous Stress Score

Regression-based stress index

---

## Multi-Task Definition

Define:

Task 1

Regional Load Forecasting

Task 2

Operational Stress Assessment

Specify:

* Regression or Classification
* Output format
* Training objective

---

## Deliverables

targets/

* forecasting_target_definition.md

* forecasting_horizon_analysis.csv

* stress_definition_analysis.md

* stress_label_distribution.csv

* multitask_formulation.md

results/phases/

phase_08_5_task_definition/

* target_summary.md

* task_validation_report.md

* decision_rationale.md

---

## Definition of Done

✔ Forecast target frozen

✔ Forecast horizon frozen

✔ Stress target frozen

✔ Multi-task formulation frozen

✔ Ready for STGT Architecture

---

## Execution Record

### Completion Date

2026-06-24

### Frozen Decisions

| Item | Decision |
| --- | --- |
| **Forecast target** | 9 × `{Region}_demand` (regional evening-peak demand, MW) |
| **Forecast horizon** | **h = 1 day**, single-step (1-day-ahead) |
| **Stress target** | **Continuous OSI** (Operational Stress Index, [0,1]) |
| **Stress formulation** | SF-04 Continuous Stress Score (24/25) |
| **Multi-task** | Task 1: regional demand regression; Task 2: OSI regression |

### Forecast Horizon Analysis

| h (days) | Mean regional MAPE | Mean regional autocorr |
| --- | --- | --- |
| **1** (selected) | **5.55%** | **0.924** |
| 3 | 7.72% | 0.854 |
| 7 | 8.78% | 0.800 |
| 14 | 10.13% | 0.749 |

h=1 selected: lowest persistence error, strongest autocorrelation, aligns with Phase 05B lag-1 features and daily BPDB cadence (Phase 01).

### Stress Formulation Evaluation

| ID | Formulation | Score (/25) | Selected |
| --- | --- | --- | --- |
| SF-04 | Continuous OSI (composite regression) | **24** | **Yes** |
| SF-02 | Binary (any shedding) | 17 | No |
| SF-03 | Multi-class OSI tertiles | 17 | No |
| SF-01 | Binary (OSI ≥ median) | 16 | No |

**Rationale:** OSI integrates shedding intensity (c₁), reserve margin (c₂), and limitation stack (c₃) per Phase 05B; addresses Phase 07C GAP-06; avoids arbitrary class boundaries.

### Multi-Task Formulation

- **Task 1 — Regional Load Forecasting:** Regression, predict \\(D_r(t+1)\\) for 9 nodes; loss \\(L_1\\) (MAE/Huber).
- **Task 2 — Operational Stress Assessment:** Regression, predict OSI\\(t+1\\); loss \\(L_2\\) (MSE).
- **Joint:** \\(L_{total} = \\lambda_1 L_1 + \\lambda_2 L_2\\) (weights deferred to training phase).

**Leakage note:** Same-day OSI must not be input when predicting OSI(t+1).

### Deliverables Generated

`targets/`:

* `forecasting_target_definition.md`
* `forecasting_horizon_analysis.csv`
* `stress_definition_analysis.md`
* `stress_label_distribution.csv`
* `multitask_formulation.md`

`results/phases/phase_08_5_task_definition/`:

* `target_summary.md`
* `task_validation_report.md`
* `decision_rationale.md`

Script: `scripts/phase_08_5_task_definition.py`

### Scope Compliance

* Task/target definition only.
* **No STGT architecture design** performed.
* **No model training** performed.
* Locked phase outputs unchanged (`train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16`; `bangladesh_smartgrid_clean.parquet` MD5: `4255024d735a91a4b53b2edee203d0ca`; `adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686`).

### Status

Ready for STGT architecture phase.
