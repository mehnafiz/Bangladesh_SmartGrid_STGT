# Sprint 04 — Explainability System Report

Generated: 2026-06-24
Status: **COMPLETE**

## Scope

Implemented PF-STGT explainability infrastructure per Phase 12 design.
No model training, benchmark execution, or full XAI experiments were run.

## Components delivered

### src/explainability/

| Module | Responsibility |
| --- | --- |
| `config.py` | Phase 12 frozen XAI defaults |
| `types.py` | Typed result containers |
| `coalitions.py` | G1–G11 feature coalition registry |
| `shap_engine.py` | GradientSHAP-style grouped attributions |
| `attention_extractor.py` | Spatial/temporal attention aggregation |
| `permutation.py` | Coalition permutation importance |
| `node_attribution.py` | Regional SHAP + attention ranking |
| `temporal_attribution.py` | Lookback α_t and top-k lags |
| `stress_attribution.py` | SHAP + OSI c1/c2/c3 dual pathway |

## Attribution levels (Phase 12)

| Level | Module(s) | Output |
| --- | --- | --- |
| L1 Feature | `ShapEngine`, `PermutationImportance` | Grouped φ, importance rank |
| L2 Node | `NodeAttributor` | node_importance.csv |
| L3 Temporal | `TemporalAttributor` | α_t, top-k lags |
| L4 Graph | `AttentionExtractor` | influence_matrix |
| L5 Stress | `StressAttributor` | driver labels + SHAP groups |

## SHAP design (frozen)

- Method: integrated gradients (GradientSHAP approximation)
- Steps: 50
- Background default: 100 train windows
- Coalitions: G1–G11 leakage-safe groups

## Quality gates (for experiment phase)

- SHAP stability Spearman ≥ 0.7
- Attention–adjacency Spearman ≥ 0.3
- SHAP–permutation Spearman ≥ 0.5

## Output layout (runtime — not generated in this sprint)

```
results/explainability/shap/
results/explainability/attention/
results/explainability/nodes/
results/explainability/stress/
results/explainability/permutation/
```

## Tests

```
pytest tests/test_explainability_coalitions.py tests/test_attention_extractor.py \
       tests/test_shap_engine.py tests/test_permutation_importance.py \
       tests/test_attribution_modules.py -v
```

**54/54** total project tests passing (16 new Sprint 04 tests).

## Locked artefact integrity

- `data/features/train_features.parquet` MD5 unchanged: True
- `data/interim/bangladesh_smartgrid_clean.parquet` MD5 unchanged: True
- `graphs/adjacency_matrix.csv` MD5 unchanged: True

## Sprint 01–03 integrity

Foundation, model, and training modules not modified.

## Next step

Train B07 PF-STGT, load best checkpoint, run Phase 12 protocol on 20 case-study dates.
