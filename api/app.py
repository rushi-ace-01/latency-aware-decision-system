from fastapi import FastAPI
import pandas as pd

from data.synthetic_generator import generate_time_series
from core.features import compute_features
from core.model import prepare_dataset, build_model
from core.latency import LatencySimulator
from core.decision import DecisionEngine
from evaluation.metrics import get_feature_contributions, explain_decision

app = FastAPI(title="Latency-Aware Decision System")

# --- Initialize system once (important) ---

df = generate_time_series()
features_df = compute_features(df)
X, y = prepare_dataset(features_df)

model = build_model()
model.fit(X, y)

latency_sim = LatencySimulator()
decision_engine = DecisionEngine()


@app.post("/decide")
def make_decision(sample_index: int = 0):
    """
    Make a latency-aware decision for a given sample index.
    """

    sample_X = X.iloc[[sample_index]]

    probability = model.predict_proba(sample_X)[0, 1]

    latency_info = latency_sim.simulate()

    decision = decision_engine.decide(probability, latency_info)

    feature_contrib = get_feature_contributions(model, sample_X)
    explanation = explain_decision(decision, feature_contrib)

    return {
        "probability": probability,
        "latency_ms": latency_info["total"],
        "decision": decision,
        "explanation": explanation,
    }
