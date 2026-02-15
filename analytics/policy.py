from main import get_crossover_year

def compare_policies(policies=(0.05, 0.08, 0.12, 0.2)):
    return {p: get_crossover_year(p) for p in policies}
