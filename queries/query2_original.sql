-- Original Query (Filter after JOIN)

SELECT
    t.customer_id,
    t.transaction_date,
    t.amount,
    c.name,
    c.plan_type,
    c.region
FROM transactions t
JOIN customers c
ON t.customer_id = c.customer_id
WHERE c.plan_type = 'Premium';