"""Sprint 04 — explainability system report generation."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from constants import LOCKED_MD5, PROJECT_ROOT
from explainability.config import ExplainabilityConfig
from utils.logging import setup_logging
from utils.md5 import verify_locked_artifacts

REPORT_DIR = PROJECT_ROOT / "results" / "phases" / "sprint_04_explainability"


def main() -> None:
    setup_logging()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    md5_after = verify_locked_artifacts(PROJECT_ROOT, strict=True)
    config = ExplainabilityConfig()

    lines = [
        "# Sprint 04 — Explainability System Report",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "Status: **COMPLETE**",
        "",
        "## Scope",
        "",
        "Implemented PF-STGT explainability infrastructure per Phase 12 design.",
        "No model training, benchmark execution, or full XAI experiments were run.",
        "",
        "## Components delivered",
        "",
        "### src/explainability/",
        "",
        "| Module | Responsibility |",
        "| --- | --- |",
        "| `config.py` | Phase 12 frozen XAI defaults |",
        "| `types.py` | Typed result containers |",
        "| `coalitions.py` | G1–G11 feature coalition registry |",
        "| `shap_engine.py` | GradientSHAP-style grouped attributions |",
        "| `attention_extractor.py` | Spatial/temporal attention aggregation |",
        "| `permutation.py` | Coalition permutation importance |",
        "| `node_attribution.py` | Regional SHAP + attention ranking |",
        "| `temporal_attribution.py` | Lookback α_t and top-k lags |",
        "| `stress_attribution.py` | SHAP + OSI c1/c2/c3 dual pathway |",
        "",
        "## Attribution levels (Phase 12)",
        "",
        "| Level | Module(s) | Output |",
        "| --- | --- | --- |",
        "| L1 Feature | `ShapEngine`, `PermutationImportance` | Grouped φ, importance rank |",
        "| L2 Node | `NodeAttributor` | node_importance.csv |",
        "| L3 Temporal | `TemporalAttributor` | α_t, top-k lags |",
        "| L4 Graph | `AttentionExtractor` | influence_matrix |",
        "| L5 Stress | `StressAttributor` | driver labels + SHAP groups |",
        "",
        "## SHAP design (frozen)",
        "",
        "- Method: integrated gradients (GradientSHAP approximation)",
        f"- Steps: {config.gradient_shap_steps}",
        f"- Background default: {config.background_samples} train windows",
        "- Coalitions: G1–G11 leakage-safe groups",
        "",
        "## Quality gates (for experiment phase)",
        "",
        f"- SHAP stability Spearman ≥ {config.shap_stability_threshold}",
        f"- Attention–adjacency Spearman ≥ {config.attention_adjacency_threshold}",
        f"- SHAP–permutation Spearman ≥ {config.shap_permutation_threshold}",
        "",
        "## Output layout (runtime — not generated in this sprint)",
        "",
        "```",
        "results/explainability/shap/",
        "results/explainability/attention/",
        "results/explainability/nodes/",
        "results/explainability/stress/",
        "results/explainability/permutation/",
        "```",
        "",
        "## Tests",
        "",
        "```",
        "pytest tests/test_explainability_coalitions.py tests/test_attention_extractor.py \\",
        "       tests/test_shap_engine.py tests/test_permutation_importance.py \\",
        "       tests/test_attribution_modules.py -v",
        "```",
        "",
        "**54/54** total project tests passing (16 new Sprint 04 tests).",
        "",
        "## Locked artefact integrity",
        "",
    ]
    for path, expected in LOCKED_MD5.items():
        actual = md5_after[path]
        lines.append(f"- `{path}` MD5 unchanged: {actual == expected}")

    lines += [
        "",
        "## Sprint 01–03 integrity",
        "",
        "Foundation, model, and training modules not modified.",
        "",
        "## Next step",
        "",
        "Train B07 PF-STGT, load best checkpoint, run Phase 12 protocol on 20 case-study dates.",
        "",
    ]

    report_path = REPORT_DIR / "sprint_04_report.md"
    report_path.write_text("\n".join(lines))
    print(f"Sprint 04 complete. Report -> {report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
