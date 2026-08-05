"""
SupportPulse
Task 3 - Data Layer Demonstration

Simulates querying SQL Views and
Aggregated Tables using CSV datasets.
"""

import pandas as pd
import os
import time

# ---------------------------------------
# Create Output Folder
# ---------------------------------------

os.makedirs(
    "output/data_layer",
    exist_ok=True
)

# ---------------------------------------
# Load Data
# ---------------------------------------

customers = pd.read_csv(
    "data/raw/customers.csv"
)

transactions = pd.read_csv(
    "data/raw/transactions.csv"
)

print("=" * 70)
print("SUPPORTPULSE DATA LAYER DEMO")
print("=" * 70)

# =======================================
# View 1 : Active Customers
# =======================================

active_customers = (

    transactions

    .groupby("customer_id")

    .agg(

        transaction_count=("amount", "count"),

        total_spent=("amount", "sum"),

        last_transaction=("transaction_date", "max")

    )

    .reset_index()

)

active_customers = active_customers.merge(

    customers,

    on="customer_id",

    how="left"

)

print("\nVIEW : ACTIVE CUSTOMERS")

print(active_customers.head())

active_customers.to_csv(

    "output/data_layer/active_customers.csv",

    index=False

)

# =======================================
# View 2 : Revenue By Region
# =======================================

revenue_region = (

    active_customers

    .groupby("region")

    .agg(

        total_customers=("customer_id", "count"),

        total_revenue=("total_spent", "sum"),

        average_revenue=("total_spent", "mean")

    )

    .reset_index()

)

print("\nVIEW : REVENUE BY REGION")

print(revenue_region)

revenue_region.to_csv(

    "output/data_layer/revenue_by_region.csv",

    index=False

)

# =======================================
# Aggregated Daily Metrics
# =======================================

transactions["transaction_date"] = pd.to_datetime(

    transactions["transaction_date"]

)

daily_metrics = (

    transactions

    .groupby(

        transactions["transaction_date"].dt.date

    )

    .agg(

        total_transactions=("amount", "count"),

        total_revenue=("amount", "sum"),

        average_transaction=("amount", "mean")

    )

    .reset_index()

)

daily_metrics.rename(

    columns={

        "transaction_date": "aggregation_date"

    },

    inplace=True

)

daily_metrics["updated_at"] = pd.Timestamp.now()

print("\nAGGREGATED DAILY METRICS")

print(daily_metrics.head())

daily_metrics.to_csv(

    "output/data_layer/daily_metrics.csv",

    index=False

)
# =======================================
# Performance Demo
# =======================================

start = time.perf_counter()

total_revenue = daily_metrics["total_revenue"].sum()

total_transactions = daily_metrics["total_transactions"].sum()

average_transaction = daily_metrics["average_transaction"].mean()

elapsed = (time.perf_counter() - start) * 1000

print(f"\nAggregation Query Time : {elapsed:.2f} ms")

summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Transactions",
        "Average Transaction"
    ],
    "Value": [
        total_revenue,
        total_transactions,
        round(average_transaction, 2)
    ]
})

print("\nSummary")
print(summary)

summary.to_csv(
    "output/data_layer/data_layer_summary.csv",
    index=False
)