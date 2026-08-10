# Finding 2: Multiple Escalations Are Associated With Higher Churn

## Finding

Customers experiencing multiple support escalations show higher churn rates in the current dataset.

## Supporting Evidence

Source:

`supporting_evidence/escalation_churn.csv`

The analysis produced:

| Escalations | Customers | Churn Rate |
|---:|---:|---:|
| 0 | 61 | 21.31% |
| 1 | 41 | 17.07% |
| 2 | 11 | 36.36% |
| 3 | 4 | 50.00% |
| 4 | 3 | 33.33% |

Customers with two escalations have a **36.36%** churn rate.

Customers with three escalations have a **50.00%** churn rate.

For comparison, customers with one escalation have a **17.07%** churn rate.

## Why This Evidence Matters

Repeated escalations can indicate that a customer's issue is difficult to resolve or that the customer has experienced multiple support problems.

The increase in churn among customers with two or more escalations makes escalation frequency a useful signal for identifying customers who may require intervention.

However, the groups with three and four escalations contain only four and three customers respectively. These small sample sizes mean the results should be treated as warning signals rather than definitive evidence.

## Business Implication

Customers with repeated escalations should be flagged for review and assigned clear ownership so unresolved problems do not continue accumulating.