"""Frozen feature name specifications (Phase 09 I/O contract)."""

from __future__ import annotations

from constants import HOLIDAY_CAT_COLUMNS, REGIONS

NODE_INPUT_FEATURE_TEMPLATES: tuple[str, ...] = (
    "{region}_demand",
    "{region}_supply",
    "{region}_load",
    "demand_lag_1_{region}",
    "demand_lag_7_{region}",
    "load_lag_1_{region}",
    "demand_rolling_mean_7_{region}",
    "regional_demand_share_{region}",
    "regional_load_intensity_{region}",
)

GLOBAL_INPUT_FEATURE_NAMES: tuple[str, ...] = (
    "day_of_year_sin",
    "day_of_year_cos",
    "trend_index",
    "gap_days_since_previous_observation",
    "total_regional_demand",
    "total_regional_load",
    "generation_reserve",
    "temperature_anomaly_month",
    "total_operational_limitation",
    "any_regional_shedding",
    "Gas/LF limitation",
    "Coal supply Limitation",
    "Low water level in Kaptai lake",
    "Plants under shut down/ maintenance",
    "Max. Demand at eve. peak (Generation end)",
    "Highest Generation (Generation end)",
    "Holiday_cat",
)

EXCLUDED_INPUT_FEATURES: frozenset[str] = frozenset({"operational_stress_index"})


def node_feature_columns(region: str) -> list[str]:
    """Return the nine input column names for one region."""
    return [template.format(region=region) for template in NODE_INPUT_FEATURE_TEMPLATES]


def global_feature_columns() -> list[str]:
    """
    Return parquet column names used to build the global feature vector.

    ``Holiday_cat`` is derived from one-hot columns at runtime.
    """
    columns: list[str] = []
    for name in GLOBAL_INPUT_FEATURE_NAMES:
        if name == "Holiday_cat":
            columns.extend(HOLIDAY_CAT_COLUMNS)
        else:
            columns.append(name)
    return columns
