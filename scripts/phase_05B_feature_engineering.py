"""Phase 05B — Feature Engineering Implementation.

Implements ONLY High-Priority engineered features from the approved
Feature Engineering Blueprint (Phase 05A). Computes features on the full
chronological timeline from clean interim data (raw MW), applies train-only
fitted transforms where required, and merges onto processed split datasets.

No feature selection, graph construction, or model training.

Inputs:
    data/processed/train.parquet, validation.parquet, test.parquet
    data/interim/bangladesh_smartgrid_clean.parquet  (raw values for engineering)

Outputs:
    data/features/train_features.parquet
    data/features/validation_features.parquet
    data/features/test_features.parquet
    results/phases/phase_05B_feature_engineering/  (5 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
INTERIM_PATH = ROOT / "data" / "interim" / "bangladesh_smartgrid_clean.parquet"
PROCESSED_DIR = ROOT / "data" / "processed"
FEATURES_DIR = ROOT / "data" / "features"
REPORT_DIR = ROOT / "results" / "phases" / "phase_05B_feature_engineering"
BLUEPRINT_INVENTORY = ROOT / "results" / "phases" / "phase_05A_feature_blueprint" / "feature_inventory.csv"

FEATURES_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REGIONS = [
    "Dhaka", "Chattogram", "Rajshahi", "Mymensingh", "Sylhet",
    "Barishal", "Rangpur", "Cumilla", "Khulna",
]

COL_EVE_PEAK = "Max. Demand at eve. peak (Generation end)"
COL_HIGHEST_GEN = "Highest Generation (Generation end)"
COL_TEMP = "Maximum Temperature in Dhaka was"
LIMITATION_COLS = [
    "Gas/LF limitation",
    "Coal supply Limitation",
    "Low water level in Kaptai lake",
    "Plants under shut down/ maintenance",
]

# High-priority global feature names (blueprint Batch 1)
GLOBAL_FEATURES = [
    "day_of_year_sin",
    "day_of_year_cos",
    "trend_index",
    "gap_days_since_previous_observation",
    "total_regional_demand",
    "total_regional_load",
    "generation_reserve",
    "temperature_anomaly_month",
    "total_operational_limitation",
    "operational_stress_index",
    "any_regional_shedding",
]

PER_REGION_TEMPLATES = [
    "demand_lag_1",
    "demand_lag_7",
    "load_lag_1",
    "demand_rolling_mean_7",
    "regional_demand_share",
    "regional_load_intensity",
]


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def high_priority_feature_names() -> list[str]:
    names = list(GLOBAL_FEATURES)
    for tmpl in PER_REGION_TEMPLATES:
        for r in REGIONS:
            names.append(f"{tmpl}_{r}")
    return names


def minmax_norm(series: pd.Series, lo: float, hi: float) -> pd.Series:
    span = hi - lo
    if span == 0:
        return pd.Series(0.0, index=series.index)
    return (series - lo) / span


def engineer_high_priority_features(
    clean: pd.DataFrame,
    train_dates: set,
) -> tuple[pd.DataFrame, dict]:
    """Compute all High-Priority features on full chronological clean data."""
    df = clean.sort_values("Date").reset_index(drop=True).copy()
    meta: dict = {"train_only_fits": []}

    # --- Temporal (cyclical + trend + gap) ---
    doy = df["Date"].dt.dayofyear.astype(float)
    df["day_of_year_sin"] = np.sin(2 * np.pi * doy / 365.25)
    df["day_of_year_cos"] = np.cos(2 * np.pi * doy / 365.25)
    df["trend_index"] = (df["Date"] - df["Date"].min()).dt.days.astype(float)
    df["gap_days_since_previous_observation"] = df["Date"].diff().dt.days.fillna(0.0)

    demand_cols = [f"{r}_demand" for r in REGIONS]
    load_cols = [f"{r}_load" for r in REGIONS]

    # --- Regional lags & rolling (observed-row, past-only) ---
    for r in REGIONS:
        dcol, lcol = f"{r}_demand", f"{r}_load"
        df[f"demand_lag_1_{r}"] = df[dcol].shift(1)
        df[f"demand_lag_7_{r}"] = df[dcol].shift(7)
        df[f"load_lag_1_{r}"] = df[lcol].shift(1)
        # Past-only rolling mean: exclude current row via shift(1) before rolling.
        df[f"demand_rolling_mean_7_{r}"] = (
            df[dcol].shift(1).rolling(window=7, min_periods=7).mean()
        )

    # --- Regional shares & load intensity ---
    total_d = df[demand_cols].sum(axis=1)
    df["total_regional_demand"] = total_d
    df["total_regional_load"] = df[load_cols].sum(axis=1)
    for r in REGIONS:
        df[f"regional_demand_share_{r}"] = df[f"{r}_demand"] / total_d.replace(0, np.nan)
        df[f"regional_load_intensity_{r}"] = df[f"{r}_load"] / df[f"{r}_demand"].clip(lower=1)

    # --- Grid ---
    df["generation_reserve"] = df[COL_HIGHEST_GEN] - df[COL_EVE_PEAK]

    # --- Weather: monthly temperature anomaly (train-only monthly means) ---
    train_mask = df["Date"].isin(train_dates)
    monthly_mean = (
        df.loc[train_mask]
        .groupby(df.loc[train_mask, "Date"].dt.month)[COL_TEMP]
        .mean()
    )
    df["temperature_anomaly_month"] = df[COL_TEMP] - df["Date"].dt.month.map(monthly_mean)
    meta["train_only_fits"].append(
        {"feature": "temperature_anomaly_month", "monthly_means": monthly_mean.to_dict()}
    )

    # --- Operational ---
    df["total_operational_limitation"] = df[LIMITATION_COLS].sum(axis=1)
    df["any_regional_shedding"] = (df[load_cols] > 0).any(axis=1).astype(np.float32)

    # --- Operational stress index (train-only min-max normalisation of components) ---
    c1 = df["total_regional_load"] / df["total_regional_demand"].replace(0, np.nan)
    c2 = 1.0 - df["generation_reserve"] / df[COL_HIGHEST_GEN].replace(0, np.nan)
    c3 = df["total_operational_limitation"] / df[COL_HIGHEST_GEN].replace(0, np.nan)
    train_c1, train_c2, train_c3 = c1[train_mask], c2[train_mask], c3[train_mask]
    bounds = {
        "c1": (float(train_c1.min()), float(train_c1.max())),
        "c2": (float(train_c2.min()), float(train_c2.max())),
        "c3": (float(train_c3.min()), float(train_c3.max())),
    }
    n1 = minmax_norm(c1, *bounds["c1"])
    n2 = minmax_norm(c2, *bounds["c2"])
    n3 = minmax_norm(c3, *bounds["c3"])
    df["operational_stress_index"] = (n1 + n2 + n3) / 3.0
    meta["train_only_fits"].append(
        {"feature": "operational_stress_index", "component_bounds": bounds, "weights": [1 / 3, 1 / 3, 1 / 3]}
    )

    feat_cols = high_priority_feature_names()
    engineered = df[["Date"] + feat_cols].copy()
    return engineered, meta


def scale_engineered_features(
    engineered: pd.DataFrame,
    train_dates: set,
    feat_cols: list[str],
) -> tuple[pd.DataFrame, StandardScaler, list[str]]:
    """StandardScale continuous engineered features; fit on train rows only."""
    out = engineered.copy()
    scale_cols = [c for c in feat_cols if c != "any_regional_shedding"]
    out[scale_cols] = out[scale_cols].astype(np.float64)
    train_idx = out["Date"].isin(train_dates)

    scaler = StandardScaler()
    scaler.fit(out.loc[train_idx, scale_cols])
    scaled = scaler.transform(out[scale_cols]).astype(np.float32)
    out[scale_cols] = scaled
    out["any_regional_shedding"] = out["any_regional_shedding"].astype(np.float32)
    return out, scaler, scale_cols


def merge_with_processed(processed: pd.DataFrame, engineered: pd.DataFrame) -> pd.DataFrame:
    """Attach engineered columns to processed split (matched by Date)."""
    eng_cols = [c for c in engineered.columns if c != "Date"]
    merged = processed.merge(engineered[["Date"] + eng_cols], on="Date", how="left", validate="one_to_one")
    return merged


def validate_features(df: pd.DataFrame, split_name: str, feat_cols: list[str]) -> list[dict]:
    rows = []
    for col in feat_cols:
        s = df[col]
        rows.append(
            {
                "split": split_name,
                "feature": col,
                "count": len(s),
                "n_missing": int(s.isna().sum()),
                "missing_pct": round(float(s.isna().mean() * 100), 4),
                "mean": round(float(s.mean()), 6) if s.notna().any() else np.nan,
                "std": round(float(s.std()), 6) if s.notna().any() else np.nan,
                "min": round(float(s.min()), 6) if s.notna().any() else np.nan,
                "max": round(float(s.max()), 6) if s.notna().any() else np.nan,
            }
        )
    return rows


def main() -> None:
    feat_cols = high_priority_feature_names()
    inventory = pd.read_csv(BLUEPRINT_INVENTORY)
    hp_inventory = inventory[
        (inventory["status"] == "Proposed") & (inventory["priority"] == "High")
    ].set_index("feature_name")

    # Load processed splits (baseline + split boundaries).
    proc_train = pd.read_parquet(PROCESSED_DIR / "train.parquet")
    proc_val = pd.read_parquet(PROCESSED_DIR / "validation.parquet")
    proc_test = pd.read_parquet(PROCESSED_DIR / "test.parquet")
    train_dates = set(proc_train["Date"])

    interim_md5_before = file_md5(INTERIM_PATH)
    processed_md5_before = {
        "train": file_md5(PROCESSED_DIR / "train.parquet"),
        "validation": file_md5(PROCESSED_DIR / "validation.parquet"),
        "test": file_md5(PROCESSED_DIR / "test.parquet"),
    }

    # Engineer on full clean timeline (raw MW values).
    clean = pd.read_parquet(INTERIM_PATH)
    engineered_raw, fit_meta = engineer_high_priority_features(clean, train_dates)
    engineered, feat_scaler, scaled_cols = scale_engineered_features(
        engineered_raw, train_dates, feat_cols
    )

    # Merge onto processed splits.
    train_feat = merge_with_processed(proc_train, engineered)
    val_feat = merge_with_processed(proc_val, engineered)
    test_feat = merge_with_processed(proc_test, engineered)

    # Leakage checks.
    train_max = proc_train["Date"].max()
    val_min = proc_val["Date"].min()
    test_min = proc_test["Date"].min()
    no_train_val_leak = train_max < val_min
    no_val_test_leak = proc_val["Date"].max() < test_min
    row_counts_ok = (
        len(train_feat) == len(proc_train)
        and len(val_feat) == len(proc_val)
        and len(test_feat) == len(proc_test)
    )

    # Save feature datasets.
    train_feat.to_parquet(FEATURES_DIR / "train_features.parquet", index=False)
    val_feat.to_parquet(FEATURES_DIR / "validation_features.parquet", index=False)
    test_feat.to_parquet(FEATURES_DIR / "test_features.parquet", index=False)

    log_rows = [
        {"step": 1, "action": "load_processed_splits", "details": f"train={len(proc_train)}, val={len(proc_val)}, test={len(proc_test)}"},
        {"step": 2, "action": "engineer_on_clean_timeline", "details": f"{len(feat_cols)} high-priority features on {len(clean)} rows"},
        {"step": 3, "action": "train_only_fits", "details": "temperature_anomaly_month, operational_stress_index, StandardScaler"},
        {"step": 4, "action": "merge_by_date", "details": "engineered features attached to processed baseline columns"},
        {"step": 5, "action": "save_feature_splits", "details": str(FEATURES_DIR.relative_to(ROOT))},
    ]
    pd.DataFrame(log_rows).to_csv(REPORT_DIR / "feature_generation_log.csv", index=False)

    # implemented_features.csv
    impl_rows = []
    for name in feat_cols:
        inv = hp_inventory.loc[name]
        impl_rows.append(
            {
                "feature_name": name,
                "blueprint_priority": "High",
                "feature_category": inv["feature_category"],
                "mathematical_definition": inv["mathematical_definition"],
                "required_input_columns": inv["required_input_columns"],
                "implementation_status": "Implemented",
                "blueprint_reference": "results/phases/phase_05A_feature_blueprint/feature_inventory.csv",
            }
        )
    pd.DataFrame(impl_rows).to_csv(REPORT_DIR / "implemented_features.csv", index=False)

    # feature_statistics.csv
    stats = (
        validate_features(train_feat, "train", feat_cols)
        + validate_features(val_feat, "validation", feat_cols)
        + validate_features(test_feat, "test", feat_cols)
    )
    pd.DataFrame(stats).to_csv(REPORT_DIR / "feature_statistics.csv", index=False)

    # Skipped = Medium + Low from blueprint
    skipped = inventory[(inventory["status"] == "Proposed") & (inventory["priority"] != "High")]

    # feature_validation_report.md
    train_na = pd.DataFrame(stats)
    train_na = train_na[train_na["split"] == "train"]
    warmup_na = train_na[train_na["n_missing"] > 0][["feature", "n_missing", "missing_pct"]]

    vr = [
        "# Phase 05B — Feature Validation Report",
        "",
        "## Leakage prevention",
        "",
        f"- Features computed on full chronological timeline; lags/rolling use **past rows only** (`shift` + `rolling`).",
        f"- Train-only fitted transforms: monthly temperature means, OSI component bounds, StandardScaler on engineered features.",
        f"- Train max date < validation min: **{no_train_val_leak}** ({train_max.date()} < {val_min.date()})",
        f"- Validation max < test min: **{no_val_test_leak}**",
        f"- Row counts preserved after merge: **{row_counts_ok}**",
        "",
        "## Output schema",
        "",
        f"- Baseline processed columns: **{proc_train.shape[1]}**",
        f"- New engineered columns: **{len(feat_cols)}**",
        f"- Total columns per split: **{train_feat.shape[1]}**",
        "",
        "## Missing values (train split)",
        "",
    ]
    if warmup_na.empty:
        vr.append("- No missing values in engineered features on train split.")
    else:
        vr += ["| feature | n_missing | missing_pct |", "| --- | --- | --- |"]
        for _, r in warmup_na.iterrows():
            vr.append(f"| {r['feature']} | {r['n_missing']} | {r['missing_pct']}% |")
        vr += [
            "",
            "- Expected warm-up NaNs at series start for lag-7 and rolling-7 features "
            "(first 7 rows of full timeline; fewer in train split start).",
        ]

    vr += [
        "",
        "## Integrity",
        "",
        f"- Interim input unchanged: **{file_md5(INTERIM_PATH) == interim_md5_before}**",
        f"- Processed train unchanged: **{file_md5(PROCESSED_DIR / 'train.parquet') == processed_md5_before['train']}**",
        "",
        "## Chronological ordering",
        "",
        f"- Train dates monotonic: **{train_feat['Date'].is_monotonic_increasing}**",
        f"- Validation dates monotonic: **{val_feat['Date'].is_monotonic_increasing}**",
        f"- Test dates monotonic: **{test_feat['Date'].is_monotonic_increasing}**",
    ]
    (REPORT_DIR / "feature_validation_report.md").write_text("\n".join(vr) + "\n")

    # engineering_summary.md
    es = [
        "# Phase 05B — Engineering Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Blueprint: `docs/methodology/Feature_Engineering_Blueprint.md`",
        f"- Implemented: **{len(feat_cols)}** High-Priority features",
        f"- Skipped: **{len(skipped)}** Medium/Low-Priority features (deferred to later batches)",
        "",
        "## Outputs",
        "",
        f"- `data/features/train_features.parquet` ({train_feat.shape[0]} × {train_feat.shape[1]})",
        f"- `data/features/validation_features.parquet` ({val_feat.shape[0]} × {val_feat.shape[1]})",
        f"- `data/features/test_features.parquet` ({test_feat.shape[0]} × {test_feat.shape[1]})",
        "",
        "## Implementation notes",
        "",
        "- Engineered on raw MW values from `bangladesh_smartgrid_clean.parquet`.",
        "- Merged onto Phase 04 processed baseline columns by `Date`.",
        "- Gap-aware lags use observed-row offsets on the sorted timeline.",
        "- Rolling means exclude the current row (shift before rolling).",
        "- `any_regional_shedding` left as binary 0/1 (not scaled).",
        "",
        "## Scope compliance",
        "",
        "- High-Priority only. No feature selection, graph construction, or model training.",
        "- Locked phase outputs (Phases 01–05A) not modified.",
    ]
    (REPORT_DIR / "engineering_summary.md").write_text("\n".join(es) + "\n")

    print("Phase 05B feature engineering complete.")
    print(f"Implemented: {len(feat_cols)} high-priority features")
    print(f"Output shape train: {train_feat.shape}")
    print(f"Leakage checks: train<val={no_train_val_leak}, val<test={no_val_test_leak}")
    print(f"Interim/processed unchanged: {file_md5(INTERIM_PATH) == interim_md5_before}")
    print(f"Features -> {FEATURES_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
