"""Data quality checks — run before load; a failed check stops the DAG."""
import json

import pandas as pd

from .config import REPORTS_DIR


def run_checks(df: pd.DataFrame) -> list[dict]:
    checks = [
        {"name": "row_count", "passed": len(df) > 0,
         "details": f"{len(df):,} rows"},
    ]
    if "city" in df.columns:
        checks.append({"name": "no_null_city",
                       "passed": int(df["city"].isna().sum()) == 0,
                       "details": f"{int(df['city'].isna().sum())} null cities"})
    if "timestamp" in df.columns:
        checks.append({"name": "no_duplicate_city_timestamp",
                       "passed": int(df.duplicated(subset=["city", "timestamp"]).sum()) == 0,
                       "details": f"{int(df.duplicated(subset=['city', 'timestamp']).sum())} duplicates"})
    if "temperature_2m" in df.columns:
        bad = int(((df["temperature_2m"] < -30) | (df["temperature_2m"] > 50)).sum())
        checks.append({"name": "range_temperature", "passed": bad == 0,
                       "details": f"{bad} values outside [-30, 50]"})
    return checks


def write_report(checks: list[dict]) -> bool:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    passed = all(c["passed"] for c in checks)
    (REPORTS_DIR / "data_quality.json").write_text(
        json.dumps({"passed": passed, "checks": checks}, indent=2)
    )
    for c in checks:
        print(f"[quality] {'PASS' if c['passed'] else 'FAIL'} {c['name']}: {c['details']}")
    return passed
