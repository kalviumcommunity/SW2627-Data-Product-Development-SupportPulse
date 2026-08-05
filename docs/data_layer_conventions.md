# Data Layer Naming Conventions

## SQL Views

All SQL Views use the prefix:

vw_

Examples:

- vw_active_customers
- vw_revenue_by_region

Purpose:
Views provide reusable business logic for reporting and dashboards.

---

## Aggregated Tables

All aggregated tables use the prefix:

agg_

Examples:

- agg_daily_metrics

Purpose:
Aggregated tables store pre-computed metrics for faster dashboard performance.

---

## Naming Rules

- Use lowercase names
- Separate words using underscores
- Use meaningful names
- Keep names business-friendly

Examples:

vw_customer_retention

vw_support_summary

agg_daily_metrics

agg_monthly_revenue

---

## Benefits

- Consistent naming
- Easier maintenance
- Better readability
- Faster onboarding for new developers