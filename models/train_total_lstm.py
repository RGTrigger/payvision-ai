import pandas as pd
import numpy as np
from pathlib import Path

from utils.preprocessing import prepare_lstm_data
from models.lstm_total import build_lstm_model

# -----------------------------
# PROJECT ROOT & PATHS
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"

# -----------------------------
# LOAD DATA
# -----------------------------
upi = pd.read_csv(DATA_DIR / "final_upi_data_2016_2025.csv")
cash = pd.read_csv(DATA_DIR / "cash_data.csv")

upi["UPI"] = upi["Value (In Cr.)"].str.replace(",", "").astype(float)
cash["Cash"] = cash["Cash_In_Circulation_Cr"].astype(float)

upi["Date"] = pd.to_datetime(upi["Month"])
cash["Date"] = pd.to_datetime(cash["Date"])

# -----------------------------
# ALIGN BY DATE
# -----------------------------
df = pd.merge(
    upi[["Date", "UPI"]],
    cash[["Date", "Cash"]],
    on="Date",
    how="inner"
)

total = df["UPI"].values + df["Cash"].values


# -----------------------------
# PREPARE DATA
# -----------------------------
X, y, scaler = prepare_lstm_data(total)

# -----------------------------
# BUILD & TRAIN MODEL
# -----------------------------
model = build_lstm_model((X.shape[1], 1))

model.fit(
    X,
    y,
    epochs=100,
    batch_size=32,
    verbose=1
)

# -----------------------------
# SAVE MODEL & SCALER
# -----------------------------
model.save(MODEL_DIR / "total_lstm_model.keras")
np.save(MODEL_DIR / "scaler.npy", scaler)

print("✅ Training complete. Model & scaler saved.")
