import pandas as pd


def compute_features(
    df: pd.DataFrame,
    window_size: int = 20
) -> pd.DataFrame:
    """
    Compute rolling time-series features from a raw signal.

    All features are backward-looking to avoid data leakage.
    """

    features = df.copy()

    # Rolling mean
    features["rolling_mean"] = (
        features["signal"]
        .rolling(window=window_size, min_periods=window_size)
        .mean()
    )

    # Rolling standard deviation
    features["rolling_std"] = (
        features["signal"]
        .rolling(window=window_size, min_periods=window_size)
        .std()
    )

    # Momentum: difference over window
    features["momentum"] = (
        features["signal"] - features["signal"].shift(window_size)
    )

    # Rate of change (first difference)
    features["delta"] = features["signal"].diff()

    # Drop rows with incomplete feature windows
    features = features.dropna().reset_index(drop=True)

    return features


if __name__ == "__main__":
    from data.synthetic_generator import generate_time_series

    df = generate_time_series()
    features_df = compute_features(df)

    print(features_df.head())
