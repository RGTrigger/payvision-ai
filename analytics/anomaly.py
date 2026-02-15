import numpy as np
import pandas as pd
from pathlib import Path


def detect_anomalies(threshold=2):
    """
    Detect abnormal spikes or drops in total transactions.

    threshold:
        number of standard deviations used to detect anomalies
    """

    # Load data directly (avoids circular import)
    data_dir = Path(__file__).resolve().parents[1] / "data"

    upi = pd.read_csv(data_dir / "final_upi_data_2016_2025.csv")
    cash = pd.read_csv(data_dir / "cash_data.csv")

    # Clean & prepare
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

    mean = total.mean()
    std = total.std()

    anomalies = df[
        (total > mean + threshold * std) |
        (total < mean - threshold * std)
    ]

    return anomalies[["Date", "UPI", "Cash"]]


def explain_anomalies():
    """
    Provide interpretation of detected anomalies.
    Used in reports & analytics.
    """
    anomalies = detect_anomalies()

    if anomalies.empty:
        return "No abnormal spikes detected."

    return (
        "Anomalies may indicate:\n"
        "• sudden digital adoption spikes\n"
        "• policy or regulatory changes\n"
        "• seasonal economic shifts\n"
        "• potential fraud or system misuse\n"
    )


def realtime_alert():
    """
    Returns system health status for monitoring.
    """
    anomalies = detect_anomalies()

    if not anomalies.empty:
        return "⚠ ALERT: Unusual transaction activity detected!"
    return "System Normal"
