# Graph Contribution Report — Experiment 03A

Generated: 2026-06-25

## Graph topology comparison

| variant   |   undirected_edges |   density_pct |   mean_weight |
|:----------|-------------------:|--------------:|--------------:|
| hybrid    |                 24 |       66.6667 |        0.1875 |
| geo       |                 21 |       58.3333 |        0.2143 |
| corr      |                 33 |       91.6667 |        0.1364 |

- **Geo-only edges not in correlation graph:** 2 pairs
- **Correlation-only edges not in geo graph:** 14 pairs
- Examples of geo-only links: Dhaka-Rangpur, Rajshahi-Rangpur

## Test demand MAE by graph variant

| Variant | Graph | MAE (MW) | Δ vs A1 |
| --- | --- | --- | --- |
| A1 | Hybrid | 93.31 | 0 |
| A5 | Geographical only | 97.98 | **+4.67** |
| A6 | Correlation only | 88.65 | **-4.66** |

Wilcoxon: A5 significantly **worse** than A1 (p_adj < 0.01); A6 significantly **better** (p < 0.001).

## Regional error pattern (ΔMAE vs A1, Dhaka)

| ablation_id   |    mae |   delta_vs_a1 |
|:--------------|-------:|--------------:|
| A4            | 285.12 |        -14.66 |
| A6            | 293.98 |         -5.79 |
| A1            | 299.78 |          0    |
| A3            | 317.18 |         17.4  |
| A2            | 336.85 |         37.08 |
| A5            | 339.14 |         39.37 |

## Interpretation

1. **Hybrid vs geo-only (A5):** Geographical edges alone hurt (+4.67 MW). Several border links
   connect regions with weak demand co-movement, acting as **noise** (especially Dhaka +39 MW vs A1).
2. **Hybrid vs corr-only (A6):** Correlation graph is **denser** (91.7% vs 66.7% density) and encodes
   strong demand co-variation; it outperforms hybrid on demand (−4.66 MW).
3. **Hybrid is not optimal for demand:** It improves over pure geography but **dilutes** the strongest
   correlation signal by retaining weaker geo edges.

Hybrid graph **is beneficial vs geography alone** but **is not beneficial vs correlation-only**
for demand under these training conditions.
