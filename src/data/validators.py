"""Data validation for P1 pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from constants import REGIONS, SPLIT_SPECS
from features.specs import global_feature_columns, node_feature_columns
from utils.exceptions import DataValidationError
from utils.logging import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = {"Date"}


@dataclass
class ValidationIssue:
    severity: str
    check: str
    message: str


@dataclass
class ValidationReport:
    split: str
    passed: bool
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, severity: str, check: str, message: str) -> None:
        self.issues.append(ValidationIssue(severity, check, message))
        if severity == "ERROR":
            self.passed = False


class DataValidator:
    """Validate schema, timestamps, and split integrity."""

    def validate_split(
        self,
        split_name: str,
        features: pd.DataFrame,
        clean: pd.DataFrame,
    ) -> ValidationReport:
        report = ValidationReport(split=split_name, passed=True)
        spec = SPLIT_SPECS[split_name]

        self._check_row_count(report, features, spec.expected_rows)
        self._check_required_columns(report, features)
        self._check_node_columns(report, features)
        self._check_global_columns(report, features)
        self._check_dates(report, features, spec)
        self._check_monotonic_dates(report, features)
        self._check_clean_alignment(report, features, clean)

        if report.passed:
            logger.info("Validation passed for split %s", split_name)
        else:
            logger.error("Validation failed for split %s: %s issues", split_name, len(report.issues))
        return report

    def validate_or_raise(self, report: ValidationReport) -> None:
        if not report.passed:
            messages = [f"[{i.severity}] {i.check}: {i.message}" for i in report.issues]
            raise DataValidationError("\n".join(messages))

    def _check_row_count(
        self, report: ValidationReport, df: pd.DataFrame, expected: int
    ) -> None:
        if len(df) != expected:
            report.add(
                "ERROR",
                "row_count",
                f"Expected {expected} rows, got {len(df)}",
            )

    def _check_required_columns(self, report: ValidationReport, df: pd.DataFrame) -> None:
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            report.add("ERROR", "schema", f"Missing required columns: {sorted(missing)}")

    def _check_node_columns(self, report: ValidationReport, df: pd.DataFrame) -> None:
        for region in REGIONS:
            for col in node_feature_columns(region):
                if col not in df.columns:
                    report.add("ERROR", "node_features", f"Missing column: {col}")

    def _check_global_columns(self, report: ValidationReport, df: pd.DataFrame) -> None:
        for col in global_feature_columns():
            if col not in df.columns and col != "Holiday_cat":
                report.add("ERROR", "global_features", f"Missing column: {col}")
        for col in ("Holiday_cat_0", "Holiday_cat_1", "Holiday_cat_2", "Holiday_cat_3"):
            if col not in df.columns:
                report.add("ERROR", "global_features", f"Missing holiday one-hot: {col}")

    def _check_dates(
        self,
        report: ValidationReport,
        df: pd.DataFrame,
        spec,
    ) -> None:
        dates = pd.to_datetime(df["Date"])
        if dates.isna().any():
            report.add("ERROR", "timestamps", "Null dates present")
        if dates.min().date() > pd.Timestamp(spec.start_date).date():
            report.add(
                "WARNING",
                "timestamps",
                f"Start date {dates.min().date()} after spec {spec.start_date}",
            )
        if dates.max().date() < pd.Timestamp(spec.end_date).date():
            report.add(
                "WARNING",
                "timestamps",
                f"End date {dates.max().date()} before spec {spec.end_date}",
            )

    def _check_monotonic_dates(self, report: ValidationReport, df: pd.DataFrame) -> None:
        dates = pd.to_datetime(df["Date"])
        if not dates.is_monotonic_increasing:
            report.add("ERROR", "timestamps", "Dates are not strictly monotonic increasing")
        if dates.duplicated().any():
            report.add("ERROR", "timestamps", "Duplicate dates detected")

    def _check_clean_alignment(
        self,
        report: ValidationReport,
        features: pd.DataFrame,
        clean: pd.DataFrame,
    ) -> None:
        if len(features) != len(clean):
            report.add(
                "ERROR",
                "alignment",
                f"Feature/clean length mismatch: {len(features)} vs {len(clean)}",
            )
            return
        f_dates = pd.to_datetime(features["Date"]).reset_index(drop=True)
        c_dates = pd.to_datetime(clean["Date"]).reset_index(drop=True)
        if not f_dates.equals(c_dates):
            report.add("ERROR", "alignment", "Feature and clean Date columns differ")
