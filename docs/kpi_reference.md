# KPI Reference

## Total Customers
- Definition: Distinct customers in the dataset.
- Formula: COUNT(DISTINCT customer_id)

## Active Customers
- Definition: Customers with no churn event.
- Formula: COUNT(customer_id) WHERE churn_status = 0

## Churn Rate
- Definition: Percent of customers who cancelled.
- Formula: SUM(churn_status) / COUNT(customer_id)

## Average Resolution Time
- Definition: Average hours to resolve support tickets.
- Formula: AVG(resolution_time) WHERE resolved = TRUE

## Average CSAT
- Definition: Average customer satisfaction score.
- Formula: AVG(csat_score)

## Escalation Rate
- Definition: Percent of tickets escalated.
- Formula: SUM(escalated) / COUNT(ticket_id)

## Revenue Per Customer
- Definition: Average monthly revenue per customer.
- Formula: AVG(monthly_revenue)

## Customer Lifetime Value
- Definition: Estimated lifetime value per customer using aggregated spend.
- Formula: SUM(total_spent * 1.5) / COUNT(customer_id)

## Ticket Resolution Rate
- Definition: Percent of tickets resolved.
- Formula: SUM(resolved) / COUNT(ticket_id)

## Unresolved Ticket Rate
- Definition: Percent of tickets not resolved.
- Formula: SUM(NOT resolved) / COUNT(ticket_id)

## Monthly Revenue
- Definition: Total monthly revenue across all customers.
- Formula: SUM(monthly_revenue)

## Revenue Lost to Churn
- Definition: Monthly revenue from churned customers.
- Formula: SUM(monthly_revenue) WHERE churn_status = 1
