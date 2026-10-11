import os
import requests
import streamlit as st

API = os.getenv("API_URL", "http://api:8000")
st.set_page_config(page_title="A/B Analyzer", layout="wide")
st.title("A/B Test Analyzer")

@st.cache_data(ttl=15)
def fetch(path):
    return requests.get(f"{API}{path}").json()

experiments = fetch("/api/experiments")
if not experiments:
    st.warning("Нет экспериментов")
    st.stop()

exp_id = st.sidebar.selectbox("Эксперимент",
                                [e["id"] for e in experiments],
                                format_func=lambda i: next(e["name"] for e in experiments if e["id"] == i))

st.subheader("Частотный анализ")
st.json(fetch(f"/api/analysis/{exp_id}/frequentist"))

st.subheader("Байесовский анализ")
st.json(fetch(f"/api/analysis/{exp_id}/bayesian"))

st.subheader("Sanity checks")
st.json(fetch(f"/api/analysis/{exp_id}/sanity"))

st.subheader("Sequential")
look = st.slider("Look", 1, 10, 1)
st.json(fetch(f"/api/analysis/{exp_id}/sequential?look={look}"))

st.subheader("MDE калькулятор")
baseline = st.number_input("Baseline rate", 0.001, 0.99, 0.10)
mde_rel = st.number_input("MDE (relative)", 0.001, 1.0, 0.05)
daily = st.number_input("Daily users", 100, 1000000, 1000)
if st.button("Рассчитать"):
    r = requests.post(f"{API}/api/mde", json={
        "baseline_rate": baseline, "mde_relative": mde_rel,
        "daily_users": int(daily)}).json()
    st.json(r)
