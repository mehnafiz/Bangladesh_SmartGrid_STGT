# Gradient Analysis — Experiment 01B

Head gradient L2 norms at best checkpoint (validation batch probe).

| Config | ‖∇‖ demand head | ‖∇‖ stress head | Grad ratio D/S | Loss ratio D/S |
| --- | --- | --- | --- | --- |
| W5 | 3.2121 | 0.000000 | 3212137714216.68 | 2.46 |
| W10 | 1.2889 | 13.772400 | 0.09 | 37.40 |
| W20 | 2.3904 | 13.531698 | 0.18 | 32.56 |
| W10_raw_demand | 138.1443 | 0.000000 | 138144310459573.03 | 10.54 |
| W20_raw_demand | 201.4946 | 27.623356 | 7.29 | 1085.52 |

## Interpretation

- Exp01 showed stress ‖∇‖ ≈ 0 with collapsed OSI output.
- Repair configs with normalized demand restore active stress-head gradients.
