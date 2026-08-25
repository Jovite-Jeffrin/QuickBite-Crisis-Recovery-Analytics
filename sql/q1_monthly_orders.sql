SELECT
    DATE_TRUNC('month', order_timestamp)::DATE AS order_month,

    COUNT(order_id) AS total_orders,

    CASE
        WHEN order_timestamp::DATE
             BETWEEN '2025-01-01' AND '2025-05-31'
            THEN 'Pre-Crisis'

        WHEN order_timestamp::DATE
             BETWEEN '2025-06-01' AND '2025-09-30'
            THEN 'Crisis'

        ELSE 'Post-Crisis'
    END AS phase

FROM fact_orders

WHERE order_timestamp::DATE >= '2025-01-01'

GROUP BY 1, 3
ORDER BY 1;