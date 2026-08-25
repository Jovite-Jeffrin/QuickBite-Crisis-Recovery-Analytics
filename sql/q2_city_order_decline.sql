WITH city_phase_orders AS (

    SELECT
        dc.city,

        CASE
            WHEN fo.order_timestamp::DATE
                 BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN fo.order_timestamp::DATE
                 BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase,

        COUNT(fo.order_id) AS total_orders

    FROM fact_orders fo

    INNER JOIN dim_customer dc
        ON fo.customer_id = dc.customer_id

    WHERE fo.order_timestamp::DATE
          BETWEEN '2025-01-01' AND '2025-09-30'

    GROUP BY
        dc.city,
        phase
),

city_comparison AS (

    SELECT
        city,

        MAX(
            CASE
                WHEN phase = 'Pre-Crisis'
                THEN total_orders
                ELSE 0
            END
        ) AS pre_crisis_orders,

        MAX(
            CASE
                WHEN phase = 'Crisis'
                THEN total_orders
                ELSE 0
            END
        ) AS crisis_orders

    FROM city_phase_orders

    GROUP BY city
)

SELECT
    city,

    pre_crisis_orders,
    crisis_orders,

    pre_crisis_orders - crisis_orders
        AS order_decline,

    ROUND(
        100.0 *
        (pre_crisis_orders - crisis_orders)
        / NULLIF(pre_crisis_orders, 0),
        2
    ) AS decline_percentage

FROM city_comparison

WHERE pre_crisis_orders > 0

ORDER BY decline_percentage DESC

LIMIT 5;