import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Create Output Folder
# ----------------------------------------------------

os.makedirs(
    "output/visualizations",
    exist_ok=True
)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

customers = pd.read_csv(
    "data/raw/customers.csv"
)

transactions = pd.read_csv(
    "data/raw/transactions.csv"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

# ----------------------------------------------------
# Merge
# ----------------------------------------------------

df = transactions.merge(
    customers,
    on="customer_id",
    how="left"
)

# ----------------------------------------------------
# Company Colour Palette
# ----------------------------------------------------

PALETTE = {

    "primary": "#1f77b4",

    "secondary": "#ff7f0e",

    "success": "#2ca02c",

    "danger": "#d62728",

    "neutral": "#7f7f7f"

}

COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd"
]

# ====================================================
# CHART 1
# Revenue by Region
# ====================================================

region = (
    df.groupby("region")["amount"]
    .sum()
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10,6))

bars = ax.barh(
    region.index,
    region.values,
    color=COLORS
)

ax.set_title(
    "Revenue by Region",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Revenue ($)")
ax.set_ylabel("Region")

for bar in bars:

    ax.text(
        bar.get_width()+5,
        bar.get_y()+bar.get_height()/2,
        f"{bar.get_width():.0f}",
        va="center"
    )

highest = region.idxmax()

ax.annotate(
    "Highest Revenue",
    xy=(region.max(), highest),
    xytext=(region.max()+150, highest),
    arrowprops=dict(arrowstyle="->")
)

plt.tight_layout()

plt.savefig(
    "output/visualizations/chart1_revenue_by_region.png",
    dpi=300
)

plt.close()

# ====================================================
# CHART 2
# Monthly Revenue Trend
# ====================================================

monthly = (
    df.groupby(
        df["transaction_date"].dt.to_period("M")
    )["amount"]
    .sum()
)

monthly.index = monthly.index.astype(str)

fig, ax = plt.subplots(figsize=(10,6))

ax.plot(
    monthly.index,
    monthly.values,
    marker="o",
    linewidth=2,
    color=PALETTE["primary"],
    label="Revenue"
)

ax.set_title(
    "Monthly Revenue Trend",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.legend()

peak = monthly.idxmax()

ax.annotate(
    "Peak Revenue",
    xy=(peak, monthly.max()),
    xytext=(peak, monthly.max()+100),
    arrowprops=dict(arrowstyle="->")
)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "output/visualizations/chart2_monthly_revenue.png",
    dpi=300
)

plt.close()

# ====================================================
# CHART 3
# Histogram
# ====================================================

fig, ax = plt.subplots(figsize=(10,6))

ax.hist(
    df["amount"],
    bins=10,
    color=PALETTE["secondary"]
)

ax.set_title(
    "Transaction Amount Distribution",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Transaction Amount ($)")
ax.set_ylabel("Frequency")

mean_amount = df["amount"].mean()

ax.axvline(
    mean_amount,
    color="red",
    linestyle="--",
    label="Average"
)

ax.legend()

plt.tight_layout()

plt.savefig(
    "output/visualizations/chart3_transaction_distribution.png",
    dpi=300
)

plt.close()

# ====================================================
# CHART 4
# Stacked Bar
# ====================================================

pivot = pd.pivot_table(

    df,

    values="amount",

    index=df["transaction_date"].dt.to_period("M"),

    columns="plan_type",

    aggfunc="sum",

    fill_value=0

)

pivot.index = pivot.index.astype(str)

fig, ax = plt.subplots(figsize=(12,6))

pivot.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    color=COLORS
)

ax.set_title(
    "Revenue by Month and Plan Type",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")

plt.legend(title="Plan Type")

plt.tight_layout()

plt.savefig(
    "output/visualizations/chart4_revenue_by_plan.png",
    dpi=300
)

plt.close()

# ====================================================
# CHART 5
# Scatter Plot
# ====================================================

customer_revenue = (

    df.groupby("customer_id")["amount"]

    .sum()

    .reset_index()

)

customer_revenue = customer_revenue.merge(

    customers[

        [
            "customer_id",

            "monthly_spend"

        ]

    ],

    on="customer_id"

)

fig, ax = plt.subplots(figsize=(10,6))

ax.scatter(

    customer_revenue["monthly_spend"],

    customer_revenue["amount"],

    color=PALETTE["success"]

)

ax.set_title(
    "Monthly Spend vs Revenue",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Monthly Spend ($)")
ax.set_ylabel("Revenue ($)")

largest = customer_revenue["amount"].idxmax()

ax.annotate(

    "Highest Revenue Customer",

    xy=(

        customer_revenue.loc[largest,"monthly_spend"],

        customer_revenue.loc[largest,"amount"]

    ),

    xytext=(

        customer_revenue.loc[largest,"monthly_spend"]+20,

        customer_revenue.loc[largest,"amount"]+100

    ),

    arrowprops=dict(arrowstyle="->")

)

plt.tight_layout()

plt.savefig(

    "output/visualizations/chart5_spend_vs_revenue.png",

    dpi=300

)

plt.close()

print("="*60)
print("ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
print("="*60)

print("Files Saved:")

print("✔ chart1_revenue_by_region.png")
print("✔ chart2_monthly_revenue.png")
print("✔ chart3_transaction_distribution.png")
print("✔ chart4_revenue_by_plan.png")
print("✔ chart5_spend_vs_revenue.png")