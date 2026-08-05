-- =====================================================
-- View: vw_active_customers
-- Purpose:
-- Shows active customers with transaction statistics.
-- Used By:
-- Dashboard, Customer Analytics
-- =====================================================

CREATE VIEW vw_active_customers AS

SELECT

    c.customer_id,
    c.name,
    c.plan_type,
    c.region,

    COUNT(t.customer_id) AS transaction_count,

    SUM(t.amount) AS total_spent,

    MAX(t.transaction_date) AS last_transaction_date

FROM customers c

LEFT JOIN transactions t

ON c.customer_id = t.customer_id

GROUP BY

    c.customer_id,
    c.name,
    c.plan_type,
    c.region;