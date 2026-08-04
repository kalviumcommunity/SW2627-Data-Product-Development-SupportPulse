"""
Task 1
Compare SELECT * vs Explicit Columns
"""

import pandas as pd
import os

# Load datasets
transactions = pd.read_csv("data/raw/transactions.csv")
customers = pd.read_csv("data/raw/customers.csv")

# Join datasets
joined = transactions.merge(
    customers,
    on="customer_id",
    how="inner"
)

# ----------------------------
# Original Query (SELECT *)
# ----------------------------
original_result = joined.copy()

# ----------------------------
# Optimized Query
# ----------------------------
optimized_result = joined[
    [
        "customer_id",
        "transaction_date",
        "amount",
        "name",
        "plan_type",
        "region",
        "monthly_spend"
    ]
]

print("=" * 60)
print("QUERY 1 COMPARISON")
print("=" * 60)

print(f"Original Columns : {original_result.shape[1]}")
print(f"Optimized Columns: {optimized_result.shape[1]}")

column_reduction = (
    (
        original_result.shape[1]
        - optimized_result.shape[1]
    )
    /
    original_result.shape[1]
) * 100

print(f"Column Reduction : {column_reduction:.2f}%")

print(f"Rows Returned : {len(original_result)}")

os.makedirs(
    "output/query_optimization",
    exist_ok=True
)

comparison = pd.DataFrame({
    "Metric": [
        "Columns Selected",
        "Rows Returned",
        "Column Reduction (%)"
    ],
    "Original": [
        original_result.shape[1],
        len(original_result),
        0
    ],
    "Optimized": [
        optimized_result.shape[1],
        len(optimized_result),
        round(column_reduction, 2)
    ]
})

comparison.to_csv(
    "output/query_optimization/query1_comparison.csv",
    index=False
)

print("\nComparison saved successfully.")