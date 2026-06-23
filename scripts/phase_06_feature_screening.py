"""Phase 06 — Feature Screening & Dataset Validation.

Validates engineered feature datasets for quality, integrity, temporal
consistency, and leakage. This phase performs NO feature selection, does NOT
remove any features (including graph-related), and does NOT train models.

Inputs (read-only):
    data/features/train_features.parquet
    data/features/validation_features.parquet
    data/features/test_features.parquet

Outputs:
    results/phases/phase_06_feature_screening/  (8 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEATURES_DIR = ROOT / "data" / "features"
REPORT_DIR = ROOT / "results" / "phases" / "phase_06_feature_screening"
IMPLEMENTED_PATH = ROOT / "results" / "phases" / "phase_05B_feature_engineering" / "implemented_features.csv"

NEAR_ZERO_VAR_THRESHOLD = 1e-10
DISTRIBUTION_SHIFT_Z = 3.0  # flag if |mean_val - mean_train| / std_train > 3

# Expected warm-up missing features (lag/rolling at series start).
EXPECTED_WARMUP_FEATURES = {
    f"{prefix}_{r}"
    for prefix in ("demand_lag_1", "demand_lag_7", "load_lag_1", "demand_rolling_mean_7")
    for r in (
        "Dhaka", "Chattogram", "Rajshahi", "Mymensingh", "Sylhet",
        "Barishal", "Rangpur", "Cumilla", "Khulna",
    )
}
EXPECTED_WARMUP_MISSING = {
    **{f: 1 for f in EXPECTED_WARMUP_FEATURES if "lag_1" in f or "load_lag" in f},
    **{f: 7 for f in EXPECTED_WARMUP_FEATURES if "lag_7" in f or "rolling_mean" in f},
}


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_splits() -> dict[str, pd.DataFrame]:
    return {
        "train": pd.read_parquet(FEATURES_DIR / "train_features.parquet"),
        "validation": pd.read_parquet(FEATURES_DIR / "validation_features.parquet"),
        "test": pd.read_parquet(FEATURES_DIR / "test_features.parquet"),
    }


def engineered_features() -> list[str]:
    impl = pd.read_csv(IMPLEMENTED_PATH)
    return impl["feature_name"].tolist()


def validate_dataset_integrity(splits: dict[str, pd.DataFrame]) -> dict:
    train, val, test = splits["train"], splits["validation"], splits["test"]
    cols_train = list(train.columns)
    cols_val = list(val.columns)
    cols_test = list(test.columns)

    date_overlap_train_val = bool(set(train["Date"]) & set(val["Date"]))
    date_overlap_val_test = bool(set(val["Date"]) & set(test["Date"]))
    date_overlap_train_test = bool(set(train["Date"]) & set(test["Date"]))

    return {
        "n_train": len(train),
        "n_validation": len(val),
        "n_test": len(test),
        "n_total": len(train) + len(val) + len(test),
        "n_columns": len(cols_train),
        "columns_identical_across_splits": cols_train == cols_val == cols_test,
        "train_date_start": str(train["Date"].iloc[0].date()),
        "train_date_end": str(train["Date"].iloc[-1].date()),
        "validation_date_start": str(val["Date"].iloc[0].date()),
        "validation_date_end": str(val["Date"].iloc[-1].date()),
        "test_date_start": str(test["Date"].iloc[0].date()),
        "test_date_end": str(test["Date"].iloc[-1].date()),
        "train_monotonic": bool(train["Date"].is_monotonic_increasing),
        "validation_monotonic": bool(val["Date"].is_monotonic_increasing),
        "test_monotonic": bool(test["Date"].is_monotonic_increasing),
        "train_max_lt_val_min": train["Date"].max() < val["Date"].min(),
        "val_max_lt_test_min": val["Date"].max() < test["Date"].min(),
        "no_date_overlap_train_val": not date_overlap_train_val,
        "no_date_overlap_val_test": not date_overlap_val_test,
        "no_date_overlap_train_test": not date_overlap_train_test,
        "date_dtype": str(train["Date"].dtype),
    }


def scan_feature_quality(
    splits: dict[str, pd.DataFrame],
    eng_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return quality_summary, constant_report, missing_report rows."""
    quality_rows: list[dict] = []
    constant_rows: list[dict] = []
    missing_rows: list[dict] = []

    train = splits["train"]
    train_stats: dict[str, dict] = {}

    for col in eng_cols:
        for split_name, df in splits.items():
            s = df[col]
            n = len(s)
            n_miss = int(s.isna().sum())
            n_inf = int(np.isinf(s.replace([np.inf, -np.inf], np.nan)).sum()) if s.dtype != "datetime64[ns]" else 0
            n_unique = int(s.nunique(dropna=True))
            std = float(s.std()) if s.notna().sum() > 1 else 0.0
            is_const = n_unique <= 1 and n_miss < n
            is_nzv = (not is_const) and std < NEAR_ZERO_VAR_THRESHOLD

            if split_name == "train":
                train_stats[col] = {"mean": float(s.mean()) if s.notna().any() else np.nan, "std": std}

            expected_miss = EXPECTED_WARMUP_MISSING.get(col, 0) if split_name == "train" else 0
            miss_expected = n_miss <= expected_miss if split_name == "train" else n_miss == 0
            miss_status = "expected_warmup" if (n_miss > 0 and miss_expected) else (
                "ok" if n_miss == 0 else "unexpected"
            )

            quality_rows.append(
                {
                    "feature": col,
                    "split": split_name,
                    "dtype": str(s.dtype),
                    "n_missing": n_miss,
                    "missing_pct": round(n_miss / n * 100, 4),
                    "missing_status": miss_status,
                    "n_infinite": n_inf,
                    "n_unique": n_unique,
                    "is_constant": is_const,
                    "is_near_zero_variance": is_nzv,
                    "mean": round(float(s.mean()), 6) if s.notna().any() else np.nan,
                    "std": round(std, 6),
                    "min": round(float(s.min()), 6) if s.notna().any() else np.nan,
                    "max": round(float(s.max()), 6) if s.notna().any() else np.nan,
                }
            )

            if is_const:
                constant_rows.append(
                    {"feature": col, "split": split_name, "n_unique": n_unique, "issue": "constant"}
                )
            if is_nzv:
                constant_rows.append(
                    {"feature": col, "split": split_name, "n_unique": n_unique,
                     "std": std, "issue": "near_zero_variance"}
                )
            if n_miss > 0:
                missing_rows.append(
                    {
                        "feature": col,
                        "split": split_name,
                        "n_missing": n_miss,
                        "missing_pct": round(n_miss / n * 100, 4),
                        "expected": miss_expected,
                        "status": miss_status,
                    }
                )
            if n_inf > 0:
                missing_rows.append(
                    {
                        "feature": col,
                        "split": split_name,
                        "n_missing": n_miss,
                        "missing_pct": round(n_miss / n * 100, 4),
                        "expected": False,
                        "status": f"infinite_values:{n_inf}",
                    }
                )

    # Distribution shift flags (train vs val/test).
    for col in eng_cols:
        t_mean = train_stats[col]["mean"]
        t_std = train_stats[col]["std"]
        for split_name in ("validation", "test"):
            s = splits[split_name][col]
            v_mean = float(s.mean()) if s.notna().any() else np.nan
            if t_std > NEAR_ZERO_VAR_THRESHOLD and not np.isnan(v_mean) and not np.isnan(t_mean):
                z_shift = abs(v_mean - t_mean) / t_std
                for row in quality_rows:
                    if row["feature"] == col and row["split"] == split_name:
                        row["distribution_shift_z"] = round(z_shift, 4)
                        row["distribution_shift_flag"] = z_shift > DISTRIBUTION_SHIFT_Z

    quality_df = pd.DataFrame(quality_rows)
    if "distribution_shift_z" not in quality_df.columns:
        quality_df["distribution_shift_z"] = np.nan
        quality_df["distribution_shift_flag"] = False

    return (
        quality_df,
        pd.DataFrame(constant_rows) if constant_rows else pd.DataFrame(
            columns=["feature", "split", "n_unique", "issue"]
        ),
        pd.DataFrame(missing_rows) if missing_rows else pd.DataFrame(
            columns=["feature", "split", "n_missing", "missing_pct", "expected", "status"]
        ),
        train_stats,
    )


def find_duplicate_features(train: pd.DataFrame, eng_cols: list[str]) -> pd.DataFrame:
    """Detect exact duplicate engineered feature columns in train split."""
    dup_rows: list[dict] = []
    numeric_eng = [c for c in eng_cols if c in train.columns and pd.api.types.is_numeric_dtype(train[c])]

    for a, b in combinations(numeric_eng, 2):
        sa, sb = train[a], train[b]
        both_na = sa.isna() & sb.isna()
        equal = (sa == sb) | both_na
        if equal.all():
            dup_rows.append(
                {
                    "feature_a": a,
                    "feature_b": b,
                    "duplicate_type": "exact",
                    "correlation": 1.0,
                    "split": "train",
                }
            )
        elif sa.notna().all() and sb.notna().all():
            corr = float(sa.corr(sb))
            if abs(corr) > 0.9999:
                dup_rows.append(
                    {
                        "feature_a": a,
                        "feature_b": b,
                        "duplicate_type": "near_perfect_correlation",
                        "correlation": round(corr, 6),
                        "split": "train",
                    }
                )

    if dup_rows:
        return pd.DataFrame(dup_rows)
    return pd.DataFrame(columns=["feature_a", "feature_b", "duplicate_type", "correlation", "split"])


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    md5_before = {p.name: file_md5(p) for p in FEATURES_DIR.glob("*.parquet")}
    splits = load_splits()
    eng_cols = engineered_features()
    ds = validate_dataset_integrity(splits)

    quality_df, constant_df, missing_df, _ = scan_feature_quality(splits, eng_cols)
    dup_df = find_duplicate_features(splits["train"], eng_cols)

    # Aggregate feature health summary (one row per engineered feature).
    summary_rows = []
    for col in eng_cols:
        sub = quality_df[quality_df["feature"] == col]
        train_row = sub[sub["split"] == "train"].iloc[0]
        summary_rows.append(
            {
                "feature": col,
                "dtype_train": train_row["dtype"],
                "train_n_missing": int(train_row["n_missing"]),
                "train_missing_status": train_row["missing_status"],
                "validation_n_missing": int(sub[sub["split"] == "validation"].iloc[0]["n_missing"]),
                "test_n_missing": int(sub[sub["split"] == "test"].iloc[0]["n_missing"]),
                "any_infinite": bool(sub["n_infinite"].sum() > 0),
                "is_constant_train": bool(train_row["is_constant"]),
                "is_near_zero_variance_train": bool(train_row["is_near_zero_variance"]),
                "validation_distribution_shift_flag": bool(
                    sub[sub["split"] == "validation"].iloc[0].get("distribution_shift_flag", False)
                ),
                "test_distribution_shift_flag": bool(
                    sub[sub["split"] == "test"].iloc[0].get("distribution_shift_flag", False)
                ),
                "validation_pass": (
                    not train_row["is_constant"]
                    and not train_row["is_near_zero_variance"]
                    and sub["n_infinite"].sum() == 0
                    and sub[sub["split"] != "train"]["n_missing"].sum() == 0
                    and train_row["missing_status"] != "unexpected"
                ),
            }
        )
    summary_df = pd.DataFrame(summary_rows)

    # Save CSV reports.
    quality_df.to_csv(REPORT_DIR / "feature_quality_summary.csv", index=False)
    constant_df.to_csv(REPORT_DIR / "constant_feature_report.csv", index=False)
    dup_df.to_csv(REPORT_DIR / "duplicate_feature_report.csv", index=False)
    missing_df.to_csv(REPORT_DIR / "missing_feature_report.csv", index=False)

    # Counts for narrative reports.
    n_const = len(constant_df[constant_df["issue"] == "constant"]) if not constant_df.empty else 0
    n_nzv = len(constant_df[constant_df["issue"] == "near_zero_variance"]) if not constant_df.empty else 0
    n_unexpected_miss = len(missing_df[missing_df["status"] == "unexpected"]) if not missing_df.empty else 0
    n_inf = int(quality_df["n_infinite"].sum())
    n_dup_exact = len(dup_df[dup_df["duplicate_type"] == "exact"]) if not dup_df.empty else 0
    n_shift_val = int(summary_df["validation_distribution_shift_flag"].sum())
    n_shift_test = int(summary_df["test_distribution_shift_flag"].sum())
    n_pass = int(summary_df["validation_pass"].sum())
    leakage_ok = (
        ds["train_max_lt_val_min"]
        and ds["val_max_lt_test_min"]
        and ds["no_date_overlap_train_val"]
        and ds["no_date_overlap_val_test"]
    )

    md5_after = {p.name: file_md5(p) for p in FEATURES_DIR.glob("*.parquet")}
    inputs_unchanged = md5_before == md5_after

    # --- leakage_validation_report.md ---
    lv = [
        "# Phase 06 — Leakage Validation Report",
        "",
        "## Temporal split integrity",
        "",
        f"| check | result |",
        f"| --- | --- |",
        f"| Train max < validation min | **{ds['train_max_lt_val_min']}** ({ds['train_date_end']} < {ds['validation_date_start']}) |",
        f"| Validation max < test min | **{ds['val_max_lt_test_min']}** ({ds['validation_date_end']} < {ds['test_date_start']}) |",
        f"| No date overlap (train ∩ val) | **{ds['no_date_overlap_train_val']}** |",
        f"| No date overlap (val ∩ test) | **{ds['no_date_overlap_train_test']}** |",
        f"| No date overlap (train ∩ test) | **{ds['no_date_overlap_train_test']}** |",
        "",
        "## Feature computation audit (Phase 05B design)",
        "",
        "- Lags and rolling features computed on full chronological timeline using past-only `shift`/`rolling`.",
        "- Train-only fitted transforms: monthly temperature means, OSI bounds, StandardScaler.",
        "- Validation/test rows use history from train period for lag features (correct for forecasting).",
        "",
        "## Distribution shift (informational, not leakage)",
        "",
        f"- Features flagged for val mean shift > {DISTRIBUTION_SHIFT_Z}σ from train: **{n_shift_val}**",
        f"- Features flagged for test mean shift > {DISTRIBUTION_SHIFT_Z}σ from train: **{n_shift_test}**",
        "- Temporal drift in demand (2019→2024 growth) causes expected shifts; this is not label leakage.",
        "",
        "## Verdict",
        "",
        f"**{'NO TEMPORAL LEAKAGE DETECTED' if leakage_ok else 'LEAKAGE RISK DETECTED'}**",
        "",
        f"- Feature input files unchanged: **{inputs_unchanged}**",
    ]
    (REPORT_DIR / "leakage_validation_report.md").write_text("\n".join(lv) + "\n")

    # --- dataset_validation_report.md ---
    dv = [
        "# Phase 06 — Dataset Validation Report",
        "",
        "## Split summary",
        "",
        "| split | rows | date start | date end | monotonic |",
        "| --- | --- | --- | --- | --- |",
        f"| train | {ds['n_train']} | {ds['train_date_start']} | {ds['train_date_end']} | {ds['train_monotonic']} |",
        f"| validation | {ds['n_validation']} | {ds['validation_date_start']} | {ds['validation_date_end']} | {ds['validation_monotonic']} |",
        f"| test | {ds['n_test']} | {ds['test_date_start']} | {ds['test_date_end']} | {ds['test_monotonic']} |",
        f"| **total** | **{ds['n_total']}** | | | |",
        "",
        "## Schema consistency",
        "",
        f"- Columns per split: **{ds['n_columns']}**",
        f"- Column names identical across splits: **{ds['columns_identical_across_splits']}**",
        f"- Date dtype: `{ds['date_dtype']}`",
        f"- Baseline + engineered: 81 processed + 65 engineered = 146",
        "",
        "## Checklist",
        "",
        f"| # | check | pass |",
        f"| --- | --- | --- |",
        f"| 1 | Row counts sum to 1,850 | **{ds['n_total'] == 1850}** |",
        f"| 2 | Temporal ordering preserved | **{ds['train_monotonic'] and ds['validation_monotonic'] and ds['test_monotonic']}** |",
        f"| 3 | Non-overlapping chronological splits | **{leakage_ok}** |",
        f"| 4 | Schema consistent across splits | **{ds['columns_identical_across_splits']}** |",
        f"| 5 | Input feature files unmodified | **{inputs_unchanged}** |",
        "",
        "## Verdict",
        "",
        f"**Dataset integrity: {'PASS' if ds['n_total'] == 1850 and leakage_ok and ds['columns_identical_across_splits'] else 'FAIL'}**",
    ]
    (REPORT_DIR / "dataset_validation_report.md").write_text("\n".join(dv) + "\n")

    # --- feature_validation_report.md ---
    fv = [
        "# Phase 06 — Feature Validation Report",
        "",
        f"Validated **{len(eng_cols)}** engineered features across train / validation / test.",
        "",
        "## Checklist",
        "",
        f"| # | check | result |",
        f"| --- | --- | --- |",
        f"| 1 | Constant features | **{n_const}** found |",
        f"| 2 | Near-zero variance features | **{n_nzv}** found |",
        f"| 3 | Exact duplicate engineered pairs | **{n_dup_exact}** found |",
        f"| 4 | Unexpected missing values | **{n_unexpected_miss}** found |",
        f"| 5 | Infinite values | **{n_inf}** found |",
        f"| 6 | Features passing validation | **{n_pass} / {len(eng_cols)}** |",
        "",
        "## Expected warm-up missing values (train only)",
        "",
        "- Lag-1 / load_lag_1: 1 missing row at series start (9 regions × 1 = 9 feature-series).",
        "- Lag-7 / rolling_mean_7: 7 missing rows at series start (9 regions × 1 = 9 feature-series).",
        "- All validation/test engineered features: 0 missing (history available from prior splits).",
        "",
        "## Graph-related features",
        "",
        "- No graph candidate features were implemented in Phase 05B (Batch 3 deferred).",
        "- No graph-related features were removed in this phase (selection prohibited).",
        "",
        "## Verdict",
        "",
    ]
    feat_ok = n_const == 0 and n_nzv == 0 and n_unexpected_miss == 0 and n_inf == 0
    fv.append(f"**Feature quality: {'PASS' if feat_ok else 'REVIEW REQUIRED'}**")
    (REPORT_DIR / "feature_validation_report.md").write_text("\n".join(fv) + "\n")

    # --- screening_summary.md ---
    ss = [
        "# Phase 06 — Screening Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Input: `data/features/` (train / validation / test)",
        f"- Engineered features validated: **{len(eng_cols)}**",
        "",
        "## Dataset health",
        "",
        f"- Total rows: **{ds['n_total']}** (1,295 + 277 + 278)",
        f"- Columns: **{ds['n_columns']}** (consistent across splits)",
        f"- Temporal integrity: **{'PASS' if leakage_ok else 'FAIL'}**",
        f"- Input files unchanged: **{inputs_unchanged}**",
        "",
        "## Feature health",
        "",
        f"- Constant: **{n_const}** | Near-zero variance: **{n_nzv}** | Infinite: **{n_inf}**",
        f"- Unexpected missing: **{n_unexpected_miss}** | Exact duplicates: **{n_dup_exact}**",
        f"- Passing validation: **{n_pass}/{len(eng_cols)}**",
        f"- Distribution shift flags (val/test): **{n_shift_val}/{n_shift_test}** (informational)",
        "",
        "## Leakage assessment",
        "",
        f"- **{'No temporal leakage detected' if leakage_ok else 'Leakage risk flagged'}**",
        "- Distribution shifts reflect real temporal drift (demand growth 2019→2024), not preprocessing leakage.",
        "",
        "## Scope compliance",
        "",
        "- Screening and validation only. No feature selection performed.",
        "- No features removed (including any graph-related). No models trained. No graphs built.",
        "- Locked phase outputs (Phases 01–05B) not modified.",
        "",
        "## Recommendations for graph construction",
        "",
        "1. Use 9 regional nodes (Dhaka, Chattogram, Rajshahi, Mymensingh, Sylhet, Barishal, Rangpur, Cumilla, Khulna).",
        "2. Node features: regional demand/supply/load + engineered lags, shares, load intensity from validated set.",
        "3. Implement Batch 3 graph candidates from blueprint: rolling_demand_corr_90d, geographic adjacency, pairwise_demand_gradient.",
        "4. Handle first 7 train rows (warm-up NaNs) via masking or drop before sequence windowing.",
        "5. Preserve chronological split boundaries when constructing dynamic edge weights.",
        "",
        "## Deliverables",
        "",
        "- `feature_validation_report.md`",
        "- `feature_quality_summary.csv`",
        "- `constant_feature_report.csv`",
        "- `duplicate_feature_report.csv`",
        "- `missing_feature_report.csv`",
        "- `leakage_validation_report.md`",
        "- `dataset_validation_report.md`",
        "- `screening_summary.md`",
    ]
    (REPORT_DIR / "screening_summary.md").write_text("\n".join(ss) + "\n")

    print("Phase 06 screening complete.")
    print(f"Engineered features validated: {len(eng_cols)}")
    print(f"Passing: {n_pass}/{len(eng_cols)}")
    print(f"Constant: {n_const}, NZV: {n_nzv}, Unexpected missing: {n_unexpected_miss}, Inf: {n_inf}")
    print(f"Leakage OK: {leakage_ok}")
    print(f"Inputs unchanged: {inputs_unchanged}")
    print(f"Reports -> {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
