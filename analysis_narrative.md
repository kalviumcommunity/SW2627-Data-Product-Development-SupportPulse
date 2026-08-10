# Customer Churn Analysis: Executive Summary

## 1. Context — The Business Problem

Customer churn is a significant business concern for SupportPulse because customers who leave reduce recurring revenue and increase the need to acquire replacement customers. The purpose of this analysis is to understand whether customer support experiences provide useful signals for identifying churn risk. In particular, we examined support resolution time, customer satisfaction, escalations, customer churn status, and transaction revenue to identify patterns that can help the business prioritize retention efforts.

The overall dataset contains 120 customers, of which 27 are classified as churned. This represents an overall churn rate of 22.50%.

## 2. Data — What We Examined

The analysis combined three sources of SupportPulse data: customer records, support ticket records, and transaction records. The customer dataset was used to measure churn status. The ticket dataset contained 480 support tickets and was used to analyze resolution time, customer satisfaction, and escalations. Transaction data was used to estimate the recorded revenue associated with customers who have churned.

Across all support tickets, the average resolution time was 13.00 and the average CSAT score was 3.85. There were 87 recorded escalations.

## 3. Findings — What the Data Revealed

- **Overall churn is 22.50%.** Of the 120 customers analyzed, 27 are classified as churned.

- **Low customer satisfaction is associated with higher churn.** Customers in the Low CSAT group had a 36.36% churn rate, compared with 21.05% among customers in the Excellent CSAT group. This suggests that poor customer experience is an important signal for identifying customers who may require retention attention.

- **Multiple escalations are associated with higher churn in this dataset.** Customers with two escalations had a 36.36% churn rate, while customers with three escalations had a 50.00% churn rate. By comparison, customers with one escalation had a 17.07% churn rate. The groups with three or four escalations are small, so these results should be treated as risk signals rather than definitive conclusions.

- **Resolution time shows a mixed pattern that requires further investigation.** Customers in the less-than-two-hour group had a 33.33% churn rate, while the 4–24 hour group had a 20.39% churn rate. The 2–4 hour group had a 50.00% churn rate, but it contains only two customers. Therefore, the current dataset does not provide enough evidence to claim that slower resolution directly causes higher churn.

- **Churn has a measurable revenue impact.** The transaction data records $1,750 in revenue associated with customers classified as churned.

## 4. Anomaly Investigation — Why Is This Happening?

The strongest and most consistent signals in this analysis are customer satisfaction and repeated escalations. Customers experiencing low satisfaction have a substantially higher churn rate than customers in the Excellent CSAT group. Similarly, customers with multiple escalations show higher churn rates than customers with fewer escalations.

The resolution-time analysis is less conclusive. Some small groups show high churn, but the number of customers in those groups is too small to establish a reliable relationship. This indicates that SupportPulse should collect and analyze more historical support-response data before using resolution time alone as a churn predictor.

The evidence therefore suggests that customer experience indicators such as satisfaction and escalation frequency should be monitored together rather than relying on a single metric.

## 5. Recommendations — What Should We Do?

1. **Prioritize customers with low CSAT.**  
   Create a retention workflow for customers with low satisfaction scores because this group recorded a 36.36% churn rate. The Support Operations team should review these customers and initiate proactive follow-up within 48 hours.

2. **Monitor repeated escalations as an early warning signal.**  
   Customers with two or more escalations should be flagged for review. The Support Manager should investigate unresolved issues and assign ownership to prevent repeated complaints. This can be implemented as part of the existing support monitoring process.

3. **Improve the quality and history of support-time data.**  
   The current resolution-time groups are uneven, with some containing very few customers. The Analytics and Support teams should maintain historical response and resolution metrics and review them alongside churn over time. This will provide stronger evidence for determining whether faster support reduces churn.

## Conclusion

The analysis shows that SupportPulse has a 22.50% overall churn rate and that customer experience signals provide useful indicators of churn risk. Low CSAT and repeated escalations are particularly important signals in the current dataset, while the relationship between resolution time and churn requires more historical evidence. By combining these indicators into a proactive retention workflow, SupportPulse can identify customers needing attention earlier and make retention decisions using measurable business evidence.