# Latency-Aware Explainable Decision System

A systems-focused prototype for probabilistic decision-making under uncertainty.
This project emphasizes software engineering principles such as latency awareness,
clean abstractions, explainability, and robustness rather than domain-specific
financial strategies or alpha generation.

---

## Motivation

In real-world decision systems, model accuracy alone is insufficient.
Production systems must also consider:

- End-to-end latency constraints
- Uncertainty in predictions
- Explainability and debuggability
- Failure scenarios and degraded inputs

This project explores how probabilistic signals can be converted into
reliable decisions under strict system constraints.

---

## Project Scope (Important)

This project intentionally avoids domain-specific financial assumptions.
All data used is synthetic, and the focus is on system design, correctness,
and engineering trade-offs rather than optimizing business or trading outcomes.

---

## System Overview

The system follows a modular pipeline:

1. **Data Ingestion**  
   Time-series signals are generated or ingested with controlled noise and regimes.

2. **Feature Engineering**  
   Rolling statistics and signal transformations are computed efficiently.

3. **Probabilistic Modeling**  
   Models output calibrated probabilities rather than point predictions.

4. **Latency-Aware Decision Engine**  
   Decisions are gated by both confidence thresholds and latency budgets.

5. **Explainability & Monitoring**  
   Each decision includes feature-level explanations and system metrics.

---

## Key Design Principles

- **Latency awareness over raw accuracy**
- **Probabilistic reasoning over binary predictions**
- **Explainability by design**
- **Failure-tolerant system behavior**
- **Configuration-driven experimentation**

---

## Technology Stack

- Python
- NumPy / Pandas
- scikit-learn
- FastAPI (API layer)
- Streamlit (lightweight visualization)

---
## Running the Demo Locally

This project consists of two components:
1. A FastAPI backend (decision engine)
2. A Streamlit frontend (demo UI)

### 1. Clone the repository
```bash
git clone https://github.com/USERNAME/latency-aware-decision-system.git
cd latency-aware-decision-system
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3.Start the backend (FastAPI)
```bash
uvicorn api.app:app --reload
```
### 4.Start the frontend (Streamlit)
Open a new terminal and run:
```bash
streamlit run experiments/demo_app.py
```

