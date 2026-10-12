-- Sales per day and country.
-- Contract: docs/data-contracts/daily_sales.md

DROP TABLE IF EXISTS daily_sales;
CREATE TABLE daily_sales AS
SELECT
    o.order_date                  AS sales_date,
    c.country                     AS country,
    COUNT(*)                      AS orders_count,
    ROUND(SUM(o.total_amount), 2) AS gross_amount
FROM stg_orders o
JOIN stg_payments p
  ON p.order_id = o.order_id
 AND p.status = 'captured'
JOIN stg_customers c
  ON c.customer_id = o.customer_id
WHERE o.status <> 'cancelled'
GROUP BY o.order_date, c.country
ORDER BY sales_date, country;
