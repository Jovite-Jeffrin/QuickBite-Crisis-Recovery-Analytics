WITH delivery_phases AS (

    SELECT
        fo.order_id,
        fo.order_timestamp::DATE AS order_date,
        dp.actual_delivery_time_mins,
        dp.expected_delivery_time_mins,

        CASE
            WHEN fo.order_timestamp::DATE
                BETWEEN '2025-01-01' AND '2025-05-31'
                THEN 'Pre-Crisis'

            WHEN fo.order_timestamp::DATE
                BETWEEN '2025-06-01' AND '2025-09-30'
                THEN 'Crisis'
        END AS phase

    FROM fact_orders fo

    INNER JOIN fact_delivery_performance dp
        ON fo.order_id = dp.order_id

    WHERE fo.order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'

      AND fo.is_cancelled = 'N'

      AND dp.actual_delivery_time_mins IS NOT NULL

      AND dp.expected_delivery_time_mins IS NOT NULL
)

SELECT
    phase,

    COUNT(*) AS delivered_orders,

    ROUND(
        AVG(actual_delivery_time_mins),
        2
    ) AS avg_actual_delivery_mins,

    ROUND(
        AVG(expected_delivery_time_mins),
        2
    ) AS avg_expected_delivery_mins,

    ROUND(
        AVG(
            actual_delivery_time_mins
            - expected_delivery_time_mins
        ),
        2
    ) AS avg_delivery_variance_mins,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN actual_delivery_time_mins
                     <= expected_delivery_time_mins
                THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(*), 0),
        2
    ) AS sla_compliance_rate

FROM delivery_phases

GROUP BY
    phase

ORDER BY
    CASE
        WHEN phase = 'Pre-Crisis' THEN 1
        WHEN phase = 'Crisis' THEN 2
    END;