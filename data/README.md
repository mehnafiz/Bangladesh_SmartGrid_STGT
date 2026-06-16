# data/

**Purpose**
Central store for all datasets across the full data lifecycle, from raw
acquisition through graph-ready representations. Large files are git-ignored.

**Future Contents**
- `raw/` — original, immutable source data.
- `interim/` — partially cleaned / intermediate data.
- `processed/` — final, model-ready datasets.
- `external/` — third-party reference data.
- `graph/` — graph structures (nodes, edges, adjacency).
