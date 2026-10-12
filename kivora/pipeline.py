"""Run the whole pipeline: raw load, SQL transformations and CSV export."""

import csv
import sqlite3
from pathlib import Path

from kivora import ingest

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"

# Executed in this order. Each script creates the tables named after it.
SCRIPTS = ["staging.sql", "daily_sales.sql", "top_customers.sql"]
EXPORTS = ["daily_sales", "top_customers"]


def export_table(conn, table, path):
    cursor = conn.execute(f"SELECT * FROM {table}")
    header = [column[0] for column in cursor.description]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(cursor.fetchall())


def run(inbox, reference, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    database = out / "warehouse.db"
    if database.exists():
        database.unlink()
    conn = sqlite3.connect(database)
    try:
        days = ingest.load_inbox(conn, inbox)
        ingest.load_reference(conn, reference)
        for script in SCRIPTS:
            conn.executescript((SQL_DIR / script).read_text(encoding="utf-8"))
        for table in EXPORTS:
            export_table(conn, table, out / f"{table}.csv")
        orders = conn.execute("SELECT COUNT(*) FROM stg_orders").fetchone()[0]
    finally:
        conn.close()
    print(f"Días procesados: {len(days)} ({days[0]} .. {days[-1]})" if days else "Sin días.")
    print(f"Pedidos en staging: {orders}")
    print(f"Salida en {out}/: " + ", ".join(f"{t}.csv" for t in EXPORTS))
