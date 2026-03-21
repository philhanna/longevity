import argparse
import csv
import sys
from datetime import datetime

from .application.use_cases import get_life_expectancy, LongevityError

ISO_FORMAT = "%Y-%m-%d"

OUTPUT_COLUMNS = ["current_age", "additional_years", "total_years", "estimated_death_date"]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Batch life-expectancy calculator. Reads a CSV, calls the SSA calculator for each row, writes results to an output CSV."
    )
    p.add_argument("input", help="Input CSV file path")
    p.add_argument("output", help="Output CSV file path")
    p.add_argument("--sex-col", default="Sex", help='Column name for sex (default: "Sex")')
    p.add_argument("--dob-col", default="DOB", help='Column name for date of birth (default: "DOB")')
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    ns = _parse_args(argv)

    try:
        in_f = open(ns.input, newline="", encoding="utf-8")
    except OSError as e:
        print(f"cannot open input file: {e}", file=sys.stderr)
        return 2

    with in_f:
        reader = csv.DictReader(in_f)
        if reader.fieldnames is None:
            print("input CSV is empty", file=sys.stderr)
            return 2

        fieldnames = list(reader.fieldnames)
        for col in (ns.sex_col, ns.dob_col):
            if col not in fieldnames:
                print(f"column {col!r} not found in input CSV (columns: {fieldnames})", file=sys.stderr)
                return 2

        # Output columns: all originals + calculated fields + error
        out_fieldnames = fieldnames + [c for c in OUTPUT_COLUMNS if c not in fieldnames] + ["error"]

        rows = list(reader)

    try:
        out_f = open(ns.output, "w", newline="", encoding="utf-8")
    except OSError as e:
        print(f"cannot open output file: {e}", file=sys.stderr)
        return 2

    errors = 0
    with out_f:
        writer = csv.DictWriter(out_f, fieldnames=out_fieldnames)
        writer.writeheader()

        for i, row in enumerate(rows, start=2):  # 2 = first data row (row 1 is header)
            sex = row[ns.sex_col].strip().lower()
            dob_str = row[ns.dob_col].strip()

            try:
                dob = datetime.strptime(dob_str, ISO_FORMAT).date()
                result = get_life_expectancy(sex, dob)
                dd = result.estimated_death_date
                row.update({
                    "current_age": f"{result.current_age:.2f}",
                    "additional_years": f"{result.additional_years:.2f}",
                    "total_years": f"{result.total_years:.2f}",
                    "estimated_death_date": f"{dd.year:04d}-{dd.month:02d}-{dd.day:02d}",
                    "error": "",
                })
            except (LongevityError, ValueError) as e:
                print(f"row {i}: {e}", file=sys.stderr)
                row.update({c: "" for c in OUTPUT_COLUMNS})
                row["error"] = str(e)
                errors += 1

            writer.writerow(row)

    if errors:
        print(f"completed with {errors} error(s). See 'error' column in output.", file=sys.stderr)
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
