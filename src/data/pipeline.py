"""P1 data pipeline orchestrator."""

from __future__ import annotations

from dataclasses import dataclass

from data.loader import DataStore, SplitFrames
from data.splits import SampleIndex, SplitManager
from data.validators import DataValidator, ValidationReport
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class DataPipelineResult:
    store: DataStore
    validation_reports: dict[str, ValidationReport]
    sample_indices: dict[str, list[SampleIndex]]


class DataPipeline:
    """Load datasets, validate splits, and expose sample indices."""

    def __init__(
        self,
        store: DataStore | None = None,
        *,
        verify_md5: bool = True,
        validate: bool = True,
    ) -> None:
        self.store = store or DataStore(verify_md5=verify_md5)
        self.split_manager = SplitManager()
        self.validator = DataValidator()
        self.validate = validate

    def run(self) -> DataPipelineResult:
        reports: dict[str, ValidationReport] = {}
        sample_indices: dict[str, list[SampleIndex]] = {}

        feature_frames = {
            name: split.features for name, split in self.store.all_splits().items()
        }
        self.split_manager.validate_boundaries(feature_frames)

        for name, split in self.store.all_splits().items():
            if self.validate:
                report = self.validator.validate_split(name, split.features, split.clean)
                self.validator.validate_or_raise(report)
                reports[name] = report
            sample_indices[name] = self.split_manager.sample_indices(split.features)

        logger.info(
            "Data pipeline complete: train=%s val=%s test=%s samples",
            len(sample_indices["train"]),
            len(sample_indices["validation"]),
            len(sample_indices["test"]),
        )
        return DataPipelineResult(
            store=self.store,
            validation_reports=reports,
            sample_indices=sample_indices,
        )

    def get_split(self, name: str) -> SplitFrames:
        return self.store.get_split(name)
