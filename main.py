import os
import numpy as np
import pandas as pd
from pathlib import Path
import tensorflow as tf

from utils.plotting import plot_substitution

# Reduce TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# =============================
# PROJECT PATHS
# =============================
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

MODEL_PATH = MODEL_DIR / "total_lstm_model.keras"
SCALER_PATH = MODEL_DIR / "scaler.npy"

OUTPUT_DIR.mkdir(exist_ok=True)

# =============================
# LOAD & PREPARE DATA
# =============================
def load_data():
    upi = pd.read_csv(DATA_DIR / "final_upi_data_2016_2025.csv")
    cash = pd.read_csv(DATA_DIR / "cash_data.csv")

    upi["UPI"] = upi["Value (In Cr.)"].str.replace(",", "").astype(float)
    cash["Cash"] = cash["Cash_In_Circulation_Cr"].astype(float)

    upi["Date"] = pd.to_datetime(upi["Month"])
    cash["Date"] = pd.to_datetime(cash["Date"])

    df = pd.merge(
        upi[["Date", "UPI"]],
        cash[["Date", "Cash"]],
        on="Date",
        how="inner"
    )
    return df


# =============================
# LOAD MODEL (cached)
# =============================
_model = None
_scaler = None

def load_model():
    global _model, _scaler

    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
        _scaler = np.load(SCALER_PATH, allow_pickle=True).item()

    return _model, _scaler


# =============================
# FORECAST ENGINE
# =============================
def forecast_transactions(policy_strength=0.08, future_months=180):
    df = load_data()
    model, scaler = load_model()

    upi_hist = df["UPI"].values
    cash_hist = df["Cash"].values
    years_hist = df["Date"].dt.year + df["Date"].dt.month / 12

    total_hist = upi_hist + cash_hist
    total_scaled = scaler.transform(total_hist.reshape(-1, 1))

    LOOKBACK = 12
    X_last = total_scaled[-LOOKBACK:].reshape(1, LOOKBACK, 1)

    forecast_scaled = []

    predict = model.predict  # ⚡ performance boost

    for _ in range(future_months):
        pred = predict(X_last, verbose=0)[0, 0]
        forecast_scaled.append(pred)
        X_last = np.append(X_last[:, 1:, :], [[[pred]]], axis=1)

    total_forecast = scaler.inverse_transform(
        np.array(forecast_scaled).reshape(-1, 1)
    ).flatten()

    # Logistic policy-driven adoption
    t = np.arange(len(total_forecast))
    t0 = len(t) * 0.35
    upi_share = 1 / (1 + np.exp(-policy_strength * (t - t0)))

    upi_forecast = total_forecast * upi_share
    cash_forecast = total_forecast * (1 - upi_share)

    years_forecast = np.linspace(
        years_hist.iloc[-1],
        years_hist.iloc[-1] + len(total_forecast) / 12,
        len(total_forecast)
    )

    return (
        years_hist,
        upi_hist,
        cash_hist,
        years_forecast,
        upi_forecast,
        cash_forecast,
    )


# =============================
# CROSSOVER DETECTION
# =============================
def get_crossover_year(policy_strength=0.08):
    _, _, _, years_f, upi_f, cash_f = forecast_transactions(policy_strength)
    idx = np.where(upi_f - cash_f >= 0)[0][0]
    return round(years_f[idx], 1)


# =============================
# POLICY SIMULATION
# =============================
def simulate_policy_effect(policy_strength):
    return get_crossover_year(policy_strength)


# =============================
# SUMMARY INFO
# =============================
def summary_data():
    return {
        "Predicted Crossover Year": get_crossover_year(),
        "Policy Strength Used": 0.08,
        "Forecast Horizon": "15 Years",
        "Model": "LSTM + Logistic Adoption",
    }


# =============================
# RUN ANALYSIS
# =============================
def run_analysis():
    (
        years_hist,
        upi_hist,
        cash_hist,
        years_forecast,
        upi_forecast,
        cash_forecast,
    ) = forecast_transactions()

    plot_substitution(
        years_hist,
        upi_hist,
        cash_hist,
        years_forecast,
        upi_forecast,
        cash_forecast,
    )

    return years_forecast, upi_forecast, cash_forecast


# =============================
# DIRECT EXECUTION
# =============================
if __name__ == "__main__":
    print("\nRunning Digital Payment Forecast...\n")

    crossover = get_crossover_year()
    print(f"📊 UPI is predicted to overtake cash around: {crossover}")

    run_analysis()
