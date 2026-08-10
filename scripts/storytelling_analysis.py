import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

customers = pd.read_csv(
    "data/raw/customers.csv"
)

tickets = pd.read_csv(
    "data/raw/tickets.csv"
)

transactions = pd.read_csv(
    "data/raw/transactions.csv"
)


# ==========================================
# BASIC CLEANING
# ==========================================

tickets["resolution_time"] = pd.to_numeric(
    tickets["resolution_time"],
    errors="coerce"
)

tickets["csat_score"] = pd.to_numeric(
    tickets["csat_score"],
    errors="coerce"
)

tickets["escalated"] = pd.to_numeric(
    tickets["escalated"],
    errors="coerce"
)

customers["churn_status"] = pd.to_numeric(
    customers["churn_status"],
    errors="coerce"
)


print("=" * 70)
print("SUPPORTPULSE - DATA STORYTELLING ANALYSIS")
print("=" * 70)


# ==========================================
# 1. OVERALL CUSTOMER METRICS
# ==========================================

total_customers = customers["customer_id"].nunique()

churned_customers = customers.loc[
    customers["churn_status"] == 1,
    "customer_id"
].nunique()

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0
    else 0
)


print("\nOVERALL METRICS")
print("-" * 40)

print(
    f"Total customers     : {total_customers}"
)

print(
    f"Churned customers   : {churned_customers}"
)

print(
    f"Overall churn rate  : {churn_rate:.2f}%"
)


# ==========================================
# 2. TICKET METRICS
# ==========================================

avg_resolution = tickets[
    "resolution_time"
].mean()

avg_csat = tickets[
    "csat_score"
].mean()

total_tickets = len(tickets)

total_escalations = tickets[
    "escalated"
].sum()


print("\nSUPPORT METRICS")
print("-" * 40)

print(
    f"Total tickets       : {total_tickets}"
)

print(
    f"Average resolution  : {avg_resolution:.2f}"
)

print(
    f"Average CSAT        : {avg_csat:.2f}"
)

print(
    f"Total escalations   : {total_escalations}"
)


# ==========================================
# 3. CUSTOMER + TICKET ANALYSIS
# ==========================================

ticket_summary = (
    tickets
    .groupby("customer_id")
    .agg(
        ticket_count=("ticket_id", "count"),
        avg_resolution=("resolution_time", "mean"),
        avg_csat=("csat_score", "mean"),
        escalations=("escalated", "sum")
    )
    .reset_index()
)


customer_analysis = customers.merge(
    ticket_summary,
    on="customer_id",
    how="left"
)


customer_analysis[
    [
        "ticket_count",
        "avg_resolution",
        "avg_csat",
        "escalations"
    ]
] = customer_analysis[
    [
        "ticket_count",
        "avg_resolution",
        "avg_csat",
        "escalations"
    ]
].fillna(0)


# ==========================================
# 4. CHURN BY RESOLUTION TIME
# ==========================================

customer_analysis["resolution_bucket"] = pd.cut(
    customer_analysis["avg_resolution"],
    bins=[
        -1,
        2,
        4,
        24,
        float("inf")
    ],
    labels=[
        "<2 hours",
        "2-4 hours",
        "4-24 hours",
        ">24 hours"
    ]
)


resolution_analysis = (
    customer_analysis
    .groupby(
        "resolution_bucket",
        observed=True
    )
    .agg(
        customers=("customer_id", "count"),
        churn_rate=("churn_status", "mean")
    )
    .reset_index()
)


resolution_analysis["churn_rate"] = (
    resolution_analysis["churn_rate"] * 100
)


print("\nCHURN BY RESPONSE / RESOLUTION TIME")
print("-" * 40)

print(
    resolution_analysis.to_string(
        index=False
    )
)


# ==========================================
# 5. CHURN BY CSAT
# ==========================================

customer_analysis["csat_bucket"] = pd.cut(
    customer_analysis["avg_csat"],
    bins=[
        -1,
        2,
        3,
        4,
        5
    ],
    labels=[
        "Low CSAT",
        "Below Average",
        "Good",
        "Excellent"
    ]
)


csat_analysis = (
    customer_analysis
    .groupby(
        "csat_bucket",
        observed=True
    )
    .agg(
        customers=("customer_id", "count"),
        churn_rate=("churn_status", "mean")
    )
    .reset_index()
)


csat_analysis["churn_rate"] = (
    csat_analysis["churn_rate"] * 100
)


print("\nCHURN BY CUSTOMER SATISFACTION")
print("-" * 40)

print(
    csat_analysis.to_string(
        index=False
    )
)


# ==========================================
# 6. CHURN BY ESCALATIONS
# ==========================================

escalation_analysis = (
    customer_analysis
    .groupby("escalations")
    .agg(
        customers=("customer_id", "count"),
        churn_rate=("churn_status", "mean")
    )
    .reset_index()
)


escalation_analysis["churn_rate"] = (
    escalation_analysis["churn_rate"] * 100
)


print("\nCHURN BY ESCALATIONS")
print("-" * 40)

print(
    escalation_analysis.to_string(
        index=False
    )
)


# ==========================================
# 7. REVENUE AT RISK
# ==========================================

revenue_by_customer = (
    transactions
    .groupby("customer_id")["amount"]
    .sum()
    .reset_index(
        name="total_revenue"
    )
)


customer_analysis = customer_analysis.merge(
    revenue_by_customer,
    on="customer_id",
    how="left"
)

customer_analysis["total_revenue"] = (
    customer_analysis["total_revenue"]
    .fillna(0)
)


revenue_at_risk = customer_analysis.loc[
    customer_analysis["churn_status"] == 1,
    "total_revenue"
].sum()


print("\nREVENUE IMPACT")
print("-" * 40)

print(
    f"Revenue from churned customers: "
    f"${revenue_at_risk:,.2f}"
)


# ==========================================
# 8. SAVE RESULTS
# ==========================================

resolution_analysis.to_csv(
    "supporting_evidence/"
    "resolution_time_churn.csv",
    index=False
)

csat_analysis.to_csv(
    "supporting_evidence/"
    "csat_churn.csv",
    index=False
)

escalation_analysis.to_csv(
    "supporting_evidence/"
    "escalation_churn.csv",
    index=False
)

customer_analysis.to_csv(
    "supporting_evidence/"
    "customer_story_data.csv",
    index=False
)


print("\nAnalysis files created successfully.")

print("=" * 70)
