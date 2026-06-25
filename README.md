# Bangladesh_SmartGrid_STGT

**An Explainable Spatio-Temporal Graph Transformer for Multi-Task Load Shedding
Forecasting and Operational Stress Assessment in Bangladesh Smart Power Networks**

A long-term AI research project investigating explainable spatio-temporal graph
transformer architectures for multi-task load shedding forecasting and
operational stress assessment across Bangladesh smart power networks.

---

## Raw data link

https://data.mendeley.com/datasets/x7r7wdb39k/1

Version 5

---

---

## Repository Status

The repository contains completed foundation sprints (data, models, training,
evaluation, explainability modules) and executed experiments **01–03B**.

**Architecture freeze (2026-06-25):** **S2** (Correlation-Only PF-STGT, Exp03 A6) is
the final model for Experiment 04 and manuscript work. **S1** (original hybrid PF-STGT W20)
remains the historical design reference and Exp02 benchmark B07.

See `experiments/architecture_freeze_revision/Final_Architecture_Decision.md`.

---

## Repository Structure

| Directory      | Purpose                                                            |
| -------------- | ----------------------------------------------------------------- |
| `data/`        | All datasets across the data lifecycle (raw → processed → graph). |
| `docs/`        | Project documentation, phases, reviews, and decision logs.        |
| `src/`         | Core source code (data, models, training, evaluation, etc.).      |
| `configs/`     | Configuration files for experiments and pipelines.                |
| `notebooks/`   | Exploratory and phase-wise research notebooks (Phase 01–16).      |
| `experiments/` | Experiment definitions (baseline, graph transformer, ablation).   |
| `results/`     | Generated figures, tables, metrics, predictions, statistics.      |
| `models/`      | Saved model artifacts.                                             |
| `checkpoints/` | Training checkpoints.                                              |
| `logs/`        | Training and execution logs.                                      |
| `paper/`       | Paper materials.         |
| `manuscript/`  | Paper drafts, Overleaf project, and submission materials.         |
| `scripts/`     | Utility and automation scripts.                                   |

---

## Getting Started

Environment setup (choose one):

```bash
# Using pip
pip install -r requirements.txt

# Using conda
conda env create -f environment.yml
```

---

## Project Phases

The research is organized into 16 sequential phases, mirrored under
`notebooks/phase_01` through `notebooks/phase_16` and documented in
`docs/phases/`.

---

## License

See [LICENSE](LICENSE).
