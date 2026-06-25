"""Temporal lookback attribution (Phase 12 L3)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from explainability.attention_extractor import AttentionExtractor
from explainability.config import ExplainabilityConfig
from explainability.types import TemporalAttentionResult, TemporalAttributionResult
from utils.logging import get_logger

logger = get_logger(__name__)


class TemporalAttributor:
    """Derive time-step contributions and top-k influential lags from attention."""

    def __init__(
        self,
        config: ExplainabilityConfig | None = None,
        attention_extractor: AttentionExtractor | None = None,
    ) -> None:
        self.config = config or ExplainabilityConfig()
        self.attention_extractor = attention_extractor or AttentionExtractor()

    def from_attention(self, temporal: TemporalAttentionResult) -> TemporalAttributionResult:
        alpha_t = temporal.alpha_t
        top_k = min(self.config.top_k_temporal, len(alpha_t))
        indices = np.argsort(alpha_t)[::-1][:top_k]
        weights = tuple(float(alpha_t[i]) for i in indices)
        logger.debug(
            "Temporal top-%s lags: %s weights=%s",
            top_k,
            tuple(int(i) for i in indices),
            weights,
        )
        return TemporalAttributionResult(
            alpha_t=alpha_t,
            top_k_indices=tuple(int(i) for i in indices),
            top_k_weights=weights,
        )

    def extract_from_tensor(self, attn_temporal) -> TemporalAttributionResult:
        temporal = self.attention_extractor.extract_temporal(attn_temporal)
        return self.from_attention(temporal)

    def lag_labels(self, indices: tuple[int, ...], window_size: int) -> tuple[str, ...]:
        """Convert timestep indices to lag-day labels (0 = most recent)."""
        labels: list[str] = []
        for idx in indices:
            lag = window_size - 1 - idx
            labels.append(f"t-{lag}")
        return tuple(labels)

    def save_csv(
        self,
        result: TemporalAttributionResult,
        path: Path,
        *,
        date_label: str = "",
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["timestep,alpha_t,date"]
        for step, weight in enumerate(result.alpha_t):
            lines.append(f"{step},{weight:.8f},{date_label}")
        path.write_text("\n".join(lines))
        logger.info("Saved temporal attribution CSV -> %s", path)
        return path

    def save_bar_plot(
        self,
        result: TemporalAttributionResult,
        path: Path,
        *,
        window_size: int | None = None,
    ) -> Path | None:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.warning("matplotlib unavailable; skipping temporal bar plot")
            return None

        path.parent.mkdir(parents=True, exist_ok=True)
        x_labels = list(range(len(result.alpha_t)))
        if window_size is not None:
            x_labels = [f"t-{window_size - 1 - i}" for i in x_labels]

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.bar(x_labels, result.alpha_t)
        ax.set_title("Temporal attention attribution α_t")
        ax.set_ylabel("weight")
        fig.tight_layout()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        logger.info("Saved temporal bar plot -> %s", path)
        return path
