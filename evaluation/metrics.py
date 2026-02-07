import numpy as np
import pandas as pd
from typing import Dict


def get_feature_contributions(
    model,
    X: pd.DataFrame
) -> Dict[str, float]:
    """
    Compute per-feature contributions for a logistic regression model.
    """

    # Extract trained classifier
    classifier = model.named_steps["classifier"]
    scaler = model.named_steps["scaler"]

    # Scale input features
    X_scaled = scaler.transform(X)

    weights = classifier.coef_[0]
    contributions = X_scaled[0] * weights

    feature_contrib = {
        feature: float(contrib)
        for feature, contrib in zip(X.columns, contributions)
    }

    return feature_contrib


def explain_decision(
    decision: Dict,
    feature_contrib: Dict[str, float]
) -> str:
    """
    Generate a human-readable explanation for a decision.
    """

    sorted_features = sorted(
        feature_contrib.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    top_features = sorted_features[:3]

    explanation = (
        f"Decision: {decision['reason']}. "
        f"Probability={decision['probability']:.2f}, "
        f"Latency={decision['latency_ms']:.1f} ms. "
        "Top contributing features: "
    )

    for feature, value in top_features:
        explanation += f"{feature} ({value:+.3f}), "

    return explanation.rstrip(", ")


def compute_feature_drift(
    features_df: pd.DataFrame,
    window_size: int = 100
) -> pd.DataFrame:
    """
    Compute rolling mean and std to monitor feature drift.
    """

    drift_metrics = {}

    for col in features_df.columns:
        drift_metrics[f"{col}_mean"] = (
            features_df[col]
            .rolling(window_size)
            .mean()
        )
        drift_metrics[f"{col}_std"] = (
            features_df[col]
            .rolling(window_size)
            .std()
        )

    return pd.DataFrame(drift_metrics)
