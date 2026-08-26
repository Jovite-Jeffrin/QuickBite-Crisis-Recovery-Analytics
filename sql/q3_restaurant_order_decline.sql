WITH restaurant_orders AS (

    SELECT
        dr.restaurant_name,

        COUNT(*) FILTER (
            WHERE fo.order_timestamp::DATE
            BETWEEN '2025-01-01' AND '2025-05-31'
        ) AS pre_crisis_orders,

        COUNT(*) FILTER (
            WHERE fo.order_timestamp::DATE
            BETWEEN '2025-06-01' AND '2025-09-30'
        ) AS crisis_orders

    FROM fact_orders fo

    INNER JOIN dim_restaurant dr
        ON fo.restaurant_id = dr.restaurant_id

    WHERE fo.order_timestamp::DATE
          BETWEEN '2025-01-01' AND '2025-09-30'

    GROUP BY
        dr.restaurant_name
)

SELECT
    restaurant_name,
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

FROM restaurant_orders

WHERE pre_crisis_orders >= 50

ORDER BY
    decline_percentage DESC,
    pre_crisis_orders DESC

LIMIT 10;