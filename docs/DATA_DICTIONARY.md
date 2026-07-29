# Data Dictionary

This project contains normalized customer support and churn analytics datasets. Each dataset is designed for a production-style analytics pipeline.

## Raw datasets

### customers.csv
- `customer_id`: unique customer identifier
- `name`: customer name
- `email`: customer email address
- `phone`: contact phone number
- `signup_date`: customer onboarding date
- `plan_type`: subscription tier or support plan
- `region`: geographic region or market
- `tenure_days`: days since signup
- `monthly_spend`: recurring monthly spend amount
- `churn_status`: binary churn indicator (1 = churned, 0 = active)
- `churn_date`: date of churn event, if applicable

### tickets.csv
- `ticket_id`: unique ticket identifier
- `customer_id`: foreign key to customers.csv
- `created_date`: ticket creation date
- `ticket_category`: support issue category
- `priority`: ticket priority level
- `support_channel`: support channel used
- `escalated`: whether the ticket was escalated
- `resolved`: whether the ticket was resolved
- `resolution_time`: time to resolution in hours
- `csat_score`: customer satisfaction rating 1-5
- `within_30d_of_cancellation`: ticket occurred within 30 days before churn

### customer_revenue.csv
- `customer_id`: foreign key to customers.csv
- `monthly_revenue`: monthly revenue per customer
- `annual_revenue`: annualized revenue per customer

### customer_transactions.csv
- `customer_id`: foreign key to customers.csv
- `total_transactions`: total successful transactions
- `purchase_count`: number of purchases
- `total_spent`: total successful payment amount
- `days_since_last_purchase`: days since last successful transaction
- `average_order_value`: average amount per purchase
- `customer_lifetime_value`: derived lifetime value estimate

### transactions.csv
- `transaction_id`: unique transaction identifier
- `customer_id`: foreign key to customers.csv
- `transaction_date`: date of transaction
- `amount`: transaction amount
- `payment_status`: transaction payment status

### missing_data.csv
- a raw dataset containing realistic missing values for testing data imputation and validation

### quality_test.csv
- a raw dataset containing invalid values for data quality testing

### data_with_dupes.csv
- a raw dataset containing duplicate customer records for deduplication testing

### messy_text_data.csv
- a raw dataset containing inconsistent capitalization, spacing, and formatting for text cleaning exercises

### untyped_data.csv
- a raw dataset with numeric fields cast to text and inconsistent date formats for type validation testing

## Processed datasets

### cleaned_customers.csv
- cleaned and normalized customer records

### cleaned_tickets.csv
- cleaned and normalized ticket records

### validated_data.csv
- customer records with validation flags for email, phone, signup date, and spend

### typed_data.csv
- typed customer records with normalized data types

### deduplicated_data.csv
- deduplicated customer records after removing duplicate keys

### feature_engineered_data.csv
- customer-level feature set including ticket frequency, churn risk, engagement, and spend quartile

### datetime_features.csv
- ticket-level date and time features such as weekday and days since ticket creation

### revenue_analysis.csv
- revenue metrics aggregated by plan and region

### customer_summary.csv
- summary statistics by plan type

### ticket_summary.csv
- summary statistics by ticket category

### dashboard_metrics.csv
- high-level dashboard KPIs for the dataset

### churn_report.csv
- churn counts and rates by plan and region
