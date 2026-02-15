from rich import print
from main import run_analysis


def run_forecast():
    print("[cyan]Generating forecast & visualization...[/cyan]")
    run_analysis(show_plot=True)
