WITH order_metrics AS (

    SELECT

        CASE
            WHEN order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase,

        COUNT(*) AS total_orders,

        COUNT(
            CASE
                WHEN is_cancelled = 'Y'
                THEN 1
            END
        ) AS cancelled_orders,

        SUM(
            CASE
                WHEN is_cancelled = 'N'
                THEN total_amount
                ELSE 0
            END
        ) AS revenue

    FROM fact_orders

    WHERE order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'

    GROUP BY
        CASE
            WHEN order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END
),

rating_metrics AS (

    SELECT

        CASE
            WHEN review_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN review_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase,

        AVG(rating) AS avg_rating

    FROM fact_ratings

    WHERE review_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'

      AND rating IS NOT NULL

    GROUP BY
        CASE
            WHEN review_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN review_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END
),

delivery_metrics AS (

    SELECT

        CASE
            WHEN fo.order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN fo.order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase,

        AVG(
            fd.actual_delivery_time_mins
        ) AS avg_delivery_time,

        AVG(
            fd.actual_delivery_time_mins
            -
            fd.expected_delivery_time_mins
        ) AS avg_delivery_variance

    FROM fact_orders fo

    INNER JOIN fact_delivery_performance fd
        ON fo.order_id = fd.order_id

    WHERE fo.order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'

      AND fo.is_cancelled = 'N'

    GROUP BY
        CASE
            WHEN fo.order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN fo.order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END
)

SELECT

    o.phase,

    o.total_orders,

    o.cancelled_orders,

    ROUND(
        100.0 *
        o.cancelled_orders
        /
        NULLIF(o.total_orders, 0),
        2
    ) AS cancellation_rate,

    ROUND(
        o.revenue,
        2
    ) AS revenue,

    ROUND(
        r.avg_rating,
        2
    ) AS avg_rating,

    ROUND(
        d.avg_delivery_time,
        2
    ) AS avg_delivery_time,

    ROUND(
        d.avg_delivery_variance,
        2
    ) AS avg_delivery_variance

FROM order_metrics o

LEFT JOIN rating_metrics r
    ON o.phase = r.phase

LEFT JOIN delivery_metrics d
    ON o.phase = d.phase

ORDER BY
    CASE
        WHEN o.phase = 'Pre-Crisis' THEN 1
        WHEN o.phase = 'Crisis' THEN 2
    END;