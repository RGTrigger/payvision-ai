import pandas as pd
from pathlib import Path
from main import forecast_transactions

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def export_csv():
    _, _, _, years, upi, cash = forecast_transactions()

    df = pd.DataFrame({
        "Year": years,
        "UPI": upi,
        "Cash": cash
    })

    path = OUTPUT_DIR / "forecast.csv"
    df.to_csv(path, index=False)
    return path
