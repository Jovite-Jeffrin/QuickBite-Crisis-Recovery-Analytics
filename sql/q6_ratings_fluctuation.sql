WITH monthly_ratings AS (

    SELECT
        DATE_TRUNC(
            'month',
            review_timestamp
        )::DATE AS review_month,

        ROUND(
            AVG(rating),
            2
        ) AS avg_rating

    FROM fact_ratings

    WHERE review_timestamp::DATE
        BETWEEN '2025-01-01' AND '2025-09-30'

      AND rating IS NOT NULL

    GROUP BY
        DATE_TRUNC(
            'month',
            review_timestamp
        )::DATE
),

rating_trend AS (

    SELECT
        review_month,
        avg_rating,

        LAG(avg_rating) OVER (
            ORDER BY review_month
        ) AS previous_month_rating

    FROM monthly_ratings
)

SELECT
    review_month,
    avg_rating,
    previous_month_rating,

    ROUND(
        avg_rating - previous_month_rating,
        2
    ) AS rating_change

FROM rating_trend

ORDER BY
    review_month;