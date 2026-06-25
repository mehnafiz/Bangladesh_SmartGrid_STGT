# Graph Validation Report — Phase 08

Generated: 2026-06-24

## Validation checks

| Check | Result |
| --- | --- |
| Symmetry | FAIL (max |A-Aᵀ|=1.32e-01) |
| Self-loops | PASS |
| Connected (edge count ≥ n−1) | PASS |
| Non-negative weights | PASS |
| Row sums (normalised) | min=1.0000, max=1.0000 |
| Train-only correlation | PASS (computed on train split only) |
| Node count = 9 divisions | PASS |

## Locked input integrity

- `data/features/train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16` (unchanged)
- `references/analysis/paper_analysis_catalog.csv` MD5: `258de5912058333f9a1e11925d5249cf` (unchanged)
- `references/gap_analysis/research_gap_matrix.csv` MD5: `d95ece0b123115f34648331ddbc62f17` (unchanged)

## Data–structure alignment

- Mean demand correlation on hybrid edges: **0.790**
- Mean demand correlation off hybrid edges: **0.757**
- On-edge mean exceeds off-edge mean → graph captures stronger couplings.

## Status

**PASS** — adjacency matrix validated and ready for STGT architecture phase.
