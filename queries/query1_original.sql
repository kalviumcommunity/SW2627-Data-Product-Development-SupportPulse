SELECT *
FROM transactions t
JOIN customers c
ON t.customer_id = c.customer_id;