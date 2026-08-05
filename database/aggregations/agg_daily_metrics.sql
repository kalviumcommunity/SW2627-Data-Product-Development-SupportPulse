-- =====================================================
-- Table: agg_daily_metrics
-- Purpose:
-- Daily revenue aggregation.
-- Refresh:
-- Daily
-- =====================================================

CREATE TABLE agg_daily_metrics (

    aggregation_date DATE,

    total_transactions INT,

    total_revenue DECIMAL(12,2),

    average_transaction DECIMAL(12,2),

    updated_at TIMESTAMP

);

INSERT INTO agg_daily_metrics

SELECT

    DATE(transaction_date) AS aggregation_date,

    COUNT(*) AS total_transactions,

    SUM(amount) AS total_revenue,

    AVG(amount) AS average_transaction,

    CURRENT_TIMESTAMP

FROM transactions

GROUP BY

    DATE(transaction_date);