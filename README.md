# ab-test-analyzer
Описание: платформа анализа A/B-экспериментов. Frequentist + Bayesian + Sequential testing + MDE-калькулятор + sanity checks.  Стек: FastAPI, PostgreSQL, SciPy, statsmodels, Streamlit, Docker.
# ab-test-analyzer

Платформа анализа A/B-экспериментов.

## Возможности
- Частотный тест (z-test, CI, p-value)
- Байесовский анализ (Beta-Binomial)
- Sequential testing (O'Brien-Fleming)
- MDE-калькулятор (sample size, длительность)
- Sanity checks (SRM, малая выборка)
- Streamlit-дашборд

## Быстрый старт
cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501
