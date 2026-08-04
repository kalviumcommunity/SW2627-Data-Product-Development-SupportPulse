"""
SupportPulse
Task 4 - Query Optimization Summary

Compares all optimization tasks and generates
a final report.
"""

import pandas as pd
import os

OUTPUT_DIR = "output/query_optimization"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# -------------------------------
# Load Reports
# -------------------------------

query1 = pd.read_csv(
    f"{OUTPUT_DIR}/query1_comparison.csv"
)

query2 = pd.read_csv(
    f"{OUTPUT_DIR}/query2_comparison.csv"
)

query3 = pd.read_csv(
    f"{OUTPUT_DIR}/query3_summary.csv"
)

print("=" * 70)
print("SUPPORTPULSE QUERY OPTIMIZATION SUMMARY")
print("=" * 70)

print("\nTask 1")
print(query1)

print("\nTask 2")
print(query2)

print("\nTask 3")
print(query3)

# -------------------------------
# Create Final Summary
# -------------------------------

summary = pd.DataFrame({

    "Optimization": [

        "Remove SELECT *",

        "Filter Before JOIN",

        "Replace Nested Query with CTE"

    ],

    "Benefit": [

        "Reduced unnecessary columns",

        "Reduced rows before JOIN",

        "Improved readability and maintenance"

    ],

    "Status": [

        "Completed",

        "Completed",

        "Completed"

    ]

})

summary.to_csv(

    f"{OUTPUT_DIR}/optimization_summary.csv",

    index=False

)

print("\nOptimization Summary")

print(summary)

print("\nSummary saved successfully.")