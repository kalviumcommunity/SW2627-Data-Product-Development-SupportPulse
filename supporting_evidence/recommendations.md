# Actionable Recommendations

## Recommendation 1 — Proactive Follow-Up for Low-CSAT Customers

### What
Create a retention alert for customers whose average CSAT score falls into the Low CSAT category.

### Why
The current analysis shows a **36.36% churn rate** among customers in the Low CSAT group, compared with **21.05%** among customers in the Excellent CSAT group.

This makes low satisfaction a useful warning signal for potential churn.

### Expected Impact
Earlier intervention can give the support or customer-success team an opportunity to understand the customer's problem, resolve outstanding issues, and improve the customer experience before cancellation occurs.

### Owner
**Support Manager / Customer Success Team**

### Timeline
Implement the monitoring rule within **2 weeks**.

### Success Measure
Track the churn rate of customers receiving proactive follow-up and compare it with the baseline Low-CSAT churn rate of **36.36%**.

---

## Recommendation 2 — Escalation-Based Customer Risk Alerts

### What
Automatically flag customers who have **two or more support escalations** for review by the support manager.

### Why
The analysis shows that customers with two escalations have a **36.36% churn rate**, while customers with three escalations have a **50.00% churn rate**.

Although the higher escalation groups are relatively small, repeated escalations are still a useful warning signal.

### Expected Impact
Identifying repeated escalations early can help the support team assign ownership, resolve recurring problems, and prevent unresolved complaints from becoming cancellation risks.

### Owner
**Support Manager / Support Operations Team**

### Timeline
Implement the escalation alert within **2 weeks**.

### Success Measure
Track the number of customers with repeated escalations and compare their subsequent churn rate with the current baseline.

---

## Recommendation 3 — Improve Historical Support-Time Tracking

### What
Maintain historical response and resolution-time data and analyze it alongside customer churn over a longer period.

### Why
The current resolution-time analysis does not show a simple relationship with churn.

For example:

- Less than 2 hours: **33.33% churn**
- 2–4 hours: **50.00% churn**
- 4–24 hours: **20.39% churn**
- More than 24 hours: **33.33% churn**

However, some groups are very small. The 2–4 hour group contains only **2 customers**, while the >24 hour group contains only **6 customers**.

Therefore, the current evidence is not strong enough to conclude that resolution time directly causes churn.

### Expected Impact
A larger historical dataset will allow SupportPulse to determine whether response and resolution times are reliable churn-risk indicators and help establish better operational targets.

### Owner
**Analytics Engineer / Support Operations Team**

### Timeline
Begin historical tracking immediately and review the relationship after **30–90 days** of additional data.

### Success Measure
Produce a monthly analysis comparing resolution-time groups with churn rates using a larger sample of customers.

---

# Priority Order

| Priority | Recommendation | Reason |
|---|---|---|
| 1 | Low-CSAT follow-up | Highest actionable customer-experience signal |
| 2 | Escalation alerts | Identifies repeated support problems |
| 3 | Historical resolution tracking | Improves future decision-making |

## Overall Business Goal

Use customer satisfaction and repeated escalations as immediate churn-warning signals while collecting better historical support data to improve future churn analysis.