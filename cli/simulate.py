from rich import print
from main import simulate_policy_effect


def simulate_policy(policy):
    year = simulate_policy_effect(policy)

    print(f"[yellow]Policy strength: {policy}[/yellow]")
    print(f"[green]New crossover year: {year}[/green]")
