# Root Cause Analysis Protocol — Phase 14

Generated: 2026-06-24
Status: **FROZEN**

## Objective

Systematically explain **why** PF-STGT errors occur by triangulating:

1. Feature attribution review (Phase 12 L1 SHAP + Permutation)
2. Attention review (Phase 12 L3–L4 graph/temporal attention)
3. Stress attribution review (Phase 12 L5 OSI component decomposition)

## Trigger conditions

Run root-cause analysis when ANY hold:

| Trigger | Threshold |
| --- | --- |
| High macro error | Daily macro MAE > test p90 |
| Regional outlier | |e_r| > 2 × MAE_r for any region |
| Stress miss | |OSI − OSI_hat| > 0.15 on High-stress day |
| Extreme event | Day flagged in E4 taxonomy |
| Ablation surprise | A2/A3 regional error pattern contradicts hypothesis |

## Three-pathway methodology

### Pathway 1 — Feature attribution review

**Tools:** GradientSHAP grouped coalitions + Permutation importance (Phase 12).

**Procedure:**

1. For flagged day d, compute SHAP for demand head (9 outputs) and stress head.
2. Rank feature groups G1–G11 (Phase 05A batches).
3. Compare top-3 SHAP groups to Permutation top-3 on validation (consistency check).
4. Label root cause if top group maps to known driver:

| SHAP group | Root-cause label |
| --- | --- |
| G1–G2 (lags, rolling) | Temporal memory failure |
| G3–G4 (regional load/intensity) | Shedding / local demand miss |
| G5–G6 (calendar, season) | Seasonal/holiday miss |
| G7–G8 (grid national) | Supply/reserve miss |
| G9–G11 (weather, limitations) | Exogenous shock miss |

**Output:** `feature_attribution_review_{date}.csv`

### Pathway 2 — Attention review

**Tools:** Graph Transformer spatial attention + Temporal Encoder attention (Phase 09/12).

**Procedure:**

1. Export α_ij (spatial) and α_t (temporal) for day d.
2. Compare spatial attention to hybrid adjacency — identify unexpected high-weight edges.
3. Check if error region r receives insufficient attention from neighbors.
4. Compute **attention deficit score**:

```
ADS_r = MAE_r / (Σ_j α_rj + ε)     high ADS → error despite low attention to r
```

5. Cross-check Phase 13 A2: if −Graph ablation error correlates with ADS, graph module failure confirmed.

**Output:** `attention_review_{date}.csv`, `spatial_attention_overlay.png`

### Pathway 3 — Stress attribution review

**Tools:** SHAP on stress head + ground-truth c1,c2,c3 decomposition (Phase 12 L5).

**Procedure:**

1. For high |OSI − OSI_hat| days, compute SHAP on OSI_hat.
2. Decompose actual OSI at t+1 into c1 (shedding), c2 (reserve), c3 (limitations).
3. Assign driver: `driver = argmax(minmax(c1), minmax(c2), minmax(c3))`.
4. Compare driver to top SHAP group — build confusion matrix:

```
results/explainability/stress/stress_driver_confusion.csv  (Phase 12)
→ extended in Phase 14 with error-conditioned rows only
```

5. If demand error and stress error co-occur, label **compound operational failure**.

**Output:** `stress_attribution_review_{date}.csv`

## Root-cause label taxonomy

| Label ID | Name | Criteria |
| --- | --- | --- |
| RC-T1 | Temporal miss | Top SHAP G1–G2; low α on recent lags |
| RC-S1 | Spatial/graph miss | High ADS; A2 ablation worse on region |
| RC-C1 | Calendar/season miss | Holiday or month-9; G5–G6 dominant |
| RC-G1 | Supply/reserve miss | c2 dominant; G7–G8 SHAP |
| RC-L1 | Shedding miss | c1 dominant; shedding day; G3/G11 |
| RC-X1 | Exogenous shock | Limitation/temperature spike; G9–G11 |
| RC-M1 | Multi-task interference | Demand ok, stress bad (or vice versa) on same day |
| RC-U1 | Uncertain | No pathway agreement (< 2/3 concur) |

## Triangulation decision rule

Assign final root cause when **≥ 2 of 3 pathways agree** on the same label family:

```
families: {Temporal}, {Spatial}, {Calendar}, {Supply}, {Shedding}, {Exogenous}
```

If only 1 pathway fires → label **RC-U1 Uncertain** and flag for manual review.

## Integration with ablation (Phase 13)

| Ablation | Root-cause use |
| --- | --- |
| A2 (−Graph) | Validate RC-S1 labels — graph removal should worsen same regions |
| A3 (−Transformer) | Validate RC-T1 — temporal removal worsens same days |
| A4 (demand-only) | Validate RC-M1 — stress errors without stress head |
| A5-GEO | Validate hybrid-edge RC-S1 cases (Cumilla–Khulna etc.) |

## Workflow summary

```
1. Compute residuals (test) → flag triggers
2. For each flagged day:
     a. Feature attribution review  (Pathway 1)
     b. Attention review            (Pathway 2)
     c. Stress attribution review   (Pathway 3)
3. Triangulate → assign RC label
4. Aggregate RC labels → error taxonomy heatmap
5. Feed findings back to paper Discussion + operator brief
```

## Output artefacts

```
results/error_analysis/root_cause/rc_label_registry.csv
results/error_analysis/root_cause/flagged_days.csv
results/error_analysis/root_cause/rc_triangulation_log.csv
results/error_analysis/root_cause/rc_summary_by_category.csv
results/error_analysis/root_cause/root_cause_case_studies.md
```

## Acceptance criteria

- All three pathways documented and executable post-training.
- Triangulation rule frozen (≥2/3 agreement).
- RC labels mapped to E1–E6 error categories for cross-tabulation.
