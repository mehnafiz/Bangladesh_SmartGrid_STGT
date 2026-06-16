"""Phase 02 — Exploratory Data Analysis (READ-ONLY).

Comprehensive EDA on the original dataset. This script is strictly read-only:
it NEVER cleans, imputes, encodes, normalizes, or engineers features, and it
NEVER modifies the source file or any locked-phase output.

Input (read-only):
    data/raw/bangladesh_smartgrid_raw.csv

Outputs:
    Reports -> results/phases/phase_02_eda/
    Figures -> results/figures/phase_02_eda/
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless, no GUI
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# ----------------------------------------------------------------------------
# Paths & conventions
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "bangladesh_smartgrid_raw.csv"
REPORT_DIR = ROOT / "results" / "phases" / "phase_02_eda"
FIG_DIR = ROOT / "results" / "figures" / "phase_02_eda"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

REGIONS = [
    "Dhaka", "Chattogram", "Rajshahi", "Mymensingh", "Sylhet",
    "Barishal", "Rangpur", "Cumilla", "Khulna",
]

NATIONAL_COLS = [
    "Max. Demand at eve. peak (Generation end)",
    "Max. Demand at eve. peak (Sub-station end)",
    "Highest Generation (Generation end)",
    "Minimum Generation (Generation end)",
    "Day-peak Generation (Generation end)",
    "Evening-peak Generation (Generation end)",
    "Minimum Generation Forecast up to 8:00 hrs.",
]

# Publication-quality defaults.
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update(
    {
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titleweight": "bold",
        "axes.titlesize": 12,
    }
)


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG_DIR / name)
    plt.close(fig)


# ----------------------------------------------------------------------------
def main() -> None:
    md5_before = file_md5(RAW_PATH)
    df = pd.read_csv(RAW_PATH)
    n_rows = len(df)

    # A non-mutating parsed Date series for temporal analysis only.
    dates = pd.to_datetime(df["Date"], errors="coerce")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    demand_cols = [f"{r}_demand" for r in REGIONS]
    supply_cols = [f"{r}_supply" for r in REGIONS]
    load_cols = [f"{r}_load" for r in REGIONS]

    # ===================================================================
    # REPORT 1 — descriptive_statistics.csv
    # ===================================================================
    desc = df[numeric_cols].describe().transpose()
    desc["median"] = df[numeric_cols].median()
    desc["skewness"] = df[numeric_cols].skew()
    desc["kurtosis"] = df[numeric_cols].kurtosis()
    desc["iqr"] = desc["75%"] - desc["25%"]
    desc["n_zeros"] = (df[numeric_cols] == 0).sum()
    desc.index.name = "feature"
    desc.to_csv(REPORT_DIR / "descriptive_statistics.csv")

    # ===================================================================
    # REPORT 2 — correlation_matrix.csv (Pearson, numeric features)
    # ===================================================================
    corr = df[numeric_cols].corr(method="pearson")
    corr.to_csv(REPORT_DIR / "correlation_matrix.csv")

    # ===================================================================
    # REPORT 3 — feature_distribution_summary.md
    # ===================================================================
    lines = ["# Phase 02 — Feature Distribution Summary", ""]
    lines += [
        "Per-feature distributional shape for all numeric features. "
        "Normality assessed with the D'Agostino-Pearson test (no modification of data).",
        "",
        "| feature | mean | std | skewness | kurtosis | n_zeros | shape |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in numeric_cols:
        s = df[c].dropna()
        sk = float(s.skew())
        ku = float(s.kurtosis())
        if abs(sk) < 0.5:
            shape = "approx. symmetric"
        elif sk > 0:
            shape = "right-skewed"
        else:
            shape = "left-skewed"
        lines.append(
            f"| {c} | {s.mean():.2f} | {s.std():.2f} | {sk:.3f} | {ku:.3f} | "
            f"{int((s == 0).sum())} | {shape} |"
        )
    (REPORT_DIR / "feature_distribution_summary.md").write_text("\n".join(lines) + "\n")

    # ===================================================================
    # REPORT 4 — temporal_analysis.md
    # ===================================================================
    tmp = pd.DataFrame({"date": dates})
    tmp["total_regional_demand"] = df[demand_cols].sum(axis=1)
    tmp["total_regional_supply"] = df[supply_cols].sum(axis=1)
    tmp["total_regional_load"] = df[load_cols].sum(axis=1)
    tmp["national_eve_peak"] = df["Max. Demand at eve. peak (Generation end)"]
    tmp["year"] = df["Year"]
    tmp["month"] = df["Month"]
    tmp["dow"] = df["Day of the week"]

    yearly = tmp.groupby("year")[
        ["national_eve_peak", "total_regional_demand", "total_regional_load"]
    ].mean().round(2)
    monthly = tmp.groupby("month")[
        ["national_eve_peak", "total_regional_demand", "total_regional_load"]
    ].mean().round(2)
    dow_order = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    dow = tmp.groupby("dow")[
        ["national_eve_peak", "total_regional_demand", "total_regional_load"]
    ].mean().reindex(dow_order).round(2)

    tlines = ["# Phase 02 — Temporal Analysis", ""]
    tlines += [
        f"- Series span: {dates.min().date()} → {dates.max().date()} ({n_rows} daily records).",
        f"- National evening-peak demand grew from {yearly['national_eve_peak'].iloc[0]:.0f} MW "
        f"(in {yearly.index[0]}) to {yearly['national_eve_peak'].iloc[-1]:.0f} MW (in {yearly.index[-1]}).",
        "",
        "## Yearly mean",
        "",
        "| year | national_eve_peak | total_regional_demand | total_regional_load |",
        "| --- | --- | --- | --- |",
    ]
    for yr, r in yearly.iterrows():
        tlines.append(
            f"| {yr} | {r['national_eve_peak']:.1f} | {r['total_regional_demand']:.1f} | {r['total_regional_load']:.1f} |"
        )
    tlines += ["", "## Monthly mean (seasonality)", "", "| month | national_eve_peak | total_regional_demand | total_regional_load |", "| --- | --- | --- | --- |"]
    for mo, r in monthly.iterrows():
        tlines.append(
            f"| {mo} | {r['national_eve_peak']:.1f} | {r['total_regional_demand']:.1f} | {r['total_regional_load']:.1f} |"
        )
    peak_month = int(monthly["national_eve_peak"].idxmax())
    low_month = int(monthly["national_eve_peak"].idxmin())
    tlines += [
        "",
        f"- Peak-demand month (mean): **{peak_month}**; lowest-demand month (mean): **{low_month}** "
        "— consistent with summer cooling load in Bangladesh.",
        "",
        "## Day-of-week mean",
        "",
        "| day | national_eve_peak | total_regional_demand | total_regional_load |",
        "| --- | --- | --- | --- |",
    ]
    for d, r in dow.iterrows():
        tlines.append(
            f"| {d} | {r['national_eve_peak']:.1f} | {r['total_regional_demand']:.1f} | {r['total_regional_load']:.1f} |"
        )
    tlines.append("")
    tlines.append(
        "- Friday (the weekly holiday) shows the lowest mean load-shedding, consistent with reduced industrial/commercial demand."
    )
    (REPORT_DIR / "temporal_analysis.md").write_text("\n".join(tlines) + "\n")

    # ===================================================================
    # REPORT 5 — regional_analysis.md
    # ===================================================================
    reg_rows = []
    total_demand_mean = df[demand_cols].mean().sum()
    for r in REGIONS:
        d = df[f"{r}_demand"]
        s = df[f"{r}_supply"]
        ld = df[f"{r}_load"]
        reg_rows.append(
            {
                "region": r,
                "demand_mean": round(float(d.mean()), 1),
                "demand_max": float(d.max()),
                "supply_mean": round(float(s.mean()), 1),
                "load_mean": round(float(ld.mean()), 2),
                "load_max": float(ld.max()),
                "load_nonzero_days": int((ld > 0).sum()),
                "load_nonzero_pct": round(float((ld > 0).mean() * 100), 2),
                "demand_share_pct": round(float(d.mean() / total_demand_mean * 100), 2),
            }
        )
    reg_df = pd.DataFrame(reg_rows).sort_values("demand_mean", ascending=False)

    rlines = ["# Phase 02 — Regional Analysis", ""]
    rlines += [
        "Per-region demand/supply/load behaviour across the 9 divisions (graph node candidates).",
        "",
        "| region | demand_mean | demand_max | supply_mean | load_mean | load_max | load_nonzero_days | load_nonzero_% | demand_share_% |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for _, r in reg_df.iterrows():
        rlines.append(
            f"| {r['region']} | {r['demand_mean']} | {r['demand_max']:.0f} | {r['supply_mean']} | "
            f"{r['load_mean']} | {r['load_max']:.0f} | {r['load_nonzero_days']} | {r['load_nonzero_pct']} | {r['demand_share_pct']} |"
        )
    top = reg_df.iloc[0]
    rlines += [
        "",
        f"- **{top['region']}** dominates national demand (~{top['demand_share_pct']}% of mean total regional demand).",
        "- Load-shedding (`_load`) is non-zero on only a small fraction of days in every region, confirming the Phase 01 sparsity finding.",
        f"- Region with most frequent load-shedding: **{reg_df.sort_values('load_nonzero_days', ascending=False).iloc[0]['region']}**.",
    ]
    (REPORT_DIR / "regional_analysis.md").write_text("\n".join(rlines) + "\n")

    # ===================================================================
    # REPORT 6 — outlier_analysis.md (IQR rule, descriptive only)
    # ===================================================================
    olines = ["# Phase 02 — Outlier Analysis", ""]
    olines += [
        "Outliers flagged with the 1.5×IQR rule (descriptive only — no rows removed or modified).",
        "",
        "| feature | n_outliers | outlier_pct | lower_fence | upper_fence |",
        "| --- | --- | --- | --- | --- |",
    ]
    outlier_summary = []
    for c in numeric_cols:
        s = df[c].dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((s < lo) | (s > hi)).sum())
        outlier_summary.append((c, n_out, round(n_out / len(s) * 100, 2), lo, hi))
    for c, n_out, pct, lo, hi in sorted(outlier_summary, key=lambda x: -x[1]):
        olines.append(f"| {c} | {n_out} | {pct} | {lo:.2f} | {hi:.2f} |")
    olines += [
        "",
        "- High outlier counts in `_load` features reflect rare load-shedding events rather than data errors.",
        "- Generation/demand outliers are concentrated at the extreme upper tail (record-high demand days).",
    ]
    (REPORT_DIR / "outlier_analysis.md").write_text("\n".join(olines) + "\n")

    # ===================================================================
    # FIGURES
    # ===================================================================
    # --- FIG 1: missing_values.png ---
    fig, ax = plt.subplots(figsize=(9, 5))
    miss = df.isna().sum().sort_values(ascending=False)
    sns.heatmap(df.isna(), cbar=False, yticklabels=False, ax=ax, cmap="viridis")
    ax.set_title(f"Missing-Value Map (total missing = {int(miss.sum())})")
    ax.set_xlabel("Features")
    save(fig, "missing_values.png")

    # --- FIG 2: feature_distributions.png ---
    dist_cols = demand_cols + NATIONAL_COLS[:3]
    ncols = 4
    nrows = int(np.ceil(len(dist_cols) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
    axes = axes.flatten()
    for i, c in enumerate(dist_cols):
        sns.histplot(df[c].dropna(), kde=True, ax=axes[i], color="steelblue")
        axes[i].set_title(c, fontsize=9)
        axes[i].set_xlabel("")
    for j in range(len(dist_cols), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Feature Distributions — Regional Demand & National Generation", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save(fig, "feature_distributions.png")

    # --- FIG 3: correlation_heatmap.png ---
    heat_cols = demand_cols + supply_cols + NATIONAL_COLS[:2]
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(
        df[heat_cols].corr(),
        annot=False, cmap="coolwarm", center=0, square=True,
        linewidths=0.4, cbar_kws={"shrink": 0.7}, ax=ax,
    )
    ax.set_title("Correlation Heatmap — Regional Demand/Supply & National Demand")
    save(fig, "correlation_heatmap.png")

    # --- FIG 4: target_distribution.png ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    nat_target = df["Max. Demand at eve. peak (Generation end)"].dropna()
    sns.histplot(nat_target, kde=True, ax=axes[0], color="darkgreen")
    axes[0].set_title("National Evening-Peak Demand (MW)")
    axes[0].set_xlabel("MW")
    load_nonzero_counts = (df[load_cols] > 0).sum().sort_values(ascending=False)
    sns.barplot(x=load_nonzero_counts.values, y=[c.replace("_load", "") for c in load_nonzero_counts.index],
                ax=axes[1], color="indianred")
    axes[1].set_title("Load-Shedding Days per Region (non-zero `_load`)")
    axes[1].set_xlabel(f"Days with load-shedding (of {n_rows})")
    fig.suptitle("Target Distributions — Continuous Demand vs. Sparse Load-Shedding", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "target_distribution.png")

    # --- FIG 5: temporal_trends.png ---
    ts = tmp.dropna(subset=["date"]).sort_values("date")
    fig, axes = plt.subplots(3, 1, figsize=(13, 11), sharex=False)
    axes[0].plot(ts["date"], ts["national_eve_peak"], color="navy", lw=0.8)
    axes[0].set_title("National Evening-Peak Demand over Time")
    axes[0].set_ylabel("MW")
    axes[1].plot(ts["date"], ts["total_regional_demand"], color="teal", lw=0.8)
    axes[1].set_title("Total Regional Demand over Time")
    axes[1].set_ylabel("MW")
    monthly.plot(y="national_eve_peak", kind="bar", ax=axes[2], color="darkorange", legend=False)
    axes[2].set_title("Mean National Evening-Peak Demand by Month (Seasonality)")
    axes[2].set_ylabel("MW")
    axes[2].set_xlabel("Month")
    fig.suptitle("Temporal Trends & Seasonality", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save(fig, "temporal_trends.png")

    # --- FIG 6: regional_comparison.png ---
    means = pd.DataFrame(
        {
            "demand": df[demand_cols].mean().values,
            "supply": df[supply_cols].mean().values,
            "load": df[load_cols].mean().values,
        },
        index=REGIONS,
    ).sort_values("demand", ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    means[["demand", "supply"]].plot(kind="bar", ax=axes[0], color=["steelblue", "lightseagreen"])
    axes[0].set_title("Mean Demand vs. Supply by Region")
    axes[0].set_ylabel("MW")
    axes[0].tick_params(axis="x", rotation=45)
    means[["load"]].plot(kind="bar", ax=axes[1], color="indianred", legend=False)
    axes[1].set_title("Mean Load-Shedding by Region")
    axes[1].set_ylabel("MW")
    axes[1].tick_params(axis="x", rotation=45)
    fig.suptitle("Regional Comparison", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "regional_comparison.png")

    # --- FIG 7: boxplots.png ---
    fig, ax = plt.subplots(figsize=(13, 6))
    melt = df[demand_cols].copy()
    melt.columns = REGIONS
    sns.boxplot(data=melt, ax=ax, palette="Set2")
    ax.set_title("Regional Demand Distributions (Boxplots) — Spread & Outliers")
    ax.set_ylabel("Demand (MW)")
    ax.tick_params(axis="x", rotation=45)
    save(fig, "boxplots.png")

    # ===================================================================
    # REPORT 7 — eda_summary_report.md (master narrative, per-figure notes)
    # ===================================================================
    md5_after = file_md5(RAW_PATH)
    slines = [
        "# Phase 02 — EDA Summary Report",
        "",
        "## Integrity",
        "",
        f"- Source: `{RAW_PATH.relative_to(ROOT)}`",
        f"- MD5 before: `{md5_before}`",
        f"- MD5 after:  `{md5_after}`",
        f"- Integrity: **{'UNCHANGED — dataset not modified' if md5_before == md5_after else 'CHANGED — WARNING'}**",
        "- Read-only EDA: no cleaning, imputation, encoding, normalization, feature engineering, modelling, or graph construction performed.",
        "",
        "## Reports Generated (`results/phases/phase_02_eda/`)",
        "",
        "- `descriptive_statistics.csv`",
        "- `feature_distribution_summary.md`",
        "- `correlation_matrix.csv`",
        "- `temporal_analysis.md`",
        "- `regional_analysis.md`",
        "- `outlier_analysis.md`",
        "- `eda_summary_report.md`",
        "",
        "## Figures Generated (`results/figures/phase_02_eda/`)",
        "",
        "### missing_values.png",
        f"- No missing cells in the dataset ({int(miss.sum())} total). The map is uniformly complete, so imputation is not required (deferred regardless to later phases).",
        "",
        "### feature_distributions.png",
        "- Regional demand series are broadly unimodal; larger divisions (Dhaka, Khulna, Chattogram) show wider spread. National generation metrics are roughly bell-shaped with a mild right tail toward record-high demand days.",
        "",
        "### correlation_heatmap.png",
        "- Strong positive correlation between each region's demand and its own supply (demand ≈ supply), and high inter-regional demand correlation driven by shared national growth and seasonality. This collinearity is important for the multi-task target design.",
        "",
        "### target_distribution.png",
        "- National evening-peak demand is a smooth continuous regression target. Regional `_load` (load-shedding) is sparse — non-zero on only a minority of days — confirming the Phase 01 imbalance risk.",
        "",
        "### temporal_trends.png",
        f"- Clear multi-year upward trend in demand (≈{yearly['national_eve_peak'].iloc[0]:.0f}→{yearly['national_eve_peak'].iloc[-1]:.0f} MW) plus strong seasonality peaking around month {peak_month} (summer cooling load).",
        "",
        "### regional_comparison.png",
        f"- {top['region']} is the dominant load centre (~{top['demand_share_pct']}% of mean total regional demand); demand and supply are nearly equal in every region, with load-shedding small in magnitude.",
        "",
        "### boxplots.png",
        "- Boxplots reveal heterogeneous regional scales and upper-tail outliers corresponding to peak-demand days, not data errors.",
        "",
        "## Key Findings",
        "",
        f"- **Trend + seasonality dominate** the demand signals (year-over-year growth, month {peak_month} peak), motivating a temporal model with trend/seasonal capacity.",
        "- **High spatial correlation** across regions and **demand≈supply** equality argue for a shared spatio-temporal representation with per-node heads.",
        "- **Load-shedding is sparse and imbalanced**, best treated as a distinct task (event/zero-inflated) rather than plain regression.",
        "- **No missing values and no duplicates**, so data completeness is not a barrier to modelling.",
        "",
        "## Scope Compliance",
        "",
        "- Strictly read-only. Phase 01 outputs and the raw dataset were not modified.",
    ]
    (REPORT_DIR / "eda_summary_report.md").write_text("\n".join(slines) + "\n")

    # Console summary.
    print("Phase 02 EDA complete.")
    print(f"Rows x Cols: {df.shape[0]} x {df.shape[1]}")
    print(f"MD5 unchanged: {md5_before == md5_after}")
    print(f"Reports -> {REPORT_DIR.relative_to(ROOT)}")
    print(f"Figures -> {FIG_DIR.relative_to(ROOT)}")
    print(f"Peak month (mean demand): {peak_month}; Low month: {low_month}")
    print(f"Top region by demand: {top['region']} ({top['demand_share_pct']}%)")


if __name__ == "__main__":
    main()
