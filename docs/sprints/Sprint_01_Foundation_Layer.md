# Sprint 01 — Foundation Layer

## Objective

Implement the foundational data infrastructure required by PF-STGT.

This sprint does NOT implement:

- PF-STGT model
- Training loop
- Evaluation
- Explainability

Only foundational pipelines.

---

## Pipeline P1 — Data Pipeline

Responsibilities:

- Load processed datasets
- Validate schema
- Validate timestamps
- Validate splits

Outputs:

- train.parquet
- validation.parquet
- test.parquet

---

## Pipeline P2 — Feature Pipeline

Responsibilities:

- Load engineered features
- Validate feature set
- Create temporal tensors

Outputs:

- X_temporal

---

## Pipeline P3 — Graph Pipeline

Responsibilities:

- Load hybrid graph
- Load adjacency matrix
- Create graph tensors

Outputs:

- X_graph

---

## Pipeline P4 — Target Pipeline

Responsibilities:

- Generate demand targets
- Generate OSI targets
- Validate target dimensions

Outputs:

- y_demand
- y_osi

---

## Acceptance Criteria

The system must successfully generate:

X_temporal

X_graph

y_demand

y_osi

without errors.

---

## Definition of Done

✔ Pipelines implemented

✔ Unit tests pass

✔ Data validation passes

✔ Tensor generation works

✔ Ready for PF-STGT implementation

---

## Execution Record

### Completion Date

2025-06-25

### Pipelines Implemented

| Pipeline | Package | Modules |
| --- | --- | --- |
| P1 Data | `src/data/` | loader, splits, validators, pipeline |
| P2 Feature | `src/features/` | specs, node/global builders, window, temporal, pipeline |
| P3 Graph | `src/graph/` | adjacency, bias, registry, pipeline |
| P4 Target | `src/targets/` | demand, osi, batch, pipeline |

Supporting: `src/constants.py`, `src/foundation.py`, `src/utils/`

### Acceptance Criteria

| Output | Shape | Status |
| --- | --- | --- |
| X_temporal (node) | (7, 9, 9) | Pass |
| X_temporal (global) | (7, 17) | Pass |
| X_graph (adjacency) | (9, 9) | Pass |
| y_demand | (9,) raw MW | Pass |
| y_osi | scalar ∈ [0, 1] | Pass |

### Tests

- **18/18** unit and integration tests passing (`pytest tests/`)
- Script: `scripts/sprint_01_foundation.py`

### Sample Counts

| Split | Valid samples |
| --- | --- |
| train | 1281 |
| validation | 263 |
| test | 264 |

### Locked Artefacts

All four locked MD5 hashes verified unchanged post-sprint.

### Deliverables

- `results/phases/sprint_01_foundation/sprint_01_report.md`
- `tests/test_*_pipeline.py` (5 test modules)

### Scope Compliance

- Foundation pipelines only — no PF-STGT, training, or explainability.
- Locked phase outputs not modified.

### Status

Ready for Sprint 2 — PF-STGT model core (`src/models/`).