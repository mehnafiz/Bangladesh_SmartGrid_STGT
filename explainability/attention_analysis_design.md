# Attention Analysis Design — Phase 12

Generated: 2026-06-24
Status: **FROZEN**

## Level 3 — Temporal attribution

### Source

Transformer Encoder self-attention: `attn_temporal` shape `(heads, T, T)` per node (shared weights).

### Aggregation

```
α_t = mean_{heads, nodes}( attn_temporal[:, :, t] )   # contribution of day t to forecast
Report top-k days (k=3) for each case study
```

### Interpretation

- High weight on t (lag-1 day) expected given autocorr 0.924 (Phase 08.5).
- Weight on t−6…t−7 supports rolling-7 / weekly seasonality (Phase 02).

## Level 4 — Graph attention analysis

### Source

Graph Transformer attention: `attn_spatial` shape `(heads, N, N)` per timestep, averaged over T.

### Inter-regional influence matrix

```
I_ij = mean_{heads, t}( attn_spatial[head, i, j, t] )
Overlay on Phase 08 hybrid adjacency A_ij (edge exists if A_ij > 0)
```

### Validation against graph prior

- Compute Spearman ρ between I_ij and hybrid edge weights A_ij on existing edges.
- High ρ supports that learned attention aligns with correlation-geographic structure.

### Visual outputs

```
results/explainability/attention/spatial_heatmap_{date}.png
results/explainability/attention/temporal_bar_{date}.png
results/explainability/attention/adjacency_attention_overlay.png
results/explainability/attention/influence_matrix.csv
```

### Limitations (document in paper)

Attention weights are **explanatory hints**, not guaranteed faithful attributions 
(Jain & Wallace, 2019). Cross-check with SHAP for top features on same case studies.
