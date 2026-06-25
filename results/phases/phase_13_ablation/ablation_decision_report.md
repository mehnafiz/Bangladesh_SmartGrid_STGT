# Ablation Decision Report — Phase 13

Generated: 2026-06-24

## Design rationale

### Component removals (A2–A3)

Parallel fusion PF-STGT (Phase 09) enables clean branch ablation without retuning depth.
A2/A3 directly test GAP-04 graph-temporal coupling claims.

### Hybrid graph (A5-GEO, A5-CORR)

Phase 08 selected hybrid over geo-only (23 vs 19) and correlation-only (23 vs 15).
Ablation quantifies whether selection holds on **test forecast metrics**, not graph statistics alone.

### Multi-task (A4)

Phase 08.5 frozen dual-task formulation; A4 isolates GAP-02 multi-task benefit on demand **and** enables stress-only evaluation on A1.

### Explainability (A6)

Phase 12 XAI is post-hoc on A1; A6 trains param-matched BiLSTM trunk without attention 
to measure performance–interpretability tradeoff (GAP-05).

## Variant registry

| ablation_id   | study_category    | variant_name                             | priority      |
|:--------------|:------------------|:-----------------------------------------|:--------------|
| A1            | reference         | PF-STGT Full Model                       | Required      |
| A2            | component_removal | Without Graph Module                     | Required      |
| A3            | component_removal | Without Transformer Module               | Required      |
| A4            | multi_task        | Without Multi-Task Learning              | Required      |
| A5            | hybrid_graph      | Hybrid Graph (same as A1)                | Required      |
| A5-GEO        | hybrid_graph      | Without Hybrid Graph — Geographical Only | Required      |
| A5-CORR       | hybrid_graph      | Correlation Graph Only                   | Supplementary |
| A6            | explainability    | Without Explainability Pathways          | Required      |
| A6-XAI        | explainability    | Full Model XAI Analysis (A1)             | Required      |

## Expected outcomes (hypotheses)

| ID | Expected if design is correct |
| --- | --- |
| A2 | Demand MAE increases (graph helps spatial coupling) |
| A3 | Demand MAE increases (transformer helps T=7 seasonality) |
| A4 | Demand MAE equal or worse; no stress output |
| A5-GEO | Demand MAE ≥ A1 (hybrid adds correlation weights) |
| A5-CORR | MAPE may degrade (dense graph over-smoothing) |
| A6 | MAE within 5% of A1; loses attention/SHAP fidelity |
