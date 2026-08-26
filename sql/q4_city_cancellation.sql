WITH city_cancellation AS (

    SELECT
        dr.city,

        COUNT(*) FILTER (
            WHERE fo.order_timestamp::DATE
            BETWEEN '2025-01-01' AND '2025-05-31'
        ) AS pre_crisis_orders,

        COUNT(*) FILTER (
            WHERE fo.order_timestamp::DATE
            BETWEEN '2025-06-01' AND '2025-09-30'
        ) AS crisis_orders,

        COUNT(*) FILTER (
            WHERE fo.order_timestamp::DATE
            BETWEEN '2025-01-01' AND '2025-05-31'
            AND fo.is_cancelled = 'Y'
        ) AS pre_crisis_cancelled,

        COUNT(*) FILTER (
            WHERE fo.order_timestamp::DATE
            BETWEEN '2025-06-01' AND '2025-09-30'
            AND fo.is_cancelled = 'Y'
        ) AS crisis_cancelled

    FROM fact_orders fo

    INNER JOIN dim_restaurant dr
        ON fo.restaurant_id = dr.restaurant_id

    WHERE fo.order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'

    GROUP BY
        dr.city
)

SELECT
    city,

    pre_crisis_orders,
    pre_crisis_cancelled,

    ROUND(
        100.0 * pre_crisis_cancelled
        / NULLIF(pre_crisis_orders, 0),
        2
    ) AS pre_crisis_cancellation_rate,

    crisis_orders,
    crisis_cancelled,

    ROUND(
        100.0 * crisis_cancelled
        / NULLIF(crisis_orders, 0),
        2
    ) AS crisis_cancellation_rate,

    ROUND(
        (
            100.0 * crisis_cancelled
            / NULLIF(crisis_orders, 0)
        )
        -
        (
            100.0 * pre_crisis_cancelled
            / NULLIF(pre_crisis_orders, 0)
        ),
        2
    ) AS cancellation_rate_change_pp

FROM city_cancellation

ORDER BY
    cancellation_rate_change_pp DESC;