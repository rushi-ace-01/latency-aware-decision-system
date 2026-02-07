import numpy as np
import pandas as pd


def generate_time_series(
    n_steps: int = 2000,
    low_noise_std: float = 0.3,
    high_noise_std: float = 1.2,
    regime_switch_prob: float = 0.01,
    anomaly_prob: float = 0.005,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generate a synthetic time-series with regime switching and anomalies.

    The goal is to simulate signals with uncertainty and non-stationarity
    without relying on domain-specific assumptions.
    """

    np.random.seed(random_seed)

    signal = np.zeros(n_steps)
    noise = np.zeros(n_steps)
    regime = np.zeros(n_steps, dtype=int)
    anomaly = np.zeros(n_steps, dtype=int)

    # Start in low-noise regime
    current_regime = 0  # 0 = low noise, 1 = high noise

    for t in range(1, n_steps):
        # Regime switching
        if np.random.rand() < regime_switch_prob:
            current_regime = 1 - current_regime

        regime[t] = current_regime

        # Noise generation based on regime
        std = low_noise_std if current_regime == 0 else high_noise_std
        eps = np.random.normal(0, std)

        # Anomaly injection
        if np.random.rand() < anomaly_prob:
            eps += np.random.normal(0, 5 * std)
            anomaly[t] = 1

        noise[t] = eps
        signal[t] = signal[t - 1] + eps

    df = pd.DataFrame({
        "timestamp": pd.date_range(start="2024-01-01", periods=n_steps, freq="S"),
        "signal": signal,
        "regime": regime,
        "noise": noise,
        "anomaly": anomaly
    })

    return df


if __name__ == "__main__":
    df = generate_time_series()
    df.to_csv("synthetic_time_series.csv", index=False)
    print(df.head())
