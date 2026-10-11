import numpy as np
from scipy import stats

def obrien_fleming(n_looks, alpha=0.05):
    t = np.arange(1, n_looks + 1)
    fractions = t / n_looks
    return stats.norm.ppf(1 - alpha / (2 * n_looks * np.sqrt(fractions))).tolist()

def sequential_test(control_rate, treat_rate, users, n_looks=5,
                     current_look=1, alpha=0.05):
    bounds = obrien_fleming(n_looks, alpha)
    se = np.sqrt(control_rate*(1-control_rate)/users
                 + treat_rate*(1-treat_rate)/users)
    if se == 0:
        return {"z": 0.0, "boundary": bounds[current_look-1], "stop": False}
    z = (treat_rate - control_rate) / se
    b = bounds[current_look - 1]
    return {"z": float(z), "boundary": float(b),
            "stop": bool(abs(z) >= b), "look": current_look}
