WITH customer_pre_crisis AS (

    SELECT
        customer_id,

        COUNT(*) AS pre_crisis_orders,

        SUM(total_amount) AS pre_crisis_spend

    FROM fact_orders

    WHERE order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-05-31'

      AND is_cancelled = 'N'

    GROUP BY
        customer_id
),

customer_ranked AS (

    SELECT
        customer_id,
        pre_crisis_orders,
        pre_crisis_spend,

        NTILE(20) OVER (
            ORDER BY pre_crisis_spend DESC
        ) AS spend_percentile

    FROM customer_pre_crisis
),

high_value_customers AS (

    SELECT
        customer_id,
        pre_crisis_orders,
        pre_crisis_spend

    FROM customer_ranked

    WHERE spend_percentile = 1
),

crisis_orders AS (

    SELECT
        customer_id,

        COUNT(*) AS crisis_orders,

        SUM(total_amount) AS crisis_spend

    FROM fact_orders

    WHERE order_timestamp::DATE
        BETWEEN '2025-06-01' AND '2025-09-30'

      AND is_cancelled = 'N'

    GROUP BY
        customer_id
),

customer_ratings AS (

    SELECT
        customer_id,

        AVG(
            CASE
                WHEN review_timestamp::DATE
                    BETWEEN '2025-01-01' AND '2025-05-31'
                THEN rating
            END
        ) AS pre_crisis_rating,

        AVG(
            CASE
                WHEN review_timestamp::DATE
                    BETWEEN '2025-06-01' AND '2025-09-30'
                THEN rating
            END
        ) AS crisis_rating

    FROM fact_ratings

    WHERE rating IS NOT NULL

    GROUP BY
        customer_id
),

customer_delivery AS (

    SELECT
        fo.customer_id,

        AVG(
            CASE
                WHEN fo.order_timestamp::DATE
                    BETWEEN '2025-01-01' AND '2025-05-31'
                THEN
                    fd.actual_delivery_time_mins
                    -
                    fd.expected_delivery_time_mins
            END
        ) AS pre_crisis_delivery_delay,

        AVG(
            CASE
                WHEN fo.order_timestamp::DATE
                    BETWEEN '2025-06-01' AND '2025-09-30'
                THEN
                    fd.actual_delivery_time_mins
                    -
                    fd.expected_delivery_time_mins
            END
        ) AS crisis_delivery_delay

    FROM fact_orders fo

    LEFT JOIN fact_delivery_performance fd
        ON fo.order_id = fd.order_id

    WHERE fo.is_cancelled = 'N'

    GROUP BY
        fo.customer_id
),

customer_preferences AS (

    SELECT
        fo.customer_id,

        MODE() WITHIN GROUP (
            ORDER BY dr.city
        ) AS city,

        MODE() WITHIN GROUP (
            ORDER BY dr.cuisine_type
        ) AS preferred_cuisine

    FROM fact_orders fo

    LEFT JOIN dim_restaurant dr
        ON fo.restaurant_id = dr.restaurant_id

    WHERE fo.order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-05-31'

      AND fo.is_cancelled = 'N'

    GROUP BY
        fo.customer_id
),

customer_metrics AS (

    SELECT

        h.customer_id,

        h.pre_crisis_orders,

        h.pre_crisis_spend,

        COALESCE(
            c.crisis_orders,
            0
        ) AS crisis_orders,

        COALESCE(
            c.crisis_spend,
            0
        ) AS crisis_spend,

        ROUND(
            100.0 *
            (
                COALESCE(c.crisis_orders, 0)
                -
                h.pre_crisis_orders
            )
            /
            NULLIF(
                h.pre_crisis_orders,
                0
            ),
            2
        ) AS order_frequency_change_pct,

        ROUND(
            r.pre_crisis_rating,
            2
        ) AS pre_crisis_rating,

        ROUND(
            r.crisis_rating,
            2
        ) AS crisis_rating,

        ROUND(
            r.crisis_rating
            -
            r.pre_crisis_rating,
            2
        ) AS rating_change,

        ROUND(
            d.pre_crisis_delivery_delay,
            2
        ) AS pre_crisis_delivery_delay,

        ROUND(
            d.crisis_delivery_delay,
            2
        ) AS crisis_delivery_delay,

        ROUND(
            d.crisis_delivery_delay
            -
            d.pre_crisis_delivery_delay,
            2
        ) AS delivery_delay_change,

        p.city,

        p.preferred_cuisine

    FROM high_value_customers h

    LEFT JOIN crisis_orders c
        ON h.customer_id = c.customer_id

    LEFT JOIN customer_ratings r
        ON h.customer_id = r.customer_id

    LEFT JOIN customer_delivery d
        ON h.customer_id = d.customer_id

    LEFT JOIN customer_preferences p
        ON h.customer_id = p.customer_id
)

SELECT
    *

FROM customer_metrics

ORDER BY
    order_frequency_change_pct ASC,
    rating_change ASC;