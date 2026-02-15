from rich import print
from main import get_crossover_year


def show_crossover():
    year = get_crossover_year()
    print(f"[green]UPI overtakes Cash in: {year}[/green]")
