# View Documentation

## View 1

### vw_active_customers

Purpose

Provides customer transaction statistics for dashboards.

Source Tables

- customers
- transactions

Columns

- customer_id
- name
- plan_type
- region
- transaction_count
- total_spent
- last_transaction_date

Used By

- Dashboard
- Customer Analytics
- Customer Timeline

---

## View 2

### vw_revenue_by_region

Purpose

Provides revenue analysis grouped by customer region.

Source Tables

- customers
- transactions

Columns

- region
- total_customers
- total_revenue
- average_transaction

Used By

- Revenue Dashboard
- Business Reports

---

## Aggregation

### agg_daily_metrics

Purpose

Stores daily business metrics.

Columns

- aggregation_date
- total_transactions
- total_revenue
- average_transaction
- updated_at

Refresh Schedule

Daily

Used By

- KPI Dashboard
- Executive Reports
- Trend Analysis