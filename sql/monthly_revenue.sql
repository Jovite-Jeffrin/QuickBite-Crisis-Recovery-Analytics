SELECT
    DATE_TRUNC('month', order_timestamp)::DATE AS order_month,
    ROUND(
        SUM(
            CASE
                WHEN is_cancelled = 'N'
                THEN total_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue
FROM fact_orders
GROUP BY 1
ORDER BY 1;