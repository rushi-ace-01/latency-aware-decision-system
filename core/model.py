import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def prepare_dataset(df: pd.DataFrame):
    """
    Prepare features and binary target for probabilistic modeling.
    Target = 1 if signal increases at next step, else 0.
    """

    df = df.copy()

    # Define target (next-step increase)
    df["target"] = (df["signal"].shift(-1) > df["signal"]).astype(int)

    # Drop last row (no future label)
    df = df.iloc[:-1]

    feature_cols = [
        "rolling_mean",
        "rolling_std",
        "momentum",
        "delta",
    ]

    X = df[feature_cols]
    y = df["target"]

    return X, y


def build_model():
    """
    Build a probabilistic classification model.
    Logistic Regression is chosen for interpretability and calibration.
    """

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    solver="lbfgs",
                    max_iter=1000
                ),
            ),
        ]
    )

    return model


if __name__ == "__main__":
    from data.synthetic_generator import generate_time_series
    from core.features import compute_features

    df = generate_time_series()
    features_df = compute_features(df)

    X, y = prepare_dataset(features_df)

    model = build_model()
    model.fit(X, y)

    probs = model.predict_proba(X)[:, 1]

    print("First 5 predicted probabilities:")
    print(probs[:5])
