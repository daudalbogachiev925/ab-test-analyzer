from app.core.mde import sample_size, days_needed

def test_sample_size():
    n = sample_size(0.10, 0.05)
    assert n > 10000

def test_days():
    assert days_needed(50000, 1000) == 100
