def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

def test_create_experiment(client):
    r = client.post("/api/experiments", json={
        "name": "exp1", "baseline_rate": 0.1, "mde": 0.05})
    assert r.status_code == 201

def test_add_observation(client):
    e = client.post("/api/experiments", json={
        "name": "exp2", "baseline_rate": 0.1, "mde": 0.05}).json()
    r = client.post(f"/api/experiments/{e['id']}/observations", json={
        "variant": "control", "users": 1000, "conversions": 100})
    assert r.status_code == 201

def test_mde_endpoint(client):
    r = client.post("/api/mde", json={
        "baseline_rate": 0.1, "mde_relative": 0.05, "daily_users": 1000})
    assert r.status_code == 200
    assert r.json()["users_per_variant"] > 0
