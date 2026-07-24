SELECT

    c.customer_type,

    strftime('%Y-%m', t.transaction_date) AS month,

    COUNT(DISTINCT t.customer_id) AS unique_customers,

    COUNT(*) AS transaction_count,

    ROUND(SUM(t.amount),2) AS monthly_revenue,

    ROUND(AVG(t.amount),2) AS avg_transaction

FROM transactions t

JOIN customers c

ON t.customer_id = c.customer_id

WHERE t.transaction_date >= '2026-01-01'

GROUP BY

    c.customer_type,

    strftime('%Y-%m', t.transaction_date)

ORDER BY month DESC;