SELECT
    DATE_TRUNC('month', review_timestamp)::DATE AS review_month,
    ROUND(AVG(rating), 2) AS average_rating
FROM fact_ratings
WHERE rating IS NOT NULL
GROUP BY 1
ORDER BY 1;