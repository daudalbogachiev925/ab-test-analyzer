import numpy as np
from scipy import stats

def two_proportion_test(control_users, control_conv, treat_users, treat_conv,
                        alpha=0.05):
    if control_users <= 0 or treat_users <= 0:
        return {"error": "no users"}
    p1 = control_conv / control_users
    p2 = treat_conv / treat_users
    p_pool = (control_conv + treat_conv) / (control_users + treat_users)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/control_users + 1/treat_users))
    if se == 0:
        return {"error": "zero variance"}
    z = (p2 - p1) / se
    p_val = 2 * (1 - stats.norm.cdf(abs(z)))
    se_diff = np.sqrt(p1*(1-p1)/control_users + p2*(1-p2)/treat_users)
    z_crit = stats.norm.ppf(1 - alpha/2)
    return {
        "control_rate": float(p1),
        "treatment_rate": float(p2),
        "absolute_lift": float(p2 - p1),
        "relative_lift": float((p2 - p1) / p1) if p1 > 0 else 0.0,
        "p_value": float(p_val),
        "z_score": float(z),
        "ci_low": float((p2 - p1) - z_crit * se_diff),
        "ci_high": float((p2 - p1) + z_crit * se_diff),
        "significant": bool(p_val < alpha),
    }
