"""Structured logging helpers."""

from __future__ import annotations

import logging
import sys
from typing import Final

DEFAULT_FORMAT: Final[str] = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logging once for CLI and tests."""
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
    root.addHandler(handler)
    root.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Return a named module logger."""
    setup_logging()
    return logging.getLogger(name)
