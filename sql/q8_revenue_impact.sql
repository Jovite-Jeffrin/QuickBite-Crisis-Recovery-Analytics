WITH revenue_by_phase AS (

    SELECT
        CASE
            WHEN order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase,

        COUNT(*) AS completed_orders,

        SUM(subtotal_amount) AS subtotal_revenue,

        SUM(discount_amount) AS total_discount,

        SUM(delivery_fee) AS total_delivery_fee,

        SUM(total_amount) AS total_revenue,

        AVG(total_amount) AS average_order_value

    FROM fact_orders

    WHERE order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'

      AND is_cancelled = 'N'

    GROUP BY
        CASE
            WHEN order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END
)

SELECT
    phase,
    completed_orders,

    ROUND(subtotal_revenue, 2)
        AS subtotal_revenue,

    ROUND(total_discount, 2)
        AS total_discount,

    ROUND(total_delivery_fee, 2)
        AS total_delivery_fee,

    ROUND(total_revenue, 2)
        AS total_revenue,

    ROUND(average_order_value, 2)
        AS average_order_value

FROM revenue_by_phase

ORDER BY
    CASE
        WHEN phase = 'Pre-Crisis' THEN 1
        WHEN phase = 'Crisis' THEN 2
    END;