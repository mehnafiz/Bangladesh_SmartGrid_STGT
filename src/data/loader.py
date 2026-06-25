"""Load feature splits and aligned clean interim data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from constants import (
    FEATURES_DIR,
    INTERIM_PATH,
    PROJECT_ROOT,
    SPLIT_NAMES,
    SPLIT_SPECS,
)
from utils.logging import get_logger
from utils.md5 import verify_locked_artifacts

logger = get_logger(__name__)


@dataclass(frozen=True)
class SplitFrames:
    """Feature and clean frames for one chronological split."""

    name: str
    features: pd.DataFrame
    clean: pd.DataFrame


class DataStore:
    """Read-only access to processed feature splits and clean interim timeline."""

    def __init__(
        self,
        root: Path | None = None,
        *,
        verify_md5: bool = True,
    ) -> None:
        self.root = root or PROJECT_ROOT
        self.features_dir = self.root / FEATURES_DIR.relative_to(PROJECT_ROOT)
        self.interim_path = self.root / INTERIM_PATH.relative_to(PROJECT_ROOT)

        if verify_md5:
            logger.info("Verifying locked artefact MD5 hashes")
            verify_locked_artifacts(self.root, strict=True)

        self._clean = self._load_clean()
        self._splits: dict[str, SplitFrames] = {}
        for split_name in SPLIT_NAMES:
            self._splits[split_name] = self._load_split(split_name)

    @property
    def clean(self) -> pd.DataFrame:
        return self._clean

    def get_split(self, name: str) -> SplitFrames:
        if name not in self._splits:
            raise KeyError(f"Unknown split: {name}. Expected one of {SPLIT_NAMES}")
        return self._splits[name]

    def all_splits(self) -> dict[str, SplitFrames]:
        return dict(self._splits)

    def _load_clean(self) -> pd.DataFrame:
        if not self.interim_path.exists():
            raise FileNotFoundError(f"Clean interim data not found: {self.interim_path}")
        df = pd.read_parquet(self.interim_path)
        df = df.sort_values("Date").reset_index(drop=True)
        df["Date"] = pd.to_datetime(df["Date"])
        logger.info("Loaded clean interim timeline: %s rows", len(df))
        return df

    def _load_split(self, name: str) -> SplitFrames:
        spec = SPLIT_SPECS[name]
        feature_path = self.features_dir / f"{name}_features.parquet"
        if not feature_path.exists():
            raise FileNotFoundError(f"Feature split not found: {feature_path}")

        features = pd.read_parquet(feature_path)
        features = features.sort_values("Date").reset_index(drop=True)
        features["Date"] = pd.to_datetime(features["Date"])

        clean = self._clean[self._clean["Date"].isin(features["Date"])].copy()
        clean = clean.sort_values("Date").reset_index(drop=True)

        if len(features) != spec.expected_rows:
            logger.warning(
                "Split %s row count %s != expected %s",
                name,
                len(features),
                spec.expected_rows,
            )
        if len(clean) != len(features):
            raise ValueError(
                f"Clean/feature row mismatch for split {name}: "
                f"{len(clean)} vs {len(features)}"
            )

        logger.info(
            "Loaded split %s: %s feature rows (%s → %s)",
            name,
            len(features),
            spec.start_date,
            spec.end_date,
        )
        return SplitFrames(name=name, features=features, clean=clean)
