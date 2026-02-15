import numpy as np
from main import forecast_transactions

def advanced_metrics(policy_strength=0.08):
    (
        _,
        upi_hist,
        cash_hist,
        years_f,
        upi_f,
        cash_f,
    ) = forecast_transactions(policy_strength)

    idx_2035 = (np.abs(years_f - 2035)).argmin()

    upi_share_2035 = upi_f[idx_2035] / (upi_f[idx_2035] + cash_f[idx_2035])
    cash_share_2035 = 1 - upi_share_2035

    growth_rate = (upi_f[-1] - upi_hist[-1]) / upi_hist[-1] * 100
    adoption_speed = np.mean(np.diff(upi_f[:60]))

    return {
        "UPI Share 2035": f"{upi_share_2035*100:.2f}%",
        "Cash Share 2035": f"{cash_share_2035*100:.2f}%",
        "UPI Growth (15yr)": f"{growth_rate:.2f}%",
        "Adoption Speed Index": round(adoption_speed, 2),
    }
