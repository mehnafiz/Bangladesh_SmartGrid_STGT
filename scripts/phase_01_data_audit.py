"""Phase 01 — Data Audit & Research Readiness (READ-ONLY).

This script performs a strictly read-only audit of the original dataset.
It NEVER modifies, cleans, imputes, encodes, normalizes, or engineers the data.
It only inspects the data and writes audit reports to:

    results/phase_01_data_audit/

Input (read-only):
    data/raw/bangladesh_smartgrid_raw.csv
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "bangladesh_smartgrid_raw.csv"
OUT_DIR = ROOT / "results" / "phase_01_data_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    md5_before = file_md5(RAW_PATH)
    file_size_bytes = RAW_PATH.stat().st_size

    # Read the dataset exactly as stored, no parsing/coercion applied.
    df = pd.read_csv(RAW_PATH)
    n_rows, n_cols = df.shape

    # ------------------------------------------------------------------
    # 1. dataset_summary.csv
    # ------------------------------------------------------------------
    memory_bytes = int(df.memory_usage(deep=True).sum())
    summary = pd.DataFrame(
        {
            "metric": [
                "source_file",
                "file_size_bytes",
                "file_md5",
                "n_rows",
                "n_columns",
                "n_numeric_columns",
                "n_non_numeric_columns",
                "total_cells",
                "total_missing_cells",
                "missing_cell_fraction",
                "n_duplicate_rows",
                "in_memory_bytes",
            ],
            "value": [
                str(RAW_PATH.relative_to(ROOT)),
                file_size_bytes,
                md5_before,
                n_rows,
                n_cols,
                int(df.select_dtypes(include=[np.number]).shape[1]),
                int(df.select_dtypes(exclude=[np.number]).shape[1]),
                int(n_rows * n_cols),
                int(df.isna().sum().sum()),
                round(float(df.isna().sum().sum()) / float(n_rows * n_cols), 6),
                int(df.duplicated().sum()),
                memory_bytes,
            ],
        }
    )
    summary.to_csv(OUT_DIR / "dataset_summary.csv", index=False)

    # ------------------------------------------------------------------
    # 2. feature_dictionary.csv
    # ------------------------------------------------------------------
    feat_rows = []
    for i, col in enumerate(df.columns):
        s = df[col]
        non_null = s.dropna()
        sample_vals = non_null.unique()[:3]
        sample_str = " | ".join(map(lambda x: str(x), sample_vals))
        feat_rows.append(
            {
                "column_index": i,
                "feature_name": col,
                "dtype": str(s.dtype),
                "n_unique": int(s.nunique(dropna=True)),
                "n_missing": int(s.isna().sum()),
                "example_values": sample_str,
            }
        )
    pd.DataFrame(feat_rows).to_csv(OUT_DIR / "feature_dictionary.csv", index=False)

    # ------------------------------------------------------------------
    # 3. data_types_report.csv
    # ------------------------------------------------------------------
    dtype_rows = []
    for col in df.columns:
        s = df[col]
        is_numeric = pd.api.types.is_numeric_dtype(s)
        # Heuristic flag: object column whose non-null values all parse as numbers.
        numeric_parseable = False
        if not is_numeric:
            parsed = pd.to_numeric(s, errors="coerce")
            non_null = s.notna().sum()
            numeric_parseable = bool(non_null > 0 and parsed.notna().sum() == non_null)
        dtype_rows.append(
            {
                "feature_name": col,
                "pandas_dtype": str(s.dtype),
                "inferred_kind": (
                    "numeric" if is_numeric else ("numeric_as_text" if numeric_parseable else "categorical/text")
                ),
                "is_numeric": is_numeric,
                "numeric_parseable_if_text": numeric_parseable,
            }
        )
    pd.DataFrame(dtype_rows).to_csv(OUT_DIR / "data_types_report.csv", index=False)

    # ------------------------------------------------------------------
    # 4. missing_value_report.csv
    # ------------------------------------------------------------------
    miss = df.isna().sum()
    miss_df = pd.DataFrame(
        {
            "feature_name": miss.index,
            "n_missing": miss.values.astype(int),
            "missing_pct": (miss.values / n_rows * 100).round(4),
            "n_present": (n_rows - miss.values).astype(int),
        }
    ).sort_values("n_missing", ascending=False)
    miss_df.to_csv(OUT_DIR / "missing_value_report.csv", index=False)

    # ------------------------------------------------------------------
    # 5. duplicate_report.csv
    # ------------------------------------------------------------------
    n_full_dups = int(df.duplicated().sum())
    dup_rows = [
        {"check": "full_row_duplicates", "count": n_full_dups},
        {"check": "unique_rows", "count": int(n_rows - n_full_dups)},
    ]
    # Duplicate check on the temporal key (Date) if present.
    if "Date" in df.columns:
        dup_rows.append(
            {"check": "duplicate_Date_values", "count": int(df["Date"].duplicated().sum())}
        )
        dup_rows.append(
            {"check": "unique_Date_values", "count": int(df["Date"].nunique(dropna=True))}
        )
    pd.DataFrame(dup_rows).to_csv(OUT_DIR / "duplicate_report.csv", index=False)

    # ------------------------------------------------------------------
    # 6. target_analysis.csv
    #    Candidate targets are detected, NOT engineered. Demand / supply /
    #    load and generation columns are the natural forecasting targets for
    #    a multi-task STGT framework.
    # ------------------------------------------------------------------
    target_keywords = ("demand", "supply", "load", "generation", "max. demand")
    target_rows = []
    for col in df.columns:
        low = col.lower()
        if any(k in low for k in target_keywords):
            s = pd.to_numeric(df[col], errors="coerce")
            target_rows.append(
                {
                    "candidate_target": col,
                    "dtype": str(df[col].dtype),
                    "n_missing": int(df[col].isna().sum()),
                    "n_unique": int(df[col].nunique(dropna=True)),
                    "min": float(s.min()) if s.notna().any() else np.nan,
                    "max": float(s.max()) if s.notna().any() else np.nan,
                    "mean": round(float(s.mean()), 4) if s.notna().any() else np.nan,
                    "std": round(float(s.std()), 4) if s.notna().any() else np.nan,
                    "n_zeros": int((s == 0).sum()),
                }
            )
    pd.DataFrame(target_rows).to_csv(OUT_DIR / "target_analysis.csv", index=False)

    # ------------------------------------------------------------------
    # 7. basic_statistics.csv (descriptive stats, all columns)
    # ------------------------------------------------------------------
    desc = df.describe(include="all").transpose()
    desc.index.name = "feature_name"
    desc.to_csv(OUT_DIR / "basic_statistics.csv")

    # ------------------------------------------------------------------
    # 8. temporal_structure_report.md
    # ------------------------------------------------------------------
    lines = ["# Phase 01 — Temporal Structure Report", ""]
    if "Date" in df.columns:
        parsed_dates = pd.to_datetime(df["Date"], errors="coerce")
        n_unparsed = int(parsed_dates.isna().sum() - df["Date"].isna().sum())
        valid = parsed_dates.dropna().sort_values()
        lines += [
            "## Date column",
            "",
            f"- Raw dtype: `{df['Date'].dtype}`",
            f"- Parseable as datetime: {int(parsed_dates.notna().sum())} / {n_rows}",
            f"- Unparseable date values: {n_unparsed}",
            f"- Missing date values: {int(df['Date'].isna().sum())}",
        ]
        if not valid.empty:
            span_days = (valid.iloc[-1] - valid.iloc[0]).days
            diffs = valid.diff().dropna().dt.days
            step_counts = diffs.value_counts().sort_index()
            gaps = step_counts[step_counts.index > 1] if not step_counts.empty else pd.Series(dtype=int)
            lines += [
                f"- Date range: {valid.iloc[0].date()} → {valid.iloc[-1].date()}",
                f"- Calendar span: {span_days} days",
                f"- Number of unique dates: {int(valid.nunique())}",
                f"- Expected daily records over span: {span_days + 1}",
                "",
                "## Sampling interval (days between consecutive dates)",
                "",
                "| step_days | count |",
                "| --- | --- |",
            ]
            for step, cnt in step_counts.items():
                lines.append(f"| {int(step)} | {int(cnt)} |")
            lines += [
                "",
                f"- Dominant interval: {int(step_counts.idxmax())} day(s)",
                f"- Number of gaps (>1 day step): {int(gaps.sum()) if not gaps.empty else 0}",
            ]
    else:
        lines.append("- No `Date` column detected.")

    # Year / Month coverage if present.
    for tcol in ("Year", "Month"):
        if tcol in df.columns:
            vc = df[tcol].value_counts(dropna=False).sort_index()
            lines += ["", f"## {tcol} coverage", "", f"| {tcol} | count |", "| --- | --- |"]
            for k, v in vc.items():
                lines.append(f"| {k} | {int(v)} |")

    if "Day of the week" in df.columns:
        vc = df["Day of the week"].value_counts(dropna=False)
        lines += ["", "## Day of the week coverage", "", "| day | count |", "| --- | --- |"]
        for k, v in vc.items():
            lines.append(f"| {k} | {int(v)} |")

    (OUT_DIR / "temporal_structure_report.md").write_text("\n".join(lines) + "\n")

    # ------------------------------------------------------------------
    # 9. data_audit_report.md (master narrative report)
    # ------------------------------------------------------------------
    md5_after = file_md5(RAW_PATH)
    region_cols = [c for c in df.columns if any(
        c.startswith(r) for r in (
            "Dhaka", "Chattogram", "Rajshahi", "Mymensingh", "Sylhet",
            "Barishal", "Rangpur", "Cumilla", "Khulna",
        )
    )]
    regions = sorted({c.split("_")[0] for c in region_cols if "_" in c})

    top_missing = miss_df[miss_df["n_missing"] > 0].head(15)

    report = [
        "# Phase 01 — Data Audit Report",
        "",
        "## 1. Provenance & Integrity",
        "",
        f"- Source file: `{RAW_PATH.relative_to(ROOT)}`",
        f"- File size: {file_size_bytes:,} bytes",
        f"- MD5 (before audit): `{md5_before}`",
        f"- MD5 (after audit): `{md5_after}`",
        f"- Integrity: **{'UNCHANGED — dataset not modified' if md5_before == md5_after else 'CHANGED — WARNING'}**",
        "",
        "## 2. Shape",
        "",
        f"- Rows: **{n_rows:,}**",
        f"- Columns: **{n_cols}**",
        f"- Numeric columns: {int(df.select_dtypes(include=[np.number]).shape[1])}",
        f"- Non-numeric columns: {int(df.select_dtypes(exclude=[np.number]).shape[1])}",
        "",
        "## 3. Missing Values",
        "",
        f"- Total missing cells: {int(df.isna().sum().sum()):,} "
        f"({round(float(df.isna().sum().sum()) / float(n_rows * n_cols) * 100, 4)}% of all cells)",
        f"- Columns with any missing values: {int((miss > 0).sum())}",
        "",
    ]
    if not top_missing.empty:
        report += ["Top columns by missing count:", "", "| feature | n_missing | missing_pct |", "| --- | --- | --- |"]
        for _, r in top_missing.iterrows():
            report.append(f"| {r['feature_name']} | {int(r['n_missing'])} | {r['missing_pct']}% |")
    else:
        report.append("- No missing values detected in any column.")

    report += [
        "",
        "## 4. Duplicates",
        "",
        f"- Full duplicate rows: {n_full_dups}",
    ]
    if "Date" in df.columns:
        report.append(f"- Duplicate `Date` values: {int(df['Date'].duplicated().sum())}")

    report += [
        "",
        "## 5. Spatial Structure (Regions)",
        "",
        f"- Regional divisions detected: {len(regions)}",
        f"- Regions: {', '.join(regions) if regions else 'none detected'}",
        "- Each region carries `_demand`, `_supply`, and `_load` columns "
        "(node-level signals suitable for a spatio-temporal graph).",
        "",
        "## 6. Candidate Targets",
        "",
        f"- {len(target_rows)} candidate target columns detected "
        "(demand / supply / load / generation).",
        "- See `target_analysis.csv` for per-target statistics.",
        "",
        "## 7. Generated Deliverables",
        "",
        "- `dataset_summary.csv`",
        "- `feature_dictionary.csv`",
        "- `data_types_report.csv`",
        "- `missing_value_report.csv`",
        "- `duplicate_report.csv`",
        "- `target_analysis.csv`",
        "- `basic_statistics.csv`",
        "- `temporal_structure_report.md`",
        "- `data_audit_report.md`",
        "",
        "## 8. Scope Compliance",
        "",
        "- Read-only audit. No rows/columns removed, no values modified, "
        "no encoding, normalization, imputation, feature engineering, "
        "graph building, or modelling performed.",
        "",
    ]
    (OUT_DIR / "data_audit_report.md").write_text("\n".join(report) + "\n")

    # Console summary.
    print("Phase 01 audit complete.")
    print(f"Rows x Cols: {n_rows} x {n_cols}")
    print(f"Total missing cells: {int(df.isna().sum().sum())}")
    print(f"Full duplicate rows: {n_full_dups}")
    print(f"Candidate targets: {len(target_rows)}")
    print(f"Regions detected: {len(regions)} -> {regions}")
    print(f"MD5 unchanged: {md5_before == md5_after}")
    print(f"Deliverables written to: {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
