Read:

Architecture Freeze Revision outputs (`Final_Architecture_Decision.md`, `final_model_specification.md`).

Execute ONLY Experiment 04.

Load the frozen S2 checkpoint (Exp03 A6). Do NOT retrain.

Run explainability analysis per Phase 12 / Sprint 04 protocol:

- SHAP (demand + stress)
- Attention extraction (spatial + temporal)
- Permutation importance
- Cross-method validation

Use identical dataset and splits.

Do NOT modify benchmark or ablation results.

Generate manuscript-ready explainability artefacts under `results/explainability/`.

Execute only Experiment 04.
