"""Tests of the daily sales pipeline."""

import csv
import re
from pathlib import Path

from kivora.pipeline import run

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "data" / "inbox"
REFERENCE = ROOT / "data" / "reference"
INITIAL_DAYS = ["2026-09-01", "2026-09-02", "2026-09-03"]


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def initial_inbox(tmp_path):
    """Copy of the first three days, so the tests do not depend on later deliveries."""
    inbox = tmp_path / "inbox"
    for day in INITIAL_DAYS:
        target = inbox / day
        target.mkdir(parents=True)
        for source in (INBOX / day).iterdir():
            (target / source.name).write_bytes(source.read_bytes())
    return inbox


def write_day(inbox, day, orders, payments, customers):
    folder = inbox / day
    folder.mkdir(parents=True)
    for name, rows in (("orders", orders), ("payments", payments), ("customers", customers)):
        with open(folder / f"{name}.csv", "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def test_pipeline_generates_daily_sales(tmp_path):
    run(initial_inbox(tmp_path), REFERENCE, tmp_path / "out")
    rows = read_csv(tmp_path / "out" / "daily_sales.csv")
    assert len(rows) > 0


def test_sales_dates_are_iso(tmp_path):
    run(initial_inbox(tmp_path), REFERENCE, tmp_path / "out")
    for row in read_csv(tmp_path / "out" / "daily_sales.csv"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["sales_date"])


def test_exact_duplicate_orders_counted_once(tmp_path):
    order = {"order_id": "K-1", "customer_id": "C1", "created_at": "2026-09-01T10:00:00Z",
             "updated_at": "2026-09-01T10:00:00Z", "status": "confirmed",
             "currency": "EUR", "total_amount": "10.00"}
    payment = {"payment_id": "P-1", "order_id": "K-1", "paid_at": "2026-09-01T10:01:00Z",
               "method": "card", "status": "captured", "amount": "10.00"}
    customer = {"customer_id": "C1", "name": "Ana", "country": "ES", "signup_date": "2025-01-01"}
    write_day(tmp_path / "inbox", "2026-09-01", [order, order], [payment], [customer])
    run(tmp_path / "inbox", REFERENCE, tmp_path / "out")
    rows = read_csv(tmp_path / "out" / "daily_sales.csv")
    assert rows[0]["orders_count"] == "1"


def test_gross_matches_source_total(tmp_path):
    """The total in daily_sales is the total of the paid orders in the source."""
    inbox = initial_inbox(tmp_path)
    run(inbox, REFERENCE, tmp_path / "out")
    paid = {p["order_id"] for day in INITIAL_DAYS
            for p in read_csv(inbox / day / "payments.csv") if p["status"] == "captured"}
    orders = {tuple(o.values()) for day in INITIAL_DAYS for o in read_csv(inbox / day / "orders.csv")}
    expected = sum(float(o[6]) for o in orders if o[0] in paid and o[4] != "cancelled")
    total = sum(float(r["gross_amount"]) for r in read_csv(tmp_path / "out" / "daily_sales.csv"))
    assert round(total, 2) == round(expected, 2)
