"""Basic checks on output/ (python tasks.py check)."""

import csv
import sys
from pathlib import Path

OUTPUT = Path("output")
EXPECTED = {
    "daily_sales.csv": ["sales_date", "country", "orders_count", "gross_amount"],
    "top_customers.csv": ["customer_id", "orders_count", "gross_amount"],
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    problems = []
    for name, columns in EXPECTED.items():
        path = OUTPUT / name
        if not path.exists():
            problems.append(f"falta {path}: ejecuta antes python tasks.py run")
            continue
        with open(path, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            missing = [c for c in columns if c not in (reader.fieldnames or [])]
            if missing:
                problems.append(f"{name}: faltan columnas {missing}")
                continue
            for line, row in enumerate(reader, start=2):
                if float(row["gross_amount"]) < 0:
                    problems.append(f"{name}:{line}: gross_amount negativo")
    for problem in problems:
        print(f"FAIL  {problem}")
    if problems:
        return 1
    print("OK: output/ tiene los ficheros y columnas esperados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
