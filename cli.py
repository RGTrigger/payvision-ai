import typer
from rich import print

from cli.forecast import run_forecast
from cli.crossover import show_crossover
from cli.simulate import simulate_policy
from cli.report import generate_report

# NEW interactive menu
from cli.menu import interactive_menu

app = typer.Typer()

@app.command()
def forecast():
    """Run future forecast"""
    print("[cyan]Running forecast...[/cyan]")
    run_forecast()

@app.command()
def crossover():
    """Show crossover year"""
    show_crossover()

@app.command()
def simulate(policy: float = 0.08):
    """Simulate policy impact"""
    simulate_policy(policy)

@app.command()
def report():
    """Generate analysis report"""
    generate_report()

@app.command()
def menu():
    """Launch interactive menu"""
    interactive_menu()

if __name__ == "__main__":
    app()
