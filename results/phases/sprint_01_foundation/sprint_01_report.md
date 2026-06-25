# Sprint 01 — Foundation Layer Report

Generated: 2026-06-24
Status: **COMPLETE**

## Scope

Implemented P1–P4 foundation pipelines only. No PF-STGT, training, or explainability.

## Pipelines implemented

| Pipeline | Package | Status |
| --- | --- | --- |
| P1 Data | `src/data/` | Complete |
| P2 Feature | `src/features/` | Complete |
| P3 Graph | `src/graph/` | Complete |
| P4 Target | `src/targets/` | Complete |

## Acceptance criteria

### Split: train

- X_temporal node shape: `(7, 9, 9)`
- X_temporal global shape: `(7, 17)`
- X_graph adjacency shape: `(9, 9)`
- y_demand shape: `(9,)`
- y_osi value: `0.1814`

### Split: validation

- X_temporal node shape: `(7, 9, 9)`
- X_temporal global shape: `(7, 17)`
- X_graph adjacency shape: `(9, 9)`
- y_demand shape: `(9,)`
- y_osi value: `0.2402`

### Split: test

- X_temporal node shape: `(7, 9, 9)`
- X_temporal global shape: `(7, 17)`
- X_graph adjacency shape: `(9, 9)`
- y_demand shape: `(9,)`
- y_osi value: `0.3816`

## Tensor contract verification

- INPUT_WINDOW_T = 7
- N_NODES = 9
- NODE_FEATURES_PER_REGION = 9
- GLOBAL_FEATURES = 17
- All acceptance checks passed: **True**

## Sample counts

- train: **1281** valid windowed samples
- validation: **263** valid windowed samples
- test: **264** valid windowed samples

## Locked artefact integrity (post-sprint)

- `data/features/train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16` (unchanged: True)
- `data/interim/bangladesh_smartgrid_clean.parquet` MD5: `4255024d735a91a4b53b2edee203d0ca` (unchanged: True)
- `graphs/adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686` (unchanged: True)

## Modules delivered

```
src/data/        loader, splits, validators, pipeline
src/features/    specs, node/global builders, window, pipeline
src/graph/       adjacency, bias, registry, pipeline
src/targets/     demand, osi, batch, pipeline
src/foundation.py
src/constants.py
src/utils/       logging, md5, exceptions
tests/           unit + integration tests
```

## Next step

Sprint 2 — PF-STGT model core (`src/models/`).
