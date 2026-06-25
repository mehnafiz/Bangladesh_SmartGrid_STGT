# Sprint 02 — PF-STGT Core Model Report

Generated: 2026-06-24
Status: **COMPLETE**

## Scope

Implemented PF-STGT core architecture only. No training, evaluation, or explainability.

## Modules delivered

| Module | File |
| --- | --- |
| Graph Transformer | `src/models/graph_transformer.py` |
| Temporal Transformer | `src/models/temporal_transformer.py` |
| Parallel Fusion | `src/models/fusion.py` |
| Multi-task Heads | `src/models/heads.py` |
| PF-STGT Wrapper | `src/models/pf_stgt.py` |

## Hyperparameters (Phase 09 / 11 defaults)

| Parameter | Value |
| --- | --- |
| d_model | 128 |
| num_heads | 4 |
| L_s (spatial layers) | 2 |
| L_t (temporal layers) | 2 |
| ffn_dim | 256 |
| spatial_dropout | 0.1 |
| temporal_dropout | 0.1 |

**Total trainable parameters:** 749,058

## Input contract validation

| Tensor | Expected | Dummy batch |
| --- | --- | --- |
| node_features | (B, 7, 9, 9) | `(2, 7, 9, 9)` |
| global_features | (B, 7, 17) | `(2, 7, 17)` |
| adjacency | (9, 9) | `(9, 9)` |

## Output contract validation

### Dummy batch (B=2)

- demand_pred: `(2, 9)`
- osi_pred: `(2, 1)`
- attn_spatial: `(2, 4, 9, 9)`
- attn_temporal: `(2, 4, 7, 7)`

### Foundation sample (B=1)

- demand_pred: `(1, 9)`
- osi_pred: `(1, 1)`
- OSI range check: [0.5775, 0.5775]

## Tests

```
pytest tests/test_pf_stgt.py tests/test_pf_stgt_integration.py -v
```

## Sprint 01 integrity

Locked artefact MD5 hashes verified unchanged. Sprint 01 modules not modified.

## Next step

Sprint 3 — Training pipeline (`src/training/`).
