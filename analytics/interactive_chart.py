import plotly.graph_objects as go
from pathlib import Path
from main import forecast_transactions

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def interactive_forecast():
    _, _, _, years, upi, cash = forecast_transactions()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years, y=upi,
        mode='lines',
        name='UPI'
    ))

    fig.add_trace(go.Scatter(
        x=years, y=cash,
        mode='lines',
        name='Cash'
    ))

    fig.update_layout(
        title="Interactive Digital Payment Forecast",
        xaxis_title="Year",
        yaxis_title="Transaction Value",
        hovermode="x unified"
    )

    fig.write_html(OUTPUT_DIR / "interactive_forecast.html")
    fig.show()
