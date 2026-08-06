# KPI Sources Documentation

## Revenue
- Source: data/raw/transactions.csv
- Calculation: Sum of the amount column
- Business Meaning: Total revenue generated from customer transactions.

---

## Active Customers
- Source: data/raw/transactions.csv
- Calculation: Count of unique customer_id values.
- Business Meaning: Number of customers making transactions.

---

## Average Order Value
- Source: data/raw/transactions.csv
- Calculation: Average of the amount column.
- Business Meaning: Average revenue generated per transaction.

---

## Churn Rate
- Source: data/processed/feature_engineered_customers.csv
- Calculation: Average of churn_status × 100.
- Business Meaning: Percentage of customers who have churned.

---

## Customer Satisfaction
- Source: data/processed/feature_engineered_tickets.csv
- Calculation: Average of csat_score.
- Business Meaning: Average customer satisfaction score.

---

## Dashboard Design

The dashboard follows a hierarchical KPI layout.

1. KPI cards at the top.
2. Trend charts in the middle.
3. Detailed tables below.
4. Filters allow drill-down into customer-level information.