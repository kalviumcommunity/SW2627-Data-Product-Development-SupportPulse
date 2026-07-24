SELECT

    customer_id,

    SUM(amount) AS annual_revenue,

    COUNT(*) AS transaction_count

FROM transactions

WHERE transaction_date >= '2026-01-01'

AND amount > 0

AND transaction_status = 'completed'

GROUP BY customer_id

ORDER BY annual_revenue DESC;