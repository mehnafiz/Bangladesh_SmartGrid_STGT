# Experiment 03A — Ablation Failure Investigation

## Objective

Investigate unexpected findings from Experiment 03.

---

## Inputs

Experiment 03 Results

Ablation Rankings

Component Contribution Analysis

Statistical Significance Results

---

## Findings To Investigate

### F1

Single-Task Model Outperforms PF-STGT

Question:

Why does A4 outperform A1?

---

### F2

No-Transformer Performs Similar To PF-STGT

Question:

Is the transformer learning meaningful temporal patterns?

---

### F3

Correlation-Only Graph Outperforms Hybrid Graph

Question:

Does the geographical graph introduce noise?

---

### F4

Hybrid Graph Contribution

Question:

Is the hybrid graph actually beneficial?

---

## Required Analyses

### A1

Representation Analysis

Compare latent representations between:

A1

A3

A4

---

### A2

Attention Utilization Analysis

Evaluate:

Transformer attention distributions.

---

### A3

Graph Contribution Analysis

Evaluate:

Geographical edges

vs

Correlation edges

---

### A4

Task Interference Analysis

Measure:

Demand gradients

vs

Stress gradients

---

### A5

Performance Trade-Off Analysis

Determine:

Whether multi-task improves OSI at the cost of demand.

---

## Required Outputs

task_interference_report.md

transformer_utilization_report.md

graph_contribution_report.md

tradeoff_analysis.md

root_cause_summary.md

recommendation_report.md

---

## Definition of Done

✔ Root causes identified

✔ Task interference analyzed

✔ Transformer utilization analyzed

✔ Graph contribution analyzed

✔ Recommendations produced

---

---

## Execution Record

**Date:** 2026-06-25
**Script:** `experiments/experiment_03A_ablation_failure_investigation/run_investigation.py`
