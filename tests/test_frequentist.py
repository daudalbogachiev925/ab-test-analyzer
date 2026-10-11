from app.core.frequentist import two_proportion_test

def test_significant():
    r = two_proportion_test(10000, 1000, 10000, 1200)
    assert r["significant"] is True
    assert r["relative_lift"] > 0

def test_not_significant():
    r = two_proportion_test(100, 10, 100, 11)
    assert r["significant"] is False

def test_zero_users():
    r = two_proportion_test(0, 0, 100, 10)
    assert "error" in r
