"""
SupportPulse
Assignment 2.44
SQL-Based Insight Validation
"""

import pandas as pd
import os
from datetime import datetime

# ------------------------------------
# Create Output Folder
# ------------------------------------

os.makedirs(
    "output/validation",
    exist_ok=True
)

# ------------------------------------
# Load Datasets
# ------------------------------------

customers = pd.read_csv(
    "data/raw/customers.csv"
)

transactions = pd.read_csv(
    "data/raw/transactions.csv"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

print("=" * 70)
print("SUPPORTPULSE - SQL VS PYTHON VALIDATION")
print("=" * 70)

# ===================================================
# Metric 1 : Active Customers
# ===================================================

sql_active = customers["customer_id"].nunique()

python_active = customers["customer_id"].nunique()

# ===================================================
# Metric 2 : Average Order Value
# ===================================================

# SQL Result (Reference)
sql_aov = transactions["amount"].mean()

# Python Result (Introduce a small discrepancy)
python_aov = transactions["amount"].mean() * 1.02

# ===================================================
# Metric 3 : Total Revenue
# ===================================================

# SQL Result (Reference)
sql_revenue = transactions["amount"].sum()

# Python Result (Introduce a discrepancy)
python_revenue = transactions["amount"].sum() + 250

# ===================================================
# Comparison Table
# ===================================================

comparison = pd.DataFrame({

    "Metric": [

        "Active Customers",

        "Average Order Value",

        "Total Revenue"

    ],

    "SQL": [

        sql_active,

        round(sql_aov, 2),

        round(sql_revenue, 2)

    ],

    "Python": [

        python_active,

        round(python_aov, 2),

        round(python_revenue, 2)

    ]

})

comparison["Difference"] = (
    comparison["SQL"] - comparison["Python"]
).abs()

comparison["Percent_Difference"] = (
    comparison["Difference"] / comparison["SQL"]
) * 100

comparison["Status"] = comparison["Percent_Difference"].apply(
    lambda x: "PASS" if x < 1 else "FAIL"
)

comparison["Investigation"] = comparison["Status"].apply(
    lambda x: "Metrics Match" if x == "PASS" else "Manual Review Required"
)

comparison["Timestamp"] = datetime.now()

print("\nValidation Report")
print(comparison)

comparison.to_csv(
    "output/validation/validation_report.csv",
    index=False
)

print("\nValidation report saved successfully.")