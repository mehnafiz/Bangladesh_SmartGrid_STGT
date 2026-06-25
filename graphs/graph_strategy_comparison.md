# Graph Strategy Comparison — Phase 08

Generated: 2026-06-24

## Strategies evaluated

1. **Geographical Graph** — binary admin-border adjacency (Phase 05A `static_geographic_adjacency_prior`).
2. **Correlation Graph** — train-only demand Pearson edges with threshold τ=0.65 (Phase 02).
3. **Hybrid Graph** — geographic structure + correlation weights; extra edges when ρ≥0.85 (Phase 06 recommendation).

## Quantitative comparison

| strategy           |   nodes |   undirected_edges |   density |   mean_edge_weight |   min_edge_weight |   max_edge_weight |   mean_demand_corr_on_edges |   mean_demand_corr_off_edges |   mean_corr_geographic_edges | is_connected   |   self_loops |
|:-------------------|--------:|-------------------:|----------:|-------------------:|------------------:|------------------:|----------------------------:|-----------------------------:|-----------------------------:|:---------------|-------------:|
| Geographical Graph |       9 |                 21 |    0.5833 |             0.2143 |            0.125  |            0.3333 |                      0.7759 |                       0.7837 |                       0.7759 | True           |            0 |
| Correlation Graph  |       9 |                 33 |    0.9167 |             0.1364 |            0.1072 |            0.2144 |                      0.7927 |                       0.6303 |                       0.7759 | True           |            0 |
| Hybrid Graph       |       9 |                 24 |    0.6667 |             0.1875 |            0.1046 |            0.2809 |                      0.7901 |                       0.7573 |                       0.7759 | True           |            0 |

## Qualitative scoring (1–5 per dimension)

| strategy           |   scientific_validity |   literature_support |   interpretability |   complexity |   stgt_suitability |   total_score | rationale                                                                                                                                                          |
|:-------------------|----------------------:|---------------------:|-------------------:|-------------:|-------------------:|--------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Hybrid Graph       |                     5 |                    5 |                  4 |            4 |                  5 |            23 | Combines Phase 06 geographic prior with train-only demand correlation weights; moderate density (66.67%), higher on-edge than off-edge mean corr (0.790 vs 0.757). |
| Geographical Graph |                     4 |                    3 |                  5 |            4 |                  3 |            19 | Domain-valid admin borders (Phase 05A static_geographic_adjacency_prior) but ignores strong non-border demand coupling (mean off-edge corr 0.784).                 |
| Correlation Graph  |                     4 |                    4 |                  2 |            2 |                  3 |            15 | Dense graph (91.67%) from Phase 02 correlation threshold; high risk of over-smoothing and weak spatial interpretability.                                           |

## Literature & gap evidence

- **Phase 07B:** Graph topology (physical vs correlation) under-specified in 5/55 graph papers.
- **Phase 07C GAP-04:** Inter-regional correlation >0.65 supports data-driven coupling; geographic prior recommended for Bangladesh transfer.
- **Phase 06:** Static geographic prior + dynamic correlation (`rolling_demand_corr_90d`) deferred to this phase.

## Selected strategy

**Hybrid Graph** (highest total score: 23/25).

Combines Phase 06 geographic prior with train-only demand correlation weights; moderate density (66.67%), higher on-edge than off-edge mean corr (0.790 vs 0.757).
