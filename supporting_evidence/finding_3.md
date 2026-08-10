# Finding 3: Resolution Time Requires Further Investigation

## Finding

The current dataset does not show a simple, consistent relationship between resolution time and churn.

## Supporting Evidence

Source:

`supporting_evidence/resolution_time_churn.csv`

The analysis produced:

| Resolution Time | Customers | Churn Rate |
|---|---:|---:|
| <2 hours | 9 | 33.33% |
| 2–4 hours | 2 | 50.00% |
| 4–24 hours | 103 | 20.39% |
| >24 hours | 6 | 33.33% |

The largest group, customers with resolution times between 4 and 24 hours, has a **20.39%** churn rate.

The 2–4 hour group has a **50.00%** churn rate, but this group contains only **2 customers**.

The >24 hour group has a **33.33%** churn rate, but contains only **6 customers**.

## Why This Evidence Matters

The results demonstrate why small groups should not be interpreted without considering sample size.

Although some smaller groups show higher churn, the available data is insufficient to conclude that slower resolution directly causes churn.

More historical observations would make the relationship easier to evaluate.

## Business Implication

SupportPulse should continue tracking response and resolution times alongside customer churn. Future analysis should use a larger historical dataset before setting operational targets based solely on resolution time.