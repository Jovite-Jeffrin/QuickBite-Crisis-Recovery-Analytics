WITH crisis_reviews AS (

    SELECT
        review_text,
        sentiment_score

    FROM fact_ratings

    WHERE review_timestamp::DATE
        BETWEEN '2025-06-01' AND '2025-09-30'

      AND review_text IS NOT NULL

      AND sentiment_score < 0
),

keyword_counts AS (

    SELECT
        keyword,
        COUNT(*) AS frequency

    FROM crisis_reviews

    CROSS JOIN LATERAL (
        VALUES
            ('taste', CASE
                WHEN LOWER(review_text) LIKE '%taste%' THEN 1
                ELSE 0
            END),

            ('quality', CASE
                WHEN LOWER(review_text) LIKE '%quality%' THEN 1
                ELSE 0
            END),

            ('food', CASE
                WHEN LOWER(review_text) LIKE '%food%' THEN 1
                ELSE 0
            END),

            ('hygiene', CASE
                WHEN LOWER(review_text) LIKE '%hygiene%' THEN 1
                ELSE 0
            END),

            ('safety', CASE
                WHEN LOWER(review_text) LIKE '%safety%' THEN 1
                ELSE 0
            END),

            ('service', CASE
                WHEN LOWER(review_text) LIKE '%service%' THEN 1
                ELSE 0
            END),

            ('late', CASE
                WHEN LOWER(review_text) LIKE '%late%' THEN 1
                ELSE 0
            END),

            ('delivery', CASE
                WHEN LOWER(review_text) LIKE '%delivery%' THEN 1
                ELSE 0
            END),

            ('cold', CASE
                WHEN LOWER(review_text) LIKE '%cold%' THEN 1
                ELSE 0
            END),

            ('stale', CASE
                WHEN LOWER(review_text) LIKE '%stale%' THEN 1
                ELSE 0
            END),

            ('packaging', CASE
                WHEN LOWER(review_text) LIKE '%packaging%' THEN 1
                ELSE 0
            END),

            ('price', CASE
                WHEN LOWER(review_text) LIKE '%price%' THEN 1
                ELSE 0
            END),

            ('portion', CASE
                WHEN LOWER(review_text) LIKE '%portion%' THEN 1
                ELSE 0
            END),

            ('worst', CASE
                WHEN LOWER(review_text) LIKE '%worst%' THEN 1
                ELSE 0
            END),

            ('never', CASE
                WHEN LOWER(review_text) LIKE '%never%' THEN 1
                ELSE 0
            END),

            ('terrible', CASE
                WHEN LOWER(review_text) LIKE '%terrible%' THEN 1
                ELSE 0
            END),

            ('horrible', CASE
                WHEN LOWER(review_text) LIKE '%horrible%' THEN 1
                ELSE 0
            END),

            ('bad', CASE
                WHEN LOWER(review_text) LIKE '%bad%' THEN 1
                ELSE 0
            END)

    ) AS keywords(keyword, matched)

    WHERE matched = 1

    GROUP BY
        keyword
)

SELECT
    keyword,
    frequency

FROM keyword_counts

ORDER BY
    frequency DESC;