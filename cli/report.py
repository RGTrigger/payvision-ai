from rich.console import Console
from rich.table import Table
from main import summary_data
from analytics.metrics import advanced_metrics
from analytics.export import export_csv
from analytics.report import generate_pdf_report

console = Console()

def generate_report():
    base = summary_data()
    metrics = advanced_metrics()

    table = Table(title="Forecast Intelligence Report")
    table.add_column("Metric")
    table.add_column("Value")

    for k, v in {**base, **metrics}.items():
        table.add_row(k, str(v))

    console.print(table)

    console.print(f"\nCSV saved: {export_csv()}")
    console.print(f"PDF saved: {generate_pdf_report()}")
