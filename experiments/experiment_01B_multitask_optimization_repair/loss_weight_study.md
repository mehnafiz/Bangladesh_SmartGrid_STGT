# Loss Weight Study — Experiment 01B

Compared λ₂ ∈ {5, 10, 20} with demand normalization (÷100 MW) and balanced early stopping.
Additional raw-demand controls show weight-only repair is insufficient.

| Config | λ₂ | Norm demand | Balanced ES | Val stress R² | Val OSI pred std | Val demand R² | Loss balance ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W5 | 5.0 | Yes | Yes | -20.5387 | 0.0000 | 0.8746 | 2.46 |
| W10 | 10.0 | Yes | Yes | 0.3893 | 0.0694 | 0.8603 | 37.40 |
| W20 | 20.0 | Yes | Yes | 0.6373 | 0.0674 | 0.8630 | 32.56 |
| W10_raw_demand | 10.0 | No | No | -115.4883 | 0.0000 | 0.8552 | 10.54 |
| W20_raw_demand | 20.0 | No | No | 0.3053 | 0.0422 | 0.8815 | 1085.52 |

## Experiment 01 baseline (λ₂=0.5, no repair)

- Val stress R²: -20.5387
- Val OSI pred std: 0.0000
- Val demand R²: 0.8780
