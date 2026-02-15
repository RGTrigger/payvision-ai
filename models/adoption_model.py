import numpy as np


def logistic_adoption(months, k=0.085, t0=42, max_share=0.97):
    """
    Logistic policy-driven adoption curve for UPI
    """
    return max_share / (1 + np.exp(-k * (months - t0)))
