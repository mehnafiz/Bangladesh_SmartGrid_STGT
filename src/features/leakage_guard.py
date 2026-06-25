"""Leakage guard for model inputs (Phase 08.5)."""

from __future__ import annotations

from features.specs import EXCLUDED_INPUT_FEATURES, GLOBAL_INPUT_FEATURE_NAMES
from utils.exceptions import FeatureValidationError


class LeakageGuard:
    """Ensure forbidden targets are not used as model inputs."""

    forbidden: frozenset[str] = EXCLUDED_INPUT_FEATURES

    @classmethod
    def filter_columns(cls, columns: list[str]) -> list[str]:
        return [col for col in columns if col not in cls.forbidden]

    @classmethod
    def validate_global_names(cls) -> None:
        overlap = set(GLOBAL_INPUT_FEATURE_NAMES) & cls.forbidden
        if overlap:
            raise FeatureValidationError(
                f"Forbidden features present in global input spec: {sorted(overlap)}"
            )


def assert_no_osi_in_inputs(feature_names: list[str]) -> None:
    """Raise when operational stress index appears in input feature list."""
    if "operational_stress_index" in feature_names:
        raise FeatureValidationError(
            "operational_stress_index must not be used as model input at horizon h=1"
        )
