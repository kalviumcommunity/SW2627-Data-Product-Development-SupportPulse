
-- Optimized Query (Filter before JOIN)

SELECT
    t.customer_id,
    t.transaction_date,
    t.amount,
    c.name,
    c.plan_type,
    c.region
FROM transactions t
JOIN (
    SELECT
        customer_id,
        name,
        plan_type,
        region
    FROM customers
    WHERE plan_type = 'Premium'
) c
ON t.customer_id = c.customer_id;