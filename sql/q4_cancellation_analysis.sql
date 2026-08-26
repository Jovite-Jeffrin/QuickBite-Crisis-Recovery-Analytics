WITH order_phases AS (

    SELECT
        order_id,
        customer_id,
        order_timestamp::DATE AS order_date,
        is_cancelled,

        CASE
            WHEN order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase

    FROM fact_orders

    WHERE order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'
),

overall_cancellation AS (

    SELECT
        phase,

        COUNT(*) AS total_orders,

        SUM(
            CASE
                WHEN is_cancelled = 'Y'
                THEN 1
                ELSE 0
            END
        ) AS cancelled_orders

    FROM order_phases

    GROUP BY phase
)

SELECT
    phase,
    total_orders,
    cancelled_orders,

    ROUND(
        100.0 * cancelled_orders
        / NULLIF(total_orders, 0),
        2
    ) AS cancellation_rate

FROM overall_cancellation

ORDER BY
    CASE
        WHEN phase = 'Pre-Crisis' THEN 1
        WHEN phase = 'Crisis' THEN 2
    END;