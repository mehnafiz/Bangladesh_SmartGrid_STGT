# Graph Decision Rationale — Phase 08

Generated: 2026-06-24

## Decision

**Selected strategy: Hybrid Graph** (score 23/25).

## Why not Geographical Graph alone?

- Valid domain prior but uniform edge weights ignore heterogeneous coupling strength.
- Includes geographically adjacent yet weakly correlated pairs (e.g., Dhaka–Rangpur ρ≈0.62).
- Misses strong non-border coupling unless augmented (Barishal–Cumilla ρ≈0.93 is border-adjacent, but other high-ρ pairs may not be).

## Why not Correlation Graph alone?

- Threshold τ=0.65 yields 33/36 edges (91.7% density) — near-complete graph.
- Phase 07B notes correlation-only topology is under-specified for transfer and interpretability.
- High density increases STGT message-passing complexity and over-smoothing risk.

## Why Hybrid Graph?

Combines Phase 06 geographic prior with train-only demand correlation weights; moderate density (66.67%), higher on-edge than off-edge mean corr (0.790 vs 0.757).

- Aligns Phase 06 guidance: static geographic prior + dynamic correlation weighting.
- Addresses Phase 07C GAP-04 (graph coupling + Bangladesh context) without architecture design.
- Balanced density (66.7%, 24/36 possible edges) with interpretable edge rules.

## Hybrid construction (final)

```
w_ij = ρ_ij  if geo_ij = 1 OR ρ_ij ≥ 0.85
w_ij = 0     otherwise
A = row_normalize(W)
```

## Next phase

Proceed to STGT architecture design using this adjacency matrix; do not alter locked features.
