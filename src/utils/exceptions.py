"""Custom exceptions for foundation pipelines."""

from __future__ import annotations


class FoundationError(Exception):
    """Base exception for Sprint 01 foundation layer."""


class LockedArtifactError(FoundationError):
    """Raised when a locked artefact fails MD5 verification."""


class DataValidationError(FoundationError):
    """Raised when P1 data validation fails."""


class FeatureValidationError(FoundationError):
    """Raised when P2 feature validation fails."""


class GraphValidationError(FoundationError):
    """Raised when P3 graph validation fails."""


class TargetValidationError(FoundationError):
    """Raised when P4 target validation fails."""
