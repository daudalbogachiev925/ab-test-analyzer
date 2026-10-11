import numpy as np
from app.config import settings

def bayesian_ab(control_conv, control_users, treat_conv, treat_users, n=None):
    n = n or settings.BAYES_SAMPLES
    ctrl = np.random.beta(1 + control_conv, 1 + control_users - control_conv, n)
    treat = np.random.beta(1 + treat_conv, 1 + treat_users - treat_conv, n)
    diff = treat - ctrl
    return {
        "prob_treatment_better": float((treat > ctrl).mean()),
        "expected_lift": float(diff.mean()),
        "credible_interval_low": float(np.percentile(diff, 2.5)),
        "credible_interval_high": float(np.percentile(diff, 97.5)),
    }
