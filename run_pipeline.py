"""Run the full pipeline once: extract -> transform -> quality -> load.
Usage: python -m src.run_pipeline
"""
import sys

from .data_quality import run_checks, write_report
from .extract import extract
from .load import load
from .transform import transform


def main() -> int:
    df = transform(extract())
    if not write_report(run_checks(df)):
        print("[pipeline] FAILED quality checks.")
        return 1
    load()
    print("[pipeline] done. Run `dbt run && dbt test` to build the marts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
