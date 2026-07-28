SELECT

    c.customer_id,

    o.order_id,

    o.order_amount

FROM customers c

LEFT JOIN orders o

ON c.customer_id=o.customer_id

UNION

SELECT

    c.customer_id,

    o.order_id,

    o.order_amount

FROM orders o

LEFT JOIN customers c

ON o.customer_id=c.customer_id;