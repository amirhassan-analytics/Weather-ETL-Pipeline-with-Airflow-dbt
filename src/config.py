"""Central settings for the Weather ETL pipeline."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STAGING_DIR = BASE_DIR / "data" / "staging"
REPORTS_DIR = BASE_DIR / "reports"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://weather:weather@localhost:5432/weather",
)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Cities tracked — the cities from my job search.
LOCATIONS = {
    "Milan": (45.4642, 9.1900),
    "Rome": (41.9028, 12.4964),
    "Naples": (40.8518, 14.2681),
    "Turin": (45.0703, 7.6869),
    "Pisa": (43.7228, 10.4017),
}

HOURLY_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]
