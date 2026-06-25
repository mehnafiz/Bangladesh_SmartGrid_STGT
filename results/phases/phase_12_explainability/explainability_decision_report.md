# Explainability Decision Report — Phase 12

Generated: 2026-06-24

## Selected toolkit

**Hybrid XAI Stack (SHAP-primary + Attention-native + Permutation-validation)**

| method                  |   total_score | role                                     |
|:------------------------|--------------:|:-----------------------------------------|
| SHAP                    |            22 | Primary — feature & stress attribution   |
| Attention Visualization |            21 | Primary — node, temporal, graph analysis |
| Permutation Importance  |            18 | Validation — global sanity check         |

## Why hybrid over single-method?

### SHAP alone (rejected as sole toolkit)
- Strong feature attribution and literature support (NOV-05, 1/55 dedicated SHAP paper).
- Misses native graph/temporal structure exposed by PF-STGT architecture (Phase 09).
- Expensive for full graph-temporal DeepSHAP on entire model.

### Attention alone (rejected as sole toolkit)
- Zero marginal cost at inference; ideal for node/temporal/graph levels.
- Attention ≠ explanation (Jain & Wallace 2019); insufficient for operator-grade stress claims.

### Permutation alone (rejected as sole toolkit)
- Good global validation; ignores temporal window structure and graph dependencies.
- Model-agnostic but expensive and high-variance on small validation set (277 rows).

## Gap alignment

| Gap | Framework response |
| --- | --- |
| GAP-05 | SHAP + attention integrated across both tasks |
| GAP-06 | Stress attribution via SHAP + c1/c2/c3 decomposition |
| GAP-07 | 11 feature coalitions map to Phase 05B groups |
| GAP-02 | Separate demand vs stress explanation paths |
