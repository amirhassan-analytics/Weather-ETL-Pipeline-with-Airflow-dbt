# Weather ETL Pipeline — Airflow + dbt + PostgreSQL

End-to-end scheduled ETL pipeline: pulls hourly weather data from the
**Open-Meteo API** (free, no key needed), cleans and validates it with
**dbt tests**, and loads it into a **PostgreSQL star schema** — orchestrated
by **Apache Airflow** and containerised with **Docker**.

## What it proves

- **Orchestration:** Airflow DAG with retries, scheduling and a quality gate
- **Transformation:** dbt models with tests (`unique`, `not_null`,
  `accepted_range`) — bad data fails the run, it never reaches the warehouse
- **Data quality:** row-count, null and range checks at every stage
- **Modelling:** star schema (`fact_weather`, `dim_date`, `dim_location`)

## Architecture

```
Open-Meteo API (hourly: temperature, humidity, wind, precipitation)
      │  extract.py  (Airflow: extract)
      ▼
data/staging/weather_raw.parquet
      │  transform.py  (Airflow: transform)
      ▼
data/staging/weather_clean.parquet
      │  load.py  (Airflow: load)
      ▼
PostgreSQL — staging_weather
      │  dbt run + dbt test  (Airflow: dbt)
      ▼
fact_weather  ·  dim_date  ·  dim_location
```

## Quick start

```bash
# 1. Start PostgreSQL + Airflow
docker compose up --build -d

# 2. Open Airflow at http://localhost:8080 (airflow / airflow)
#    and trigger the DAG: weather_etl

# Or run the pipeline once without Airflow:
pip install -r requirements.txt
python -m src.run_pipeline
dbt run && dbt test
```

## Project structure

```
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── dbt_project.yml
├── .env.example
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── data_quality.py
│   └── run_pipeline.py
├── sql/
│   └── schema.sql
├── models/
│   ├── staging_weather.sql
│   ├── fact_daily_weather.sql
│   └── schema.yml
├── dags/
│   └── weather_etl_dag.py
├── tests/
│   └── test_transform.py
├── data/
│   └── README.md
└── .github/workflows/ci.yml
```

## Tech

Python · Apache Airflow · dbt · PostgreSQL · Docker · pandas · SQL
