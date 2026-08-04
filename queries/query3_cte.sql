
-- Optimized Query using CTE

WITH customer_summary AS
(
    SELECT
        customer_id,
        SUM(amount) AS total_spent
    FROM transactions
    GROUP BY customer_id
)

SELECT
    customer_id,
    total_spent
FROM customer_summary
WHERE total_spent > 5000;