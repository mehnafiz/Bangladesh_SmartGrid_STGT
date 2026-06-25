# Graph Construction Report — Phase 08

Generated: 2026-06-24

## Selected strategy

**Hybrid Graph**

### Construction rule

1. Compute train-only Pearson correlation ρ_ij on `{Region}_demand` (n=1,295 train rows).
2. Geographic neighbor set from Bangladesh admin division borders (see `GEOGRAPHIC_NEIGHBORS`).
3. Edge (i,j) exists if **geo_ij=1** OR **ρ_ij ≥ 0.85**.
4. Edge weight w_ij = ρ_ij (zero on diagonal); row-normalise for message-passing stability.

### Rationale

- Geographic edges provide interpretable inductive bias (Phase 05A/06).
- Correlation weights reflect observed national growth/seasonality coupling (Phase 02).
- Strong-correlation augmentation captures high-coupling non-border pairs (e.g., Barishal–Cumilla ρ≈0.93) without full dense correlation graph.

## Train demand correlation summary

- Pairwise ρ: min=0.622, mean=0.779, max=0.934
- Pairs with ρ≥0.65: 33/36 (Phase 02 threshold nearly saturates).

## Selected graph statistics

| strategy     |   nodes |   undirected_edges |   density |   mean_edge_weight |   min_edge_weight |   max_edge_weight |   mean_demand_corr_on_edges |   mean_demand_corr_off_edges |   mean_corr_geographic_edges | is_connected   |   self_loops |
|:-------------|--------:|-------------------:|----------:|-------------------:|------------------:|------------------:|----------------------------:|-----------------------------:|-----------------------------:|:---------------|-------------:|
| Hybrid Graph |       9 |                 24 |    0.6667 |             0.1875 |            0.1046 |            0.2809 |                      0.7901 |                       0.7573 |                       0.7759 | True           |            0 |

## Edge catalogue (selected hybrid)

| node_i     | node_j     |   demand_corr_train | geographic_neighbor   | hybrid_edge   |   hybrid_weight |
|:-----------|:-----------|--------------------:|:----------------------|:--------------|----------------:|
| Barishal   | Cumilla    |              0.9344 | True                  | True          |          0.2794 |
| Barishal   | Khulna     |              0.9203 | True                  | True          |          0.2751 |
| Chattogram | Dhaka      |              0.8624 | True                  | True          |          0.2256 |
| Barishal   | Chattogram |              0.7477 | True                  | True          |          0.2235 |
| Barishal   | Dhaka      |              0.7425 | True                  | True          |          0.222  |
| Khulna     | Rajshahi   |              0.8985 | True                  | True          |          0.2127 |
| Chattogram | Cumilla    |              0.7692 | True                  | True          |          0.2012 |
| Chattogram | Sylhet     |              0.7397 | True                  | True          |          0.1935 |
| Chattogram | Mymensingh |              0.7035 | True                  | True          |          0.184  |
| Mymensingh | Rajshahi   |              0.8569 | True                  | True          |          0.1818 |
| Mymensingh | Sylhet     |              0.8093 | True                  | True          |          0.1717 |
| Khulna     | Rangpur    |              0.7229 | True                  | True          |          0.1711 |
| Mymensingh | Rangpur    |              0.7699 | True                  | True          |          0.1633 |
| Rajshahi   | Rangpur    |              0.6346 | True                  | True          |          0.159  |
| Cumilla    | Khulna     |              0.9189 | False                 | True          |          0.154  |
| Cumilla    | Sylhet     |              0.8893 | False                 | True          |          0.1491 |
| Cumilla    | Rajshahi   |              0.86   | False                 | True          |          0.1442 |
| Cumilla    | Mymensingh |              0.8403 | True                  | True          |          0.1408 |
| Dhaka      | Khulna     |              0.7643 | True                  | True          |          0.1285 |
| Cumilla    | Dhaka      |              0.7537 | True                  | True          |          0.1263 |
| Dhaka      | Rajshahi   |              0.7407 | True                  | True          |          0.1245 |
| Dhaka      | Mymensingh |              0.7339 | True                  | True          |          0.1234 |
| Dhaka      | Sylhet     |              0.728  | True                  | True          |          0.1224 |
| Dhaka      | Rangpur    |              0.6219 | True                  | True          |          0.1046 |

## Scope

- Graph construction only; STGT architecture not designed.
- Locked phase datasets not modified.
