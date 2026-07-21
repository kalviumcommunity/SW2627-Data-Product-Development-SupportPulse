# Columns

## customer_id

- Type: Integer
- Business Meaning: Unique customer identifier
- Example: 1001
- Related KPI: Customer Count
- Null Handling: Never Null

---

## ticket_category

- Type: String
- Business Meaning: Type of customer complaint
- Example: Billing
- Related KPI: Complaint Distribution

---

## resolution_time

- Type: Float
- Business Meaning: Time taken to resolve the ticket
- Example: 5.5
- Related KPI: Average Resolution Time

---

## churn

- Type: Integer
- Business Meaning: Indicates whether the customer churned
- Example: 1
- Related KPI: Churn Rate
- Valid Values:
  - 0 = No
  - 1 = Yes

  # Column to KPI Mapping

## Churn Rate

Formula:
SUM(churn) / Total Customers

Related Columns:
- churn
- customer_id

Business Importance:
Measures customer retention.

---

## Average Resolution Time

Formula:
AVG(resolution_time)

Related Columns:
- resolution_time

Business Importance:
Measures support efficiency.

---

## Ticket Volume

Formula:
COUNT(ticket_id)

Related Columns:
- ticket_id

Business Importance:
Tracks support workload.

---

## Complaint Distribution

Related Columns:
- ticket_category

Business Importance:
Identifies the most common complaint categories.

---

## Customer Satisfaction

Related Columns:
- satisfaction_score

Business Importance:
Measures customer experience.

# Ambiguous Columns

## churn

Original Ambiguity:
Current churn or future churn?

Resolved Meaning:
Customer cancelled the service.

Suggested Rename:
has_churned

---

## priority

Original Ambiguity:
Business priority or ticket urgency?

Resolved Meaning:
Support ticket urgency.

Suggested Rename:
ticket_priority

# Column Relationships

## Resolution Time by Ticket Category

Related Columns:
- resolution_time
- ticket_category

Business Impact:
Shows which complaint categories take longer to resolve.

---

## Churn by Ticket Priority

Related Columns:
- priority
- churn

Business Impact:
Determines whether unresolved high-priority tickets increase churn.

