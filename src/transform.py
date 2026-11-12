"""Transform: clean the raw API data.

- Rename columns to snake_case, parse timestamps.
- Drop rows with a missing timestamp or city.
- Clip temperature to a plausible range (-30 to 50 C) and humidity to [0, 100];
  drop rows outside those ranges instead of silently keeping bad data.
- Add a date column for the star schema.
"""
import pandas as pd

from .config import STAGING_DIR


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    df = df.rename(columns={"time": "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp", "city"])

    if "temperature_2m" in df.columns:
        df = df[(df["temperature_2m"] >= -30) & (df["temperature_2m"] <= 50)]
    if "relative_humidity_2m" in df.columns:
        df = df[(df["relative_humidity_2m"] >= 0) & (df["relative_humidity_2m"] <= 100)]
    if "precipitation" in df.columns:
        df["precipitation"] = df["precipitation"].fillna(0)

    df["date"] = df["timestamp"].dt.date
    df = df.drop_duplicates(subset=["city", "timestamp"])
    df.to_parquet(STAGING_DIR / "weather_clean.parquet", index=False)
    print(f"[transform] {len(df):,} rows")
    return df


if __name__ == "__main__":
    transform(pd.read_parquet(STAGING_DIR / "weather_raw.parquet"))
