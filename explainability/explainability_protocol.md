# Explainability Protocol — Phase 12

Generated: 2026-06-24
Status: **FROZEN**

## Execution workflow (implementation phase)

```
1. Load frozen S2 checkpoint (Exp03 A6) — see architecture_freeze_revision/final_model_specification.md
2. Select 20 case-study dates (stratified from validation + test)
3. Export attention maps (spatial + temporal) for each date
4. Compute GradientSHAP for demand (9 regions) and stress (global)
5. Compute permutation importance on validation (global ranking)
6. Cross-validate: SHAP top groups vs permutation top groups (Spearman ρ)
7. Stress: compare SHAP drivers vs OSI c1/c2/c3 decomposition
8. Generate manuscript figures from results/explainability/
```

## Case-study selection (frozen)

| Stratum | Count | Selection rule |
| --- | --- | --- |
| High OSI | 5 | Top decile OSI(t+1) on validation |
| Low OSI | 5 | Bottom decile |
| Peak demand | 5 | Top decile total_regional_demand |
| Shedding event | 5 | any_regional_shedding=1 |

## Attribution levels → methods mapping

| Level | Method(s) | Metric output |
| --- | --- | --- |
| L1 Feature | SHAP + Permutation | φ values, importance rank |
| L2 Node | SHAP coalitions + spatial attention | node_importance.csv |
| L3 Temporal | Temporal attention | α_t per lag day |
| L4 Graph | Spatial attention + A_ij overlay | influence_matrix.csv |
| L5 Stress | SHAP + c1/c2/c3 decomposition | stress_driver labels |

## Quality checks

1. **Leakage audit:** no OSI(t) in SHAP input tensor for OSI(t+1) explanation.
2. **Stability:** bootstrap 10 backgrounds → report SHAP rank correlation > 0.7.
3. **Attention–SHAP agreement:** same top-2 feature groups on ≥60% case studies.
4. **Graph prior alignment:** Spearman(attention, A) > 0.3 on **correlation** edges (S2 graph).

## Manuscript integration (Phase 16 placeholder)

- Figure: spatial attention heatmap on Bangladesh 9-node layout.
- Figure: SHAP beeswarm for stress (grouped G1–G11).
- Table: stress driver classification vs SHAP top group agreement rate.
