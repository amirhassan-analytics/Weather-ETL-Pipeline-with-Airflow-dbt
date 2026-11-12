"""Airflow DAG: weather ETL, daily at 06:00.

extract -> transform -> data quality gate -> load -> dbt run -> dbt test
The quality gate raises if any check fails, so bad data never reaches
the warehouse and dbt never runs on it.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from src.data_quality import run_checks, write_report
from src.extract import extract
from src.load import load
from src.transform import transform

default_args = {
    "owner": "amirhassan",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def _quality_gate(**context):
    import pandas as pd
    from src.config import STAGING_DIR

    df = pd.read_parquet(STAGING_DIR / "weather_clean.parquet")
    if not write_report(run_checks(df)):
        raise ValueError("Data quality checks failed — see reports/data_quality.json")


with DAG(
    dag_id="weather_etl",
    default_args=default_args,
    description="Daily weather ETL: Open-Meteo API -> PostgreSQL -> dbt",
    schedule_interval="@daily",
    start_date=datetime(2026, 11, 12),
    catchup=False,
    tags=["etl", "weather", "dbt"],
) as dag:
    t_extract = PythonOperator(task_id="extract", python_callable=extract)
    t_transform = PythonOperator(
        task_id="transform",
        python_callable=lambda: transform(
            __import__("pandas").read_parquet("data/staging/weather_raw.parquet")
        ),
    )
    t_quality = PythonOperator(task_id="data_quality_gate", python_callable=_quality_gate)
    t_load = PythonOperator(task_id="load", python_callable=load)
    t_dbt_run = BashOperator(task_id="dbt_run", bash_command="dbt run")
    t_dbt_test = BashOperator(task_id="dbt_test", bash_command="dbt test")

    t_extract >> t_transform >> t_quality >> t_load >> t_dbt_run >> t_dbt_test
