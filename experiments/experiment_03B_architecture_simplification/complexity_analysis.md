# Complexity Analysis — Experiment 03B

Generated: 2026-06-25

## Architecture variants

| ID | Model | Graph | Transformer | Fusion | Active modules |
| --- | --- | --- | --- | --- | --- |
| S1 | PF-STGT W20 | Hybrid | Yes | Yes | embedding, graph, temporal, fusion, heads |
| S2 | Correlation-only | Correlation (τ=0.65) | Yes | Yes | same as S1 |
| S3 | No-transformer | Hybrid | No | No | embedding, graph, heads |
| S4 | Corr + no-transformer | Correlation | No | No | embedding, graph, heads |

## Parameter counts

All variants share the same **stored** weight tensor layout (749,058 parameters).
S3/S4 skip temporal transformer and fusion in the **forward pass**; those weights remain allocated but inactive.

| variant_id   | model_name                        |   total_parameters |   active_parameters |   inactive_parameters |
|:-------------|:----------------------------------|-------------------:|--------------------:|----------------------:|
| S1           | PF-STGT (W20)                     |             749058 |              749058 |                     0 |
| S2           | Correlation-Only PF-STGT          |             749058 |              749058 |                     0 |
| S3           | No-Transformer PF-STGT            |             749058 |              451202 |                297856 |
| S4           | Correlation-Only + No-Transformer |             749058 |              451202 |                297856 |

## Module-level breakdown (PF-STGT base)

| module               |   parameters |
|:---------------------|-------------:|
| embedding            |         5632 |
| graph_transformer    |       264960 |
| temporal_transformer |       264960 |
| fusion               |        32896 |
| demand_head          |          129 |
| stress_head          |       180481 |

## Graph topology

| variant_id   | graph_variant   |   graph_undirected_edges |   density_pct |
|:-------------|:----------------|-------------------------:|--------------:|
| S1           | hybrid          |                       24 |          66.7 |
| S2           | corr            |                       33 |          91.7 |
| S3           | hybrid          |                       24 |          66.7 |
| S4           | corr            |                       33 |          91.7 |

## Training time (seconds)

| variant_id   | model_name                        |   training_seconds |
|:-------------|:----------------------------------|-------------------:|
| S1           | PF-STGT (W20)                     |              413.5 |
| S2           | Correlation-Only PF-STGT          |              393.1 |
| S3           | No-Transformer PF-STGT            |              367   |
| S4           | Correlation-Only + No-Transformer |              308.8 |

- S1: Experiment 01B W20 training (reference checkpoint, not retrained here)
- S2/S3: Experiment 03 ablation checkpoints
- S4: trained in Experiment 03B (W20 protocol)

## Inference latency (test loader, batch=32, mean of 20 batches)

| variant_id   |   inference_ms_per_batch32 |
|:-------------|---------------------------:|
| S1           |                       5.9  |
| S2           |                       5.78 |
| S3           |                       4.97 |
| S4           |                       5.08 |
