import argparse
from datetime import datetime, date

from .application.use_cases import get_life_expectancy


ISO_FORMAT = "%Y-%m-%d"


USAGE = """Gets life expectancy from the Social Security Administration's website.

positional arguments:
  sex        "m" or "f"
  dob        Date of birth in YYYY-MM-DD format
"""


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("sex", help='"m" or "f"')
    p.add_argument("dob", help="Date of birth in YYYY-MM-DD format")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    ns = _parse_args(argv)
    sex = ns.sex
    try:
        dob_dt = datetime.strptime(ns.dob, ISO_FORMAT)
        dob: date = dob_dt.date()
    except Exception:
        print("dob must be in YYYY-MM-DD format")
        return 2

    try:
        resp = get_life_expectancy(sex, dob)
    except Exception as e:
        print(str(e))
        return 1

    dd = resp.estimated_death_date
    print(f"current age      = {resp.current_age:.2f}")
    print(f"additional years = {resp.additional_years:.2f}")
    print(f"total years      = {resp.total_years:.2f}")
    print(f"estimated death  = {dd.year:04d}-{dd.month:02d}-{dd.day:02d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
