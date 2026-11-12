"""Extract: pull hourly weather from the Open-Meteo API (free, no key)."""
import pandas as pd
import requests

from .config import HOURLY_VARS, LOCATIONS, OPEN_METEO_URL, STAGING_DIR


def extract() -> pd.DataFrame:
    frames = []
    for city, (lat, lon) in LOCATIONS.items():
        resp = requests.get(
            OPEN_METEO_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": ",".join(HOURLY_VARS),
                "forecast_days": 7,
                "timezone": "Europe/Rome",
            },
            timeout=30,
        )
        resp.raise_for_status()
        hourly = resp.json()["hourly"]
        df = pd.DataFrame(hourly)
        df["city"] = city
        df["latitude"] = lat
        df["longitude"] = lon
        frames.append(df)

    out = pd.concat(frames, ignore_index=True)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    out.to_parquet(STAGING_DIR / "weather_raw.parquet", index=False)
    print(f"[extract] {len(out):,} rows, {len(LOCATIONS)} cities")
    return out


if __name__ == "__main__":
    extract()
