"""Explainability configuration (Phase 12 frozen defaults)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from constants import PROJECT_ROOT


@dataclass(frozen=True)
class ExplainabilityConfig:
    """Frozen XAI defaults for PF-STGT post-training analysis."""

    background_samples: int = 100
    gradient_shap_steps: int = 50
    permutation_repeats: int = 5
    top_k_temporal: int = 3
    top_k_nodes: int = 9
    shap_stability_bootstraps: int = 10
    shap_stability_threshold: float = 0.7
    attention_adjacency_threshold: float = 0.3
    shap_permutation_threshold: float = 0.5
    case_study_count: int = 20
    device: str = "cpu"
    output_root: Path = field(
        default_factory=lambda: PROJECT_ROOT / "results" / "explainability"
    )

    def shap_dir(self) -> Path:
        return self.output_root / "shap"

    def attention_dir(self) -> Path:
        return self.output_root / "attention"

    def nodes_dir(self) -> Path:
        return self.output_root / "nodes"

    def stress_dir(self) -> Path:
        return self.output_root / "stress"

    def permutation_dir(self) -> Path:
        return self.output_root / "permutation"
