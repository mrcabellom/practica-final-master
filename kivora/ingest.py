"""Load the raw sources into SQLite, as text, without cleaning anything."""

import csv
from pathlib import Path

SOURCES = {
    "orders": ["order_id", "customer_id", "created_at", "updated_at", "status",
               "currency", "total_amount"],
    "customers": ["customer_id", "name", "country", "signup_date"],
    "payments": ["payment_id", "order_id", "paid_at", "method", "status", "amount"],
}


def _create(conn, table, columns):
    conn.execute(f"DROP TABLE IF EXISTS {table}")
    conn.execute(f"CREATE TABLE {table} ({', '.join(c + ' TEXT' for c in columns)})")


def load_inbox(conn, inbox):
    """One raw_<source> table per source, with the day folder in `_day`."""
    for name, columns in SOURCES.items():
        _create(conn, f"raw_{name}", columns + ["_day"])
    days = sorted(p for p in Path(inbox).iterdir() if p.is_dir())
    for day in days:
        for name, columns in SOURCES.items():
            path = day / f"{name}.csv"
            if not path.exists():
                continue
            with open(path, encoding="utf-8", newline="") as fh:
                rows = [[row[c] for c in columns] + [day.name] for row in csv.DictReader(fh)]
            placeholders = ", ".join("?" for _ in range(len(columns) + 1))
            conn.executemany(f"INSERT INTO raw_{name} VALUES ({placeholders})", rows)
    conn.commit()
    return [d.name for d in days]


def load_reference(conn, reference):
    _create(conn, "ref_fx_rates", ["currency", "rate_to_eur"])
    with open(Path(reference) / "fx_rates.csv", encoding="utf-8", newline="") as fh:
        rows = [[row["currency"], row["rate_to_eur"]] for row in csv.DictReader(fh)]
    conn.executemany("INSERT INTO ref_fx_rates VALUES (?, ?)", rows)
    conn.commit()
