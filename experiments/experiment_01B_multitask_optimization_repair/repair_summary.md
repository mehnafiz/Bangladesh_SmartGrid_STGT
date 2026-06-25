# Repair Summary — Experiment 01B

Generated: 2026-06-25

## Objective

Repair OSI learning collapse from Experiment 01A via optimization changes only.

## Interventions tested

1. **Loss weight study:** λ₂ ∈ {5, 10, 20}
2. **Demand loss normalization:** Huber demand ÷ 100 MW
3. **Balanced early stopping:** 0.7·(demand_MAE/100) + 0.3·stress_MAE

## Configurations run

- Primary repair runs: W5, W10, W20 (normalized + balanced ES)
- Controls: W10_raw_demand, W20_raw_demand (weight-only, no norm)

## Success criteria (01B)

- Configs meeting stress R² > 0 and OSI variance > 0: **2/3** primary runs
- Best config: **W20** (λ₂=20.0)

## Recommendation

Adopt **`W20`** for subsequent experiments: λ₂=20.0, normalized demand loss, balanced early stopping.

## Scope compliance

- Architecture, graph, features, targets unchanged
- No baselines or ablations
