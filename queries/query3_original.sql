
-- Original Nested Query

SELECT
    customer_id,
    total_spent
FROM
(
    SELECT
        customer_id,
        SUM(amount) AS total_spent
    FROM transactions
    GROUP BY customer_id
) t
WHERE total_spent > 5000;