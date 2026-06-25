"""Operational stress attribution (Phase 12 L5)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from explainability.coalitions import COALITION_REGISTRY
from explainability.shap_engine import ShapEngine
from explainability.types import (
    GroupedShapValues,
    OSIComponentDecomposition,
    StressAttributionResult,
)
from targets.osi import OSIComponentBounds, OSITargetBuilder
from utils.logging import get_logger

logger = get_logger(__name__)

STRESS_PRIORITY_GROUPS: tuple[str, ...] = ("G7", "G8", "G3", "G11")
COMPONENT_LABELS = ("c1_shedding", "c2_reserve", "c3_limitation")


class StressAttributor:
    """
    Dual-pathway stress attribution: model SHAP + OSI component decomposition.

    Path A — grouped SHAP on the stress head (model-based).
    Path B — c1/c2/c3 ground-truth decomposition at t+1 (component-based).
    """

    def __init__(self, shap_engine: ShapEngine | None = None) -> None:
        self.shap_engine = shap_engine

    def decompose_components(
        self,
        clean_row: pd.DataFrame,
        bounds: OSIComponentBounds,
    ) -> OSIComponentDecomposition:
        """Compute raw and min-max normalised OSI components for one target row."""
        c1, c2, c3 = OSITargetBuilder._components(clean_row)
        raw_c1 = float(c1.iloc[0])
        raw_c2 = float(c2.iloc[0])
        raw_c3 = float(c3.iloc[0])
        n1 = OSITargetBuilder._minmax(raw_c1, *bounds.c1)
        n2 = OSITargetBuilder._minmax(raw_c2, *bounds.c2)
        n3 = OSITargetBuilder._minmax(raw_c3, *bounds.c3)
        driver = self.classify_driver(n1, n2, n3)
        return OSIComponentDecomposition(
            c1_raw=raw_c1,
            c2_raw=raw_c2,
            c3_raw=raw_c3,
            c1_norm=n1,
            c2_norm=n2,
            c3_norm=n3,
            driver=driver,
        )

    @staticmethod
    def classify_driver(c1_norm: float, c2_norm: float, c3_norm: float) -> str:
        values = (c1_norm, c2_norm, c3_norm)
        idx = int(np.argmax(values))
        return COMPONENT_LABELS[idx]

    def shap_driver_group(self, grouped: GroupedShapValues) -> str:
        ranking = sorted(
            zip(grouped.group_ids, grouped.phi, strict=True),
            key=lambda item: abs(item[1]),
            reverse=True,
        )
        return ranking[0][0]

    def driver_agreement(self, top_shap_group: str, component_driver: str) -> bool:
        """Heuristic mapping between SHAP coalitions and OSI component drivers."""
        mapping = {
            "c1_shedding": {"G11", "G3", "G1"},
            "c2_reserve": {"G7", "G10"},
            "c3_limitation": {"G8"},
        }
        expected = mapping.get(component_driver, set())
        return top_shap_group in expected

    def analyze(
        self,
        grouped_shap: GroupedShapValues,
        components: OSIComponentDecomposition,
    ) -> StressAttributionResult:
        top_group = self.shap_driver_group(grouped_shap)
        agreement = self.driver_agreement(top_group, components.driver)
        notes: list[str] = []
        if not agreement:
            notes.append(
                f"Top SHAP group {top_group} differs from component driver {components.driver}"
            )
        if top_group in STRESS_PRIORITY_GROUPS:
            notes.append(f"Top SHAP group {top_group} matches expected stress coalition")

        logger.info(
            "Stress attribution driver=%s top_shap=%s agreement=%s",
            components.driver,
            top_group,
            agreement,
        )
        return StressAttributionResult(
            grouped_shap=grouped_shap,
            components=components,
            top_shap_group=top_group,
            driver_agreement=agreement,
            notes=tuple(notes),
        )

    def save_component_csv(
        self,
        components: OSIComponentDecomposition,
        path: Path,
        *,
        date_label: str = "",
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "component,raw,normalized,driver,date",
            f"c1,{components.c1_raw:.8f},{components.c1_norm:.8f},{components.driver},{date_label}",
            f"c2,{components.c2_raw:.8f},{components.c2_norm:.8f},{components.driver},{date_label}",
            f"c3,{components.c3_raw:.8f},{components.c3_norm:.8f},{components.driver},{date_label}",
        ]
        path.write_text("\n".join(lines))
        logger.info("Saved OSI component CSV -> %s", path)
        return path

    def save_grouped_shap_csv(
        self,
        grouped: GroupedShapValues,
        path: Path,
        *,
        date_label: str = "",
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        name_map = {spec.group_id: spec.group_name for spec in COALITION_REGISTRY}
        lines = ["group_id,group_name,phi,date"]
        for gid, phi in zip(grouped.group_ids, grouped.phi, strict=True):
            lines.append(f"{gid},{name_map.get(gid, gid)},{phi:.8f},{date_label}")
        path.write_text("\n".join(lines))
        logger.info("Saved stress grouped SHAP CSV -> %s", path)
        return path

    def save_report(
        self,
        result: StressAttributionResult,
        path: Path,
        *,
        date_label: str = "",
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# Stress case study — {date_label}",
            "",
            f"- Component driver: `{result.components.driver}`",
            f"- Top SHAP group: `{result.top_shap_group}`",
            f"- Agreement: `{result.driver_agreement}`",
            "",
            "## Notes",
        ]
        lines.extend(f"- {note}" for note in result.notes)
        path.write_text("\n".join(lines))
        logger.info("Saved stress case study markdown -> %s", path)
        return path
