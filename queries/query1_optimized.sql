SELECT
    t.customer_id,
    t.transaction_date,
    t.amount,
    c.name,
    c.plan_type,
    c.region,
    c.monthly_spend
FROM transactions t
JOIN customers c
ON t.customer_id = c.customer_id;