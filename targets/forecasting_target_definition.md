# Forecasting Target Definition — Phase 08.5

Generated: 2026-06-24
Status: **FROZEN**

## Primary forecast target

**Regional evening-peak demand (`{Region}_demand`, 9 nodes)**

Each graph node \(r \in \{\text{9 divisions}\}\) predicts next-day regional evening-peak demand \(D_r(t+1)\) in MW.

## Target variable specification

| Property | Value |
| --- | --- |
| Variable | `{Region}_demand` for each of 9 regions |
| Unit | MW |
| Granularity | Daily (one value per region per day) |
| Output tensor shape (conceptual) | `(9,)` demand vector |

## Excluded alternatives (evidence-based)

- **`{Region}_supply`:** Rejected — Phase 02 demand≈supply collinearity (ρ>0.9); redundant with demand target.
- **`{Region}_load` (shedding):** Not Task 1 target — sparse zero-inflated signal (Phase 02); embedded in Task 2 OSI component \(c_1=L_{total}/D_{total}\).
- **National aggregate only:** Rejected — graph has 9 regional nodes (Phase 08); node-level targets required.

## Forecast horizon

**Single-step (1-day-ahead) — horizon \(h = 1\) day**

- Persistence baseline at h=1: mean regional MAPE **5.55%**, mean regional MAE **69.6 MW**.
- Mean regional autocorrelation at lag 1: **0.924**.
- Aligns with Phase 05B lag-1 / rolling-7 feature design and daily BPDB reporting cadence (Phase 01).

## Multi-step extension (not frozen)

Horizons h=3,7,14 documented in `forecasting_horizon_analysis.csv` for future multi-step experiments; primary STGT formulation uses **h=1 only**.
