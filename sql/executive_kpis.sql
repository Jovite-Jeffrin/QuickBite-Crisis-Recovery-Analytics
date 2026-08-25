SELECT
    COUNT(DISTINCT fo.order_id) AS total_orders,

    ROUND(
        SUM(
            CASE
                WHEN fo.is_cancelled = 'N'
                THEN fo.total_amount
                ELSE 0
            END
        ),
        2
    ) AS total_revenue,

    COUNT(
        DISTINCT CASE
            WHEN fo.is_cancelled = 'N'
            THEN fo.customer_id
        END
    ) AS total_customers,

    ROUND(
        AVG(fr.rating),
        2
    ) AS average_rating,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN fo.is_cancelled = 'Y'
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(fo.order_id), 0),
        2
    ) AS cancellation_rate,

    ROUND(
        AVG(
            fdp.actual_delivery_time_mins
        ),
        2
    ) AS average_delivery_time

FROM fact_orders fo

LEFT JOIN fact_ratings fr
    ON fo.order_id = fr.order_id

LEFT JOIN fact_delivery_performance fdp
    ON fo.order_id = fdp.order_id;