-- Staging: types and duplicates.
-- Reads the raw_* tables loaded by kivora/ingest.py.

DROP TABLE IF EXISTS stg_orders;
CREATE TABLE stg_orders AS
SELECT DISTINCT
    order_id,
    customer_id,
    created_at,
    updated_at,
    status,
    currency,
    CAST(total_amount AS REAL) AS total_amount,
    substr(created_at, 1, 10)   AS order_date
FROM raw_orders;

DROP TABLE IF EXISTS stg_customers;
CREATE TABLE stg_customers AS
SELECT DISTINCT
    customer_id,
    name,
    country,
    signup_date
FROM raw_customers;

DROP TABLE IF EXISTS stg_payments;
CREATE TABLE stg_payments AS
SELECT
    payment_id,
    order_id,
    paid_at,
    method,
    status,
    CAST(amount AS REAL) AS amount
FROM raw_payments;
