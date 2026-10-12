-- The 10 customers who bought the most over the whole period.

DROP TABLE IF EXISTS top_customers;
CREATE TABLE top_customers AS
SELECT
    o.customer_id,
    COUNT(*)                      AS orders_count,
    ROUND(SUM(o.total_amount), 2) AS gross_amount
FROM stg_orders o
JOIN stg_payments p
  ON p.order_id = o.order_id
 AND p.status = 'captured'
WHERE o.status <> 'cancelled'
GROUP BY o.customer_id
ORDER BY gross_amount DESC, o.customer_id
LIMIT 10;
