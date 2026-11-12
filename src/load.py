"""Load: write the cleaned data into PostgreSQL (staging table for dbt)."""
import pandas as pd
from sqlalchemy import create_engine, text

from .config import DATABASE_URL, STAGING_DIR


def load() -> None:
    engine = create_engine(DATABASE_URL)
    schema = (STAGING_DIR.parent.parent / "sql" / "schema.sql").read_text()
    with engine.begin() as conn:
        for statement in schema.split(";"):
            if statement.strip():
                conn.execute(text(statement))
    df = pd.read_parquet(STAGING_DIR / "weather_clean.parquet")
    df.to_sql("staging_weather", engine, if_exists="replace", index=False)
    print(f"[load] staging_weather: {len(df):,} rows")


if __name__ == "__main__":
    load()
