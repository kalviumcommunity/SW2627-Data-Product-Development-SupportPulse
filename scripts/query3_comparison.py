"""
Task 3
CTE Demonstration using Pandas
"""

import pandas as pd
import os

# -----------------------------------
# Load Dataset
# -----------------------------------

transactions = pd.read_csv("data/raw/transactions.csv")

# -----------------------------------
# Create Customer Summary
# -----------------------------------

customer_summary = (
    transactions
    .groupby("customer_id")
    .agg(
        total_spent=("amount", "sum")
    )
    .reset_index()
)

print("=" * 60)
print("CUSTOMER SPENDING SUMMARY")
print("=" * 60)

print(customer_summary.head())

print("\nStatistics")
print(customer_summary["total_spent"].describe())

# -----------------------------------
# Dynamic Threshold
# -----------------------------------

threshold = customer_summary["total_spent"].median()

print(f"\nUsing Spending Threshold : {threshold:.2f}")

# -----------------------------------
# Original Query (Nested Query Equivalent)
# -----------------------------------

nested_result = (
    transactions
    .groupby("customer_id")["amount"]
    .sum()
    .reset_index()
)

nested_result.rename(
    columns={
        "amount": "total_spent"
    },
    inplace=True
)

nested_result = nested_result[
    nested_result["total_spent"] > threshold
]

# -----------------------------------
# CTE Equivalent
# -----------------------------------

cte_result = customer_summary[
    customer_summary["total_spent"] > threshold
]

# -----------------------------------
# Comparison
# -----------------------------------

print("\n" + "=" * 60)
print("QUERY 3 - CTE COMPARISON")
print("=" * 60)

print(f"Nested Query Rows : {len(nested_result)}")
print(f"CTE Query Rows    : {len(cte_result)}")

print(
    f"\nResults are identical : "
    f"{nested_result.equals(cte_result)}"
)

# -----------------------------------
# Save Output
# -----------------------------------

os.makedirs(
    "output/query_optimization",
    exist_ok=True
)

cte_result.to_csv(
    "output/query_optimization/query3_results.csv",
    index=False
)

summary = pd.DataFrame({
    "Metric": [
        "Threshold Used",
        "Nested Query Rows",
        "CTE Query Rows",
        "Results Match"
    ],
    "Value": [
        round(threshold, 2),
        len(nested_result),
        len(cte_result),
        nested_result.equals(cte_result)
    ]
})

summary.to_csv(
    "output/query_optimization/query3_summary.csv",
    index=False
)

print("\nFiles Generated:")
print("✔ query3_results.csv")
print("✔ query3_summary.csv")

print("\nCTE comparison completed successfully.")