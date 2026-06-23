"""Phase 04 — Data Preprocessing.

Prepare the cleaned dataset for machine learning with a leakage-safe,
chronological train/validation/test split and a preprocessing pipeline
fitted on training data only.

This phase performs NO feature engineering: no lags, rolling statistics,
derived features, graph construction, or model training.

Input:
    data/interim/bangladesh_smartgrid_clean.parquet

Outputs:
    data/processed/train.parquet
    data/processed/validation.parquet
    data/processed/test.parquet
    configs/preprocessing_config.yaml  (written if absent; read at runtime)
    models/preprocessing_pipeline.pkl
    results/phases/phase_04_preprocessing/  (5 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "preprocessing_config.yaml"
INTERIM_PATH = ROOT / "data" / "interim" / "bangladesh_smartgrid_clean.parquet"
PROCESSED_DIR = ROOT / "data" / "processed"
PIPELINE_PATH = ROOT / "models" / "preprocessing_pipeline.pkl"
REPORT_DIR = ROOT / "results" / "phases" / "phase_04_preprocessing"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def chronological_split(
    df: pd.DataFrame,
    sort_col: str,
    train_ratio: float,
    val_ratio: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Split sorted data chronologically into train / validation / test."""
    sorted_df = df.sort_values(sort_col).reset_index(drop=True)
    n = len(sorted_df)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    n_test = n - n_train - n_val

    train = sorted_df.iloc[:n_train].copy()
    val = sorted_df.iloc[n_train : n_train + n_val].copy()
    test = sorted_df.iloc[n_train + n_val :].copy()

    meta = {
        "n_total": n,
        "n_train": len(train),
        "n_validation": len(val),
        "n_test": len(test),
        "train_date_start": str(train[sort_col].iloc[0].date()),
        "train_date_end": str(train[sort_col].iloc[-1].date()),
        "validation_date_start": str(val[sort_col].iloc[0].date()),
        "validation_date_end": str(val[sort_col].iloc[-1].date()),
        "test_date_start": str(test[sort_col].iloc[0].date()),
        "test_date_end": str(test[sort_col].iloc[-1].date()),
    }
    return train, val, test, meta


def build_pipeline(cfg: dict) -> ColumnTransformer:
    numeric_cols = cfg["columns"]["numeric"]
    categorical_cols = cfg["columns"]["categorical"]

    enc_cfg = cfg["encoding"]
    encoder = OneHotEncoder(
        handle_unknown=enc_cfg["handle_unknown"],
        sparse_output=enc_cfg["sparse"],
    )

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", encoder, categorical_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def transform_split(
    pipeline: ColumnTransformer,
    split_df: pd.DataFrame,
    datetime_col: str,
    float_dtype: str,
) -> pd.DataFrame:
    """Apply fitted pipeline and reattach the datetime column."""
    features = pipeline.transform(split_df)
    feature_names = pipeline.get_feature_names_out()
    out = pd.DataFrame(features, columns=feature_names, index=split_df.index)
    out = out.astype(float_dtype)
    out.insert(0, datetime_col, split_df[datetime_col].values)
    return out


def main() -> None:
    cfg = load_config()
    interim_md5_before = file_md5(INTERIM_PATH)

    df = pd.read_parquet(INTERIM_PATH)
    n_in, cols_in = df.shape
    datetime_col = cfg["columns"]["datetime"][0]
    numeric_cols = cfg["columns"]["numeric"]
    categorical_cols = cfg["columns"]["categorical"]
    float_dtype = cfg["dtype_optimization"]["processed_float"]

    log_rows: list[dict] = []

    # ------------------------------------------------------------------
    # Step 1 — Chronological sort & split (before any fitting)
    # ------------------------------------------------------------------
    train_df, val_df, test_df, split_meta = chronological_split(
        df,
        sort_col=cfg["split"]["sort_column"],
        train_ratio=cfg["split"]["train_ratio"],
        val_ratio=cfg["split"]["validation_ratio"],
    )
    log_rows.append(
        {
            "step": 1,
            "action": "chronological_split",
            "details": (
                f"train={split_meta['n_train']}, "
                f"val={split_meta['n_validation']}, test={split_meta['n_test']}"
            ),
        }
    )

    # Leakage checks.
    train_max = train_df[datetime_col].max()
    val_min, val_max = val_df[datetime_col].min(), val_df[datetime_col].max()
    test_min = test_df[datetime_col].min()
    no_train_val_overlap = train_max < val_min
    no_val_test_overlap = val_max < test_min
    rows_sum = split_meta["n_train"] + split_meta["n_validation"] + split_meta["n_test"]
    rows_preserved = rows_sum == n_in

    # ------------------------------------------------------------------
    # Step 2 — Fit preprocessing pipeline on TRAIN ONLY
    # ------------------------------------------------------------------
    pipeline = build_pipeline(cfg)
    pipeline.fit(train_df)
    log_rows.append(
        {"step": 2, "action": "fit_pipeline", "details": "fitted on train split only"}
    )

    # ------------------------------------------------------------------
    # Step 3 — Transform each split (no refitting)
    # ------------------------------------------------------------------
    train_proc = transform_split(pipeline, train_df, datetime_col, float_dtype)
    val_proc = transform_split(pipeline, val_df, datetime_col, float_dtype)
    test_proc = transform_split(pipeline, test_df, datetime_col, float_dtype)
    log_rows.append(
        {"step": 3, "action": "transform_splits", "details": "train/validation/test transformed"}
    )

    # ------------------------------------------------------------------
    # Step 4 — Save processed datasets & pipeline
    # ------------------------------------------------------------------
    train_proc.to_parquet(PROCESSED_DIR / "train.parquet", index=False)
    val_proc.to_parquet(PROCESSED_DIR / "validation.parquet", index=False)
    test_proc.to_parquet(PROCESSED_DIR / "test.parquet", index=False)
    joblib.dump(pipeline, PIPELINE_PATH)
    log_rows.append({"step": 4, "action": "save_outputs", "details": "parquet splits + pipeline.pkl"})

    interim_md5_after = file_md5(INTERIM_PATH)
    feature_names = pipeline.get_feature_names_out()

    # ------------------------------------------------------------------
    # REPORT — encoding_report.csv
    # ------------------------------------------------------------------
    cat_encoder: OneHotEncoder = pipeline.named_transformers_["cat"]
    enc_rows = []
    for i, col in enumerate(categorical_cols):
        cats = cat_encoder.categories_[i]
        train_cats = train_df[col].unique()
        enc_rows.append(
            {
                "column": col,
                "n_categories_in_train": int(len(cats)),
                "categories_in_train": " | ".join(str(c) for c in cats),
                "n_unique_in_validation": int(val_df[col].nunique()),
                "n_unique_in_test": int(test_df[col].nunique()),
                "unseen_in_val": bool(set(val_df[col].unique()) - set(cats)),
                "unseen_in_test": bool(set(test_df[col].unique()) - set(cats)),
            }
        )
    pd.DataFrame(enc_rows).to_csv(REPORT_DIR / "encoding_report.csv", index=False)

    # ------------------------------------------------------------------
    # REPORT — scaling_report.csv
    # ------------------------------------------------------------------
    scaler: StandardScaler = pipeline.named_transformers_["num"]
    scale_rows = []
    for col, mean, scale in zip(
        numeric_cols, scaler.mean_, scaler.scale_, strict=True
    ):
        scale_rows.append(
            {
                "column": col,
                "train_mean": round(float(mean), 6),
                "train_std": round(float(scale), 6),
                "scaler": cfg["scaling"]["method"],
                "fit_on": cfg["scaling"]["fit_on"],
            }
        )
    pd.DataFrame(scale_rows).to_csv(REPORT_DIR / "scaling_report.csv", index=False)

    # ------------------------------------------------------------------
    # REPORT — split_report.md
    # ------------------------------------------------------------------
    sr = [
        "# Phase 04 — Split Report",
        "",
        "## Strategy",
        "",
        f"- Method: **{cfg['split']['strategy']}** (sorted by `{cfg['split']['sort_column']}`)",
        f"- Ratios: train {cfg['split']['train_ratio']:.0%} / "
        f"validation {cfg['split']['validation_ratio']:.0%} / "
        f"test {cfg['split']['test_ratio']:.0%}",
        "",
        "## Split sizes",
        "",
        "| split | rows | date start | date end |",
        "| --- | --- | --- | --- |",
        f"| train | {split_meta['n_train']} | {split_meta['train_date_start']} | {split_meta['train_date_end']} |",
        f"| validation | {split_meta['n_validation']} | {split_meta['validation_date_start']} | {split_meta['validation_date_end']} |",
        f"| test | {split_meta['n_test']} | {split_meta['test_date_start']} | {split_meta['test_date_end']} |",
        f"| **total** | **{n_in}** | | |",
        "",
        "## Data leakage checks",
        "",
        f"- Train max date < validation min date: **{no_train_val_overlap}** "
        f"({train_max.date()} < {val_min.date()})",
        f"- Validation max date < test min date: **{no_val_test_overlap}** "
        f"({val_max.date()} < {test_min.date()})",
        f"- All input rows assigned to exactly one split: **{rows_preserved}**",
        f"- Preprocessing fitted on train only: **True**",
        f"- Interim input unchanged (MD5 `{interim_md5_before}`): "
        f"**{interim_md5_before == interim_md5_after}**",
        "",
        "## Calendar gaps",
        "",
        "- The 17 missing calendar days documented in Phase 03 are **not imputed** "
        "and **not filled** in this phase. Rows remain at observed daily timestamps only.",
    ]
    (REPORT_DIR / "split_report.md").write_text("\n".join(sr) + "\n")

    # ------------------------------------------------------------------
    # REPORT — preprocessing_log.csv
    # ------------------------------------------------------------------
    pd.DataFrame(log_rows).to_csv(REPORT_DIR / "preprocessing_log.csv", index=False)

    # ------------------------------------------------------------------
    # REPORT — preprocessing_summary.md
    # ------------------------------------------------------------------
    ps = [
        "# Phase 04 — Preprocessing Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Input: `{INTERIM_PATH.relative_to(ROOT)}` ({n_in} rows × {cols_in} cols)",
        f"- Output splits: `{PROCESSED_DIR.relative_to(ROOT)}/`",
        f"- Pipeline: `{PIPELINE_PATH.relative_to(ROOT)}`",
        f"- Config: `{CONFIG_PATH.relative_to(ROOT)}`",
        "",
        "## Split strategy",
        "",
        f"- Chronological split on `{datetime_col}`: "
        f"{split_meta['n_train']} / {split_meta['n_validation']} / {split_meta['n_test']} "
        f"(train / validation / test).",
        "",
        "## Encoding strategy",
        "",
        "- Categorical columns encoded with `OneHotEncoder` (`handle_unknown=ignore`), "
        "fitted on train categories only:",
        f"  - `{categorical_cols[0]}`, `{categorical_cols[1]}`, `{categorical_cols[2]}`",
        f"- Encoded feature count: {len(feature_names) - len(numeric_cols)} "
        f"(from {len(categorical_cols)} source columns).",
        "",
        "## Scaling strategy",
        "",
        f"- `{cfg['scaling']['method'].title()}Scaler` applied to {len(numeric_cols)} numeric columns, "
        f"parameters learned from **train split only**.",
        f"- Processed numeric features stored as `{float_dtype}`.",
        "",
        "## Output schema",
        "",
        f"- Each processed split: `{datetime_col}` + {len(feature_names)} transformed features "
        f"= **{train_proc.shape[1]} columns**.",
        f"- No new predictive features created; only encoding/scaling of existing columns.",
        "",
        "## Data leakage prevention",
        "",
        "- Chronological split performed **before** fitting transformers.",
        "- `StandardScaler` and `OneHotEncoder` fitted exclusively on train.",
        "- Validation and test transformed with frozen train parameters.",
        f"- Temporal ordering preserved; leakage checks passed: "
        f"train<val={no_train_val_overlap}, val<test={no_val_test_overlap}.",
        "",
        "## Scope compliance",
        "",
        "- No feature engineering, rolling statistics, lag features, graph construction, "
        "model training, hyperparameter tuning, or target balancing performed.",
        "- Locked phase outputs (Phases 01–03) were not modified.",
        "",
        "## Reports",
        "",
        "- `preprocessing_summary.md`",
        "- `encoding_report.csv`",
        "- `scaling_report.csv`",
        "- `split_report.md`",
        "- `preprocessing_log.csv`",
    ]
    (REPORT_DIR / "preprocessing_summary.md").write_text("\n".join(ps) + "\n")

    print("Phase 04 preprocessing complete.")
    print(f"Rows in: {n_in} -> train/val/test: {split_meta['n_train']}/{split_meta['n_validation']}/{split_meta['n_test']}")
    print(f"Processed features: {len(feature_names)} (+ Date)")
    print(f"Leakage checks: train<val={no_train_val_overlap}, val<test={no_val_test_overlap}")
    print(f"Interim MD5 unchanged: {interim_md5_before == interim_md5_after}")
    print(f"Processed -> {PROCESSED_DIR.relative_to(ROOT)}")
    print(f"Pipeline -> {PIPELINE_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
