SELECT

    c.customer_type,

    COUNT(DISTINCT t.customer_id) AS segment_customers,

    SUM(t.amount) AS segment_revenue,

    ROUND(AVG(t.amount),2) AS avg_order_value

FROM transactions t

JOIN customers c

ON t.customer_id=c.customer_id

WHERE

    t.transaction_date >= '2026-01-01'

AND t.transaction_status='completed'

AND t.amount>0

GROUP BY c.customer_type

HAVING

    COUNT(DISTINCT t.customer_id)>=10

AND SUM(t.amount)>100000

ORDER BY segment_revenue DESC;