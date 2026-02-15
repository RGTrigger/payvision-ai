import numpy as np
import pandas as pd
from pathlib import Path


def forecast_confidence():
    """
    Generate forecast confidence bands based on
    historical variability.
    """

    data_dir = Path(__file__).resolve().parents[1] / "data"

    upi = pd.read_csv(data_dir / "final_upi_data_2016_2025.csv")
    cash = pd.read_csv(data_dir / "cash_data.csv")

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

    total = df["UPI"] + df["Cash"]

    # future timeline (same horizon as forecast)
    future_steps = 180
    years = np.linspace(
        df["Date"].dt.year.iloc[-1],
        df["Date"].dt.year.iloc[-1] + future_steps / 12,
        future_steps
    )

    # baseline projection (flat continuation)
    baseline = np.full(future_steps, total.iloc[-1])

    # confidence band using historical volatility
    std = total.std() * 0.05

    upper = baseline + std
    lower = baseline - std

    return years, baseline, upper, lower
