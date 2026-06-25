# Node Importance Design — Phase 12

Generated: 2026-06-24
Status: **FROZEN**

## Level 2 — Node-level attribution

### Regional contribution analysis (Task 1)

For each forecast day and target region r*, compute:

1. **SHAP node coalition score:** sum |φ| for groups G1,G3,G4,G5 restricted to node r.
2. **Spatial attention inflow:** Σ_i attn_spatial[i, r*, t] (who influences r*).
3. **Spatial attention outflow:** Σ_j attn_spatial[r*, j, t] (r* influences whom).

### Node ranking table (per case study)

| Column | Definition |
| --- | --- |
| `node` | Division name |
| `shap_mass` | Σ\|φ\| over node-local features |
| `attention_inflow` | Mean incoming attention |
| `attention_outflow` | Mean outgoing attention |
| `demand_share` | regional_demand_share (context) |

### Dhaka emphasis

Always report Dhaka separately (Phase 02: ~35.7% national share); macro rankings can hide hub influence.

### Regional contribution to national forecast

```
Contribution_r = shap_mass_r / sum_r shap_mass_r
Compare to demand_share_r for consistency check
```

### Output

```
results/explainability/nodes/node_importance_{date}.csv
results/explainability/nodes/regional_contribution_ranking.png
```
