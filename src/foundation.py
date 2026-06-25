"""Foundation layer coordinator — wires P1–P4 pipelines."""

from __future__ import annotations

from dataclasses import dataclass

from data.pipeline import DataPipeline
from data.splits import SampleIndex
from features.pipeline import FeaturePipeline
from features.temporal import XTemporal
from graph.pipeline import GraphPipeline
from graph.registry import GraphVariant
from graph.types import XGraph
from targets.batch import TargetBatch
from targets.pipeline import TargetPipeline
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class FoundationSample:
    """Complete Sprint 01 output for one windowed observation."""

    split: str
    sample: SampleIndex
    x_temporal: XTemporal
    x_graph: XGraph
    targets: TargetBatch


class FoundationCoordinator:
    """Orchestrate data, feature, graph, and target pipelines."""

    def __init__(
        self,
        *,
        verify_md5: bool = True,
        graph_variant: GraphVariant = GraphVariant.HYBRID,
    ) -> None:
        self.data_pipeline = DataPipeline(verify_md5=verify_md5)
        self.data_result = self.data_pipeline.run()
        train_clean = self.data_result.store.get_split("train").clean
        self.feature_pipeline = FeaturePipeline()
        self.graph_pipeline = GraphPipeline(
            variant=graph_variant,
            train_clean=train_clean,
        )
        self.graph_result = self.graph_pipeline.build()
        self.target_pipeline = TargetPipeline(train_clean)

    @property
    def x_graph(self) -> XGraph:
        return self.graph_result.x_graph

    def build_sample(self, split: str, end_idx: int) -> FoundationSample:
        split_frames = self.data_result.store.get_split(split)
        indices = self.data_result.sample_indices[split]
        sample = next((s for s in indices if s.end_idx == end_idx), None)
        if sample is None:
            raise ValueError(
                f"end_idx={end_idx} is not a valid sample index for split {split}"
            )

        feature_result = self.feature_pipeline.build_sample(
            split_frames.features, end_idx
        )
        target_result = self.target_pipeline.build(split_frames.clean, sample)

        return FoundationSample(
            split=split,
            sample=sample,
            x_temporal=feature_result.x_temporal,
            x_graph=self.graph_result.x_graph,
            targets=target_result.batch,
        )

    def smoke_sample(self, split: str = "train") -> FoundationSample:
        """Build the first valid sample for smoke testing."""
        indices = self.data_result.sample_indices[split]
        if not indices:
            raise RuntimeError(f"No valid sample indices for split {split}")
        return self.build_sample(split, indices[0].end_idx)
