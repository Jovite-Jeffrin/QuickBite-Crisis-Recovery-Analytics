WITH phase_orders AS (
    SELECT
        CASE
            WHEN order_timestamp::DATE
                 BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN order_timestamp::DATE
                 BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase,

        COUNT(order_id) AS total_orders

    FROM fact_orders

    WHERE order_timestamp::DATE
          BETWEEN '2025-01-01' AND '2025-09-30'

    GROUP BY 1
),

comparison AS (
    SELECT
        MAX(
            CASE
                WHEN phase = 'Pre-Crisis'
                THEN total_orders
            END
        ) AS pre_crisis_orders,

        MAX(
            CASE
                WHEN phase = 'Crisis'
                THEN total_orders
            END
        ) AS crisis_orders

    FROM phase_orders
)

SELECT
    pre_crisis_orders,
    crisis_orders,

    pre_crisis_orders - crisis_orders
        AS order_decline,

    ROUND(
        100.0 *
        (pre_crisis_orders - crisis_orders)
        / NULLIF(pre_crisis_orders, 0),
        2
    ) AS order_decline_percentage,

    ROUND(
        pre_crisis_orders / 5.0,
        2
    ) AS avg_monthly_pre_crisis_orders,

    ROUND(
        crisis_orders / 4.0,
        2
    ) AS avg_monthly_crisis_orders,

    ROUND(
        100.0 *
        (
            (pre_crisis_orders / 5.0)
            -
            (crisis_orders / 4.0)
        )
        / NULLIF(pre_crisis_orders / 5.0, 0),
        2
    ) AS monthly_order_decline_percentage

FROM comparison;