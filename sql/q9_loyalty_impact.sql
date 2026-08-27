WITH pre_crisis_customers AS (

    SELECT
        customer_id,
        COUNT(*) AS pre_crisis_orders

    FROM fact_orders

    WHERE order_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-05-31'

      AND is_cancelled = 'N'

    GROUP BY
        customer_id

    HAVING COUNT(*) >= 5
),

crisis_customers AS (

    SELECT DISTINCT
        customer_id

    FROM fact_orders

    WHERE order_timestamp::DATE
        BETWEEN '2025-06-01' AND '2025-09-30'

      AND is_cancelled = 'N'
),

stopped_customers AS (

    SELECT
        p.customer_id,
        p.pre_crisis_orders

    FROM pre_crisis_customers p

    LEFT JOIN crisis_customers c
        ON p.customer_id = c.customer_id

    WHERE c.customer_id IS NULL
),

customer_ratings AS (

    SELECT
        customer_id,
        ROUND(
            AVG(rating),
            2
        ) AS avg_rating

    FROM fact_ratings

    WHERE rating IS NOT NULL

    GROUP BY
        customer_id
)

SELECT

    COUNT(*) AS loyal_pre_crisis_customers,

    COUNT(
        CASE
            WHEN s.customer_id IS NOT NULL
            THEN 1
        END
    ) AS stopped_customers,

    ROUND(
        100.0 *
        COUNT(
            CASE
                WHEN s.customer_id IS NOT NULL
                THEN 1
            END
        )
        /
        NULLIF(COUNT(*), 0),
        2
    ) AS stopped_customer_percentage,

    COUNT(
        CASE
            WHEN s.customer_id IS NOT NULL
             AND r.avg_rating > 4.5
            THEN 1
        END
    ) AS stopped_high_rating_customers,

    ROUND(
        100.0 *
        COUNT(
            CASE
                WHEN s.customer_id IS NOT NULL
                 AND r.avg_rating > 4.5
                THEN 1
            END
        )
        /
        NULLIF(
            COUNT(
                CASE
                    WHEN s.customer_id IS NOT NULL
                    THEN 1
                END
            ),
            0
        ),
        2
    ) AS high_rating_percentage

FROM pre_crisis_customers p

LEFT JOIN stopped_customers s
    ON p.customer_id = s.customer_id

LEFT JOIN customer_ratings r
    ON p.customer_id = r.customer_id;