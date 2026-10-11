from app.core.bayesian import bayesian_ab

def test_bayes_probability():
    r = bayesian_ab(1000, 10000, 1200, 10000, n=5000)
    assert r["prob_treatment_better"] > 0.9
    assert r["expected_lift"] > 0

def test_ci_contains_lift():
    r = bayesian_ab(100, 1000, 110, 1000, n=5000)
    assert r["credible_interval_low"] <= r["expected_lift"] <= r["credible_interval_high"]
