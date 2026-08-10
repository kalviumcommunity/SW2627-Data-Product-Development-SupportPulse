import os
import pandas as pd
import plotly.express as px

from export_functions import export_analysis


# ==========================================
# LOAD SUPPORTPULSE DATA
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
# PREPARE DATA
# ==========================================

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

tickets["csat_score"] = pd.to_numeric(
    tickets["csat_score"],
    errors="coerce"
)

tickets["resolution_time"] = pd.to_numeric(
    tickets["resolution_time"],
    errors="coerce"
)

tickets["escalated"] = pd.to_numeric(
    tickets["escalated"],
    errors="coerce"
)


# ==========================================
# CREATE CUSTOMER ANALYSIS DATASET
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


revenue_summary = (
    transactions
    .groupby("customer_id")
    .agg(
        total_revenue=("amount", "sum"),
        transaction_count=("amount", "count")
    )
    .reset_index()
)


analysis_df = customers.merge(
    ticket_summary,
    on="customer_id",
    how="left"
)


analysis_df = analysis_df.merge(
    revenue_summary,
    on="customer_id",
    how="left"
)


# Fill missing values

numeric_columns = [
    "ticket_count",
    "avg_resolution",
    "avg_csat",
    "escalations",
    "total_revenue",
    "transaction_count"
]

for column in numeric_columns:

    if column in analysis_df.columns:

        analysis_df[column] = (
            analysis_df[column]
            .fillna(0)
        )


# ==========================================
# CHART 1 — CHURN BY CSAT
# ==========================================

csat_df = (
    analysis_df
    .assign(
        csat_bucket=pd.cut(
            analysis_df["avg_csat"],
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
    )
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


csat_df["churn_rate"] = (
    csat_df["churn_rate"] * 100
)


fig_csat = px.bar(
    csat_df,
    x="csat_bucket",
    y="churn_rate",
    title="Churn Rate by Customer Satisfaction",
    labels={
        "csat_bucket": "CSAT Group",
        "churn_rate": "Churn Rate (%)"
    },
    text="churn_rate"
)


fig_csat.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)


# ==========================================
# CHART 2 — CHURN BY ESCALATIONS
# ==========================================

escalation_df = (
    analysis_df
    .groupby("escalations")
    .agg(
        customers=("customer_id", "count"),
        churn_rate=("churn_status", "mean")
    )
    .reset_index()
)


escalation_df["churn_rate"] = (
    escalation_df["churn_rate"] * 100
)


fig_escalations = px.bar(
    escalation_df,
    x="escalations",
    y="churn_rate",
    title="Churn Rate by Support Escalations",
    labels={
        "escalations": "Number of Escalations",
        "churn_rate": "Churn Rate (%)"
    },
    text="churn_rate"
)


fig_escalations.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)


# ==========================================
# CHART 3 — REVENUE BY CHURN STATUS
# ==========================================

revenue_df = (
    analysis_df
    .groupby("churn_status")
    .agg(
        total_revenue=("total_revenue", "sum")
    )
    .reset_index()
)


revenue_df["status"] = (
    revenue_df["churn_status"]
    .map({
        0: "Active",
        1: "Churned"
    })
)


fig_revenue = px.bar(
    revenue_df,
    x="status",
    y="total_revenue",
    title="Revenue by Customer Churn Status",
    labels={
        "status": "Customer Status",
        "total_revenue": "Revenue"
    },
    text="total_revenue"
)


fig_revenue.update_traces(
    texttemplate="$%{text:.2f}",
    textposition="outside"
)


# ==========================================
# LOAD EXECUTIVE SUMMARY
# ==========================================

with open(
    "executive_summary.md",
    "r",
    encoding="utf-8"
) as file:

    summary = file.read()


# ==========================================
# CHART COLLECTION
# ==========================================

charts = {

    "Churn by Customer Satisfaction":
        fig_csat,

    "Churn by Support Escalations":
        fig_escalations,

    "Revenue by Customer Status":
        fig_revenue

}


# ==========================================
# EXPORT
# ==========================================

report_dir = export_analysis(
    df=analysis_df,
    summary_text=summary,
    charts_dict=charts,
    output_dir="output/reports"
)


print()
print("EXPORT COMPLETED SUCCESSFULLY")
print()
print(
    f"Report directory: {report_dir}"
)