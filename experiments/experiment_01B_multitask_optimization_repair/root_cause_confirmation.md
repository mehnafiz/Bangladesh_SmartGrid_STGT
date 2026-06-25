# Root Cause Confirmation — Experiment 01B

## Hypothesis (from 01A)

Architecture is valid; optimization imbalance caused OSI collapse.

## Confirmation

**Confirmed.** Repair interventions (demand normalization + balanced early stopping + higher λ₂) restore OSI variance and positive stress R² without architecture/graph/feature/target changes.

## Evidence

| Metric | Exp01 | Best repair (W20) |
| --- | --- | --- |
| Val stress R² | -20.5387 | 0.6373 |
| Val OSI pred std | 0.0000 | 0.0674 |
| Stress ‖∇‖ | ~0 | 13.531698 |
| Val demand R² | 0.8780 | 0.8630 |

## Conclusion

The 01A root cause stands: **loss-scale imbalance + demand-only early stopping** suppressed OSI learning. Repair requires **joint loss rebalancing and balanced model selection**, not architectural changes.
