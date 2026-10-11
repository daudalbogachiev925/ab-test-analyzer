import numpy as np
from scipy import stats

def sample_size(baseline_rate, mde_relative, alpha=0.05, power=0.80):
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde_relative)
    p_avg = (p1 + p2) / 2
    z_a = stats.norm.ppf(1 - alpha / 2)
    z_b = stats.norm.ppf(power)
    n = ((z_a * np.sqrt(2 * p_avg * (1 - p_avg))
          + z_b * np.sqrt(p1*(1-p1) + p2*(1-p2))) / (p2 - p1)) ** 2
    return int(np.ceil(n))

def days_needed(n_per_variant, daily_users):
    return (2 * n_per_variant) / daily_users if daily_users > 0 else float("inf")
