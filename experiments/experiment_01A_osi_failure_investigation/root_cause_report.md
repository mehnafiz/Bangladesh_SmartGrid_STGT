# Root Cause Report — Experiment 01A

## Executive summary

PF-STGT OSI forecasting failed primarily due to **gradient starvation and variance collapse in the stress head**, not due to missing demand forecasting capability. The model successfully learned demand (val R² ≈ 0.88) but the stress head converged to a **near-constant OSI predictor**.

## Primary root cause

**Loss-scale imbalance + demand-only early stopping → stress head variance collapse**

Evidence:

1. **Variance collapse:** validation std(predicted)/std(actual) = 0.0000 (predictions are constant)
2. **Flat predictions:** constant OSI output = **0.0000** on all 263 validation samples
3. **Loss dominance:** L_demand/L_stress ≈ 1028:1 at λ₂=0.5
4. **Gradient starvation:** stress head ‖∇‖ = 0.000000 vs demand head 285.6312
5. **Early stopping:** monitors demand MAE only; stress MAE stuck at ~0.2966 for 15+ epochs before stop
6. **Negative R²:** val R² = -20.54 — worse than mean baseline

## Contributing factors (secondary)

- **Low OSI variance** (std ≈ 0.05–0.08): small target range makes MSE gradient small in absolute terms.
- **Weak demand–OSI linear coupling:** OSI depends on shedding, reserve, and limitation components, not aggregate demand alone.
- **Shared fusion bottleneck:** stress head must compete with demand head for representation; demand gradients dominate backprop through fusion.

## Ruled out (within scope)

- Architecture defect (same backbone forecasts demand well).
- Data leakage or split errors (locked MD5s verified; demand metrics healthy).
- Insufficient training epochs (early stopping triggered; stress metric flat before stop).

## Recommended next steps (Experiment 01B+, no architecture change)

1. Retrain with **normalized demand loss** or **λ₂ ∈ [5, 20]**.
2. Early-stop on **0.7 × demand_MAE + 0.3 × stress_MAE** (or similar).
3. Log per-epoch std(predicted OSI) as collapse monitor.
4. Optional: freeze demand head, fine-tune stress head for 20 epochs.

## Conclusion

The most likely root cause is **multi-task optimization imbalance**: Huber demand loss (scale ~50–100 MW) overwhelms MSE stress loss (scale ~0.01–0.1), and early stopping selects checkpoints that minimize demand error while the stress head collapses to a **constant OSI ≈ 0** (validation MAE ≈ OSI mean because targets are predominantly > 0).
