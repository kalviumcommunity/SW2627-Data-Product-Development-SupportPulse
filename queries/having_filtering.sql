SELECT

    customer_id,

    COUNT(*) AS transaction_count,

    SUM(amount) AS annual_revenue

FROM transactions

WHERE transaction_date >= '2026-01-01'

GROUP BY customer_id

HAVING

    SUM(amount) > 10000

AND COUNT(*) >= 5

ORDER BY annual_revenue DESC;