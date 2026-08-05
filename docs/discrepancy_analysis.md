# SQL-Based Insight Validation - Discrepancy Analysis

## Objective

The purpose of this validation process is to ensure that business metrics calculated using SQL match those calculated using the Python analytics pipeline.

---

## Metrics Validated

1. Active Customers
2. Average Order Value
3. Total Revenue

---

## Validation Results

| Metric | SQL | Python | Status |
|--------|-----|--------|--------|
| Active Customers | Match | Match | PASS |
| Average Order Value | Different | Different | FAIL |
| Total Revenue | Different | Different | PASS |

---

## Cause of Discrepancies

### Average Order Value

A small discrepancy was intentionally introduced into the Python calculation by increasing the value by 2%.

Purpose:
To simulate computation drift between two independent analytics systems.

---

### Total Revenue

A fixed value was added to the Python calculation to simulate incorrect aggregation.

Purpose:
To demonstrate how validation detects mismatched business metrics.

---

## Investigation

Possible causes of mismatched metrics include:

- Different filtering logic
- Missing records
- Duplicate records
- Different aggregation methods
- Data synchronization delay
- Manual calculation errors

---

## Resolution

- Compare SQL and Python calculations.
- Validate source datasets.
- Review aggregation logic.
- Ensure both systems use identical business rules.

---

## Conclusion

Automated validation helps identify inconsistencies early and improves confidence in dashboard metrics and business reporting.