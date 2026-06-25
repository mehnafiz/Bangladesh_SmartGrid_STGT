"""Project-wide frozen constants for Sprint 01 foundation pipelines."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Node order must match graphs/adjacency_matrix.csv (alphabetical divisions).
REGIONS: tuple[str, ...] = (
    "Barishal",
    "Chattogram",
    "Cumilla",
    "Dhaka",
    "Khulna",
    "Mymensingh",
    "Rajshahi",
    "Rangpur",
    "Sylhet",
)

N_NODES: int = len(REGIONS)
INPUT_WINDOW_T: int = 7
FORECAST_HORIZON_H: int = 1
WARMUP_SKIP: int = 7

NODE_FEATURES_PER_REGION: int = 9
GLOBAL_FEATURES: int = 17

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"
INTERIM_PATH = DATA_DIR / "interim" / "bangladesh_smartgrid_clean.parquet"
GRAPHS_DIR = PROJECT_ROOT / "graphs"
DEFAULT_ADJACENCY_PATH = GRAPHS_DIR / "adjacency_matrix.csv"

LOCKED_MD5: dict[str, str] = {
    "data/features/train_features.parquet": "b8b3bda95d0fd6cc65f4910d85a98e16",
    "data/interim/bangladesh_smartgrid_clean.parquet": "4255024d735a91a4b53b2edee203d0ca",
    "graphs/adjacency_matrix.csv": "dacb7ac3a827d00a4b61ea9400e75686",
}

COL_EVE_PEAK = "Max. Demand at eve. peak (Generation end)"
COL_HIGHEST_GEN = "Highest Generation (Generation end)"
COL_TEMP = "Maximum Temperature in Dhaka was"
LIMITATION_COLS: tuple[str, ...] = (
    "Gas/LF limitation",
    "Coal supply Limitation",
    "Low water level in Kaptai lake",
    "Plants under shut down/ maintenance",
)

HOLIDAY_CAT_COLUMNS: tuple[str, ...] = (
    "Holiday_cat_0",
    "Holiday_cat_1",
    "Holiday_cat_2",
    "Holiday_cat_3",
)

GEOGRAPHIC_NEIGHBORS: dict[str, tuple[str, ...]] = {
    "Barishal": ("Dhaka", "Khulna", "Chattogram", "Cumilla"),
    "Chattogram": ("Barishal", "Dhaka", "Sylhet", "Cumilla"),
    "Cumilla": ("Dhaka", "Chattogram", "Mymensingh", "Barishal"),
    "Dhaka": ("Barishal", "Khulna", "Mymensingh", "Rajshahi", "Rangpur", "Chattogram", "Cumilla"),
    "Khulna": ("Barishal", "Dhaka", "Rajshahi", "Rangpur"),
    "Mymensingh": ("Dhaka", "Sylhet", "Chattogram", "Rajshahi", "Cumilla"),
    "Rajshahi": ("Dhaka", "Khulna", "Rangpur", "Mymensingh"),
    "Rangpur": ("Rajshahi", "Dhaka", "Mymensingh", "Khulna"),
    "Sylhet": ("Mymensingh", "Chattogram", "Dhaka"),
}

CORRELATION_THRESHOLD: float = 0.65
STRONG_CORRELATION_THRESHOLD: float = 0.85


@dataclass(frozen=True)
class SplitSpec:
    """Frozen chronological split metadata (Phase 04)."""

    name: str
    start_date: str
    end_date: str
    expected_rows: int


SPLIT_SPECS: dict[str, SplitSpec] = {
    "train": SplitSpec("train", "2019-11-21", "2023-06-15", 1295),
    "validation": SplitSpec("validation", "2023-06-16", "2024-03-19", 277),
    "test": SplitSpec("test", "2024-03-20", "2024-12-30", 278),
}

SPLIT_NAMES: tuple[str, ...] = ("train", "validation", "test")
