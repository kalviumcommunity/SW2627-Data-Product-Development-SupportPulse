"""
Task 2
Filter Before JOIN
"""

import pandas as pd
import os

# Load datasets
transactions = pd.read_csv("data/raw/transactions.csv")
customers = pd.read_csv("data/raw/customers.csv")

# -----------------------------
# Original Query
# Join first, then filter
# -----------------------------
joined_original = transactions.merge(
    customers,
    on="customer_id",
    how="inner"
)

original_result = joined_original[
    joined_original["plan_type"] == "Premium"
]

# -----------------------------
# Optimized Query
# Filter first, then join
# -----------------------------
premium_customers = customers[
    customers["plan_type"] == "Premium"
]

optimized_result = transactions.merge(
    premium_customers,
    on="customer_id",
    how="inner"
)

print("=" * 60)
print("QUERY 2 - FILTER BEFORE JOIN")
print("=" * 60)

print(f"Rows after Original Query : {len(original_result)}")
print(f"Rows after Optimized Query: {len(optimized_result)}")

print(f"Customers Before Filter : {len(customers)}")
print(f"Customers After Filter  : {len(premium_customers)}")

reduction = (
    (len(customers) - len(premium_customers))
    / len(customers)
) * 100

print(f"Dataset Reduction : {reduction:.2f}%")

# Save results
os.makedirs(
    "output/query_optimization",
    exist_ok=True
)

summary = pd.DataFrame({
    "Metric": [
        "Customers Before Filter",
        "Customers After Filter",
        "Rows Returned",
        "Reduction (%)"
    ],
    "Value": [
        len(customers),
        len(premium_customers),
        len(optimized_result),
        round(reduction, 2)
    ]
})

summary.to_csv(
    "output/query_optimization/query2_comparison.csv",
    index=False
)

print("\nComparison saved successfully.")