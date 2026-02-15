import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from analytics.anomaly import detect_anomalies
from analytics.uncertainty import forecast_confidence

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def anchor_forecast(forecast, last_actual):
    return forecast - forecast[0] + last_actual


def plot_substitution(
    years_hist,
    upi_hist,
    cash_hist,
    years_forecast,
    upi_forecast,
    cash_forecast
):
    upi_forecast = anchor_forecast(upi_forecast, upi_hist[-1])
    cash_forecast = anchor_forecast(cash_forecast, cash_hist[-1])

    plt.figure(figsize=(13, 7))

    # Historical
    plt.plot(years_hist, upi_hist, label="UPI (Historical)")
    plt.plot(years_hist, cash_hist, label="Cash (Historical)")

    # Forecast
    plt.plot(years_forecast, upi_forecast, "--", label="UPI Forecast")
    plt.plot(years_forecast, cash_forecast, "--", label="Cash Forecast")

    # ✅ CONFIDENCE BANDS
    years, total, upper, lower = forecast_confidence()
    plt.fill_between(years, lower, upper, alpha=0.15, label="Forecast Confidence")

    # Intersection
    idx = np.where(upi_forecast >= cash_forecast)[0][0]
    plt.scatter(years_forecast[idx], upi_forecast[idx], color="red", zorder=5)

    # ✅ ANOMALY MARKERS
    anomalies = detect_anomalies()
    if not anomalies.empty:
        anomaly_years = anomalies["Date"].dt.year
        anomaly_vals = anomalies["UPI"] + anomalies["Cash"]

        plt.scatter(
            anomaly_years,
            anomaly_vals,
            color="orange",
            marker="x",
            s=80,
            label="Anomalies Detected"
        )

    plt.title("Digital Payment Adoption Forecast")
    plt.xlabel("Year")
    plt.ylabel("Transaction Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "forecast.png", dpi=300, bbox_inches="tight")
    plt.show()
