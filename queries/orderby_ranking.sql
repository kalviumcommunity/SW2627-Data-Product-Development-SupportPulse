SELECT

    c.customer_type,

    c.industry,

    COUNT(DISTINCT t.customer_id) AS customers,

    SUM(t.amount) AS total_revenue,

    ROUND(AVG(t.amount),2) AS avg_order,

    RANK() OVER(

        ORDER BY SUM(t.amount) DESC

    ) AS revenue_rank

FROM transactions t

JOIN customers c

ON t.customer_id=c.customer_id

WHERE t.transaction_date>='2026-01-01'

GROUP BY

    c.customer_type,

    c.industry

HAVING COUNT(DISTINCT t.customer_id)>=5

ORDER BY total_revenue DESC

LIMIT 20;