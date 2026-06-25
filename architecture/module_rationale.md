# Module Selection Rationale — Phase 09

Generated: 2026-06-24

## Architecture options evaluated

| architecture_id   | name                                        | spatial           | temporal            | fusion             |   total_score | selected   |
|:------------------|:--------------------------------------------|:------------------|:--------------------|:-------------------|--------------:|:-----------|
| ARCH-A            | GCN-LSTM Multi-Task Baseline                | GCN               | LSTM                | Spatial → Temporal |            14 | False      |
| ARCH-B            | GAT + Temporal Attention (ST-first)         | GAT               | Temporal Attention  | Spatial → Temporal |            18 | False      |
| ARCH-C            | PF-STGT (Parallel-Fusion Graph Transformer) | Graph Transformer | Transformer Encoder | Parallel Fusion    |            27 | True       |

## Spatial module: Graph Transformer (25/25)

- **Literature:** 8/55 High STGT-relevance papers; Graph Transformers topic in corpus (spatiotemporal graph attention-enabled transformer, IJEPES 2024).
- **GAP-04 / NOV-04:** Explicit graph + transformer coupling is the project differentiator.
- **Phase 08:** Hybrid adjacency provides edge weights for attention bias (not just binary GCN).
- **GAP-05:** Self-attention weights exportable for spatial explainability (vs opaque GCN aggregation).
- **Rejected GCN:** Fixed aggregation, no attention maps, weaker STGT alignment.
- **Rejected GAT:** Neighbour-only attention; hybrid graph includes selective long-range ρ≥0.85 edges.

## Temporal module: Transformer Encoder (25/25)

- **Phase 02:** Strong lag-1 autocorrelation (0.924) and weekly seasonality → multi-day context needed.
- **Phase 05B:** lag-7 and rolling-7 features imply T≥7 input window.
- **Literature:** 7/55 transformer-based papers in corpus; temporal transformer backbone in High-relevance GNN papers.
- **Rejected single Temporal Attention:** Insufficient depth for composite seasonal + trend patterns.
- **Rejected causal Temporal Transformer:** No autoregressive decoding at h=1; full window encoding suffices.

## Fusion: Parallel Fusion (23/25)

- **Phase 02 dual driver:** shared national trend (temporal path) + inter-regional correlation (spatial path).
- **Multi-task:** stress head benefits from global temporal context AND spatial stress propagation simultaneously.
- **Rejected Spatial→Temporal:** Premature spatial mixing may attenuate node-specific temporal trajectories before fusion.
- **Rejected Temporal→Spatial:** Delays modelling of same-day cross-region demand coupling.

## Selected stack: PF-STGT (27/27 component sum)

Combines highest-scoring spatial, temporal, and fusion modules with multi-task heads aligned to Phase 08.5.
