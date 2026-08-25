SELECT
    DATE_TRUNC('month', order_timestamp)::DATE AS order_month,
    COUNT(order_id) AS total_orders
FROM fact_orders
GROUP BY 1
ORDER BY 1;