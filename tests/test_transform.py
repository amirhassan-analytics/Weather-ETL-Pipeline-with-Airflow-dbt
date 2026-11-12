"""Unit tests for the Weather transform and data-quality checks."""
import pandas as pd

from src.data_quality import run_checks
from src.transform import transform


def _sample():
    return pd.DataFrame({
        "time": ["2026-11-12T00:00", "2026-11-12T01:00", "2026-11-12T02:00"],
        "temperature_2m": [12.5, 99.0, 11.0],
        "relative_humidity_2m": [60, 55, 120],
        "precipitation": [0.0, None, 0.2],
        "wind_speed_10m": [5.0, 6.0, 4.0],
        "city": ["Milan", "Milan", "Milan"],
    })


def test_transform_drops_out_of_range_rows():
    df = transform(_sample())
    assert len(df) == 1
    assert df.iloc[0]["temperature_2m"] == 12.5


def test_quality_checks_fail_on_duplicates():
    df = pd.DataFrame({
        "city": ["Milan", "Milan"],
        "timestamp": pd.to_datetime(["2026-11-12T00:00", "2026-11-12T00:00"]),
        "temperature_2m": [12.5, 12.5],
    })
    assert not all(c["passed"] for c in run_checks(df))


def test_quality_checks_pass_on_clean_data():
    df = pd.DataFrame({
        "city": ["Milan", "Rome"],
        "timestamp": pd.to_datetime(["2026-11-12T00:00", "2026-11-12T00:00"]),
        "temperature_2m": [12.5, 15.0],
    })
    assert all(c["passed"] for c in run_checks(df))
