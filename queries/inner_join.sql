SELECT

    c.customer_id,

    c.customer_type,

    o.order_id,

    o.order_amount

FROM customers c

INNER JOIN orders o

ON c.customer_id=o.customer_id;