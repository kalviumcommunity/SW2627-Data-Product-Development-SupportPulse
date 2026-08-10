# SupportPulse — Technical Analysis

## 1. Objective

The objective of this analysis is to identify measurable customer-support signals associated with customer churn and provide evidence that can support retention decisions.

The analysis focuses on:

- Customer churn
- Customer satisfaction
- Support escalations
- Resolution time
- Transaction revenue

---

## 2. Data Sources

The analysis uses three primary datasets.

### Customers

Source:

`data/raw/customers.csv`

Important fields:

- `customer_id`
- `churn_status`
- `plan_type`
- `region`
- `monthly_spend`
- `signup_date`

### Support Tickets

Source:

`data/raw/tickets.csv`

Important fields:

- `ticket_id`
- `customer_id`
- `resolution_time`
- `csat_score`
- `escalated`

### Transactions

Source:

`data/raw/transactions.csv`

Important fields:

- `customer_id`
- `transaction_date`
- `amount`

---

## 3. Overall Customer Metrics

The dataset contains:

- **120 customers**
- **27 churned customers**
- **22.50% overall churn rate**

The churn rate was calculated as:

```text
Churn Rate =
Churned Customers / Total Customers × 100