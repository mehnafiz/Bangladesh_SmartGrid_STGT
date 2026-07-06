# Experiment 04 — Explainability Analysis

## Objective

Analyze and explain the prediction behavior of the final S2 architecture (Correlation-Aware Multi-Task Forecasting Framework).

This experiment validates the interpretability of the proposed model and provides evidence for manuscript discussion.

---

## Final Model

S2 — Correlation-Aware Multi-Task Forecasting Framework

Components:

* Correlation Graph
* Multi-Task Learning
* Demand Forecasting Head
* Operational Stress Forecasting Head

---

## Explainability Objectives

### E1

Global Feature Importance

Determine the most influential input features.

---

### E2

Local Feature Attribution

Explain individual predictions using SHAP.

---

### E3

Node Attribution

Determine which regions contribute most to predictions.

---

### E4

Temporal Attribution

Identify the most influential historical timesteps.

---

### E5

Operational Stress Attribution

Identify the primary drivers of predicted Operational Stress Index (OSI).

---

### E6

Case Studies

Provide explanations for:

* Typical demand day
* High-demand day
* High-stress event
* Low-demand day

---

## Visualizations

Generate:

* SHAP Summary Plot
* SHAP Bar Plot
* Feature Importance Ranking
* Node Importance Heatmap
* Temporal Importance Plot
* Stress Attribution Plot

---

## Required Outputs

shap_summary.md

feature_importance.md

node_attribution.md

temporal_attribution.md

stress_attribution.md

case_studies.md

regional_analysis.md

xai_summary.md

---

## Definition of Done

✔ SHAP analysis completed

✔ Node attribution completed

✔ Temporal attribution completed

✔ Stress attribution completed

✔ Case studies completed

✔ Explainability report completed


---

---

## Execution Record

**Date:** 2026-07-06
**Model:** S2 (A6 checkpoint)
**Script:** `experiments/experiment_04_explainability_analysis/run_explainability.py`
**Deliverables:** 8 markdown reports + 7 figures
