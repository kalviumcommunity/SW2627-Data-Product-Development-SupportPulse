import pandas as pd
import matplotlib.pyplot as plt
import os

customers = pd.read_csv(
    "data/processed/feature_engineered_customers.csv"
)

tickets = pd.read_csv(
    "data/processed/feature_engineered_tickets.csv"
)

os.makedirs("output/charts", exist_ok=True)

plan = customers.groupby(
    "plan_type"
)["churn_status"].mean() * 100

plt.figure(figsize=(6,4))
plan.plot(kind="bar")

plt.title("Churn Rate by Plan")
plt.ylabel("Churn Rate (%)")

plt.tight_layout()

plt.savefig(
    "output/charts/churn_by_plan.png"
)

plt.close()

customers["region"].value_counts().plot(
    kind="bar",
    figsize=(6,4)
)

plt.title("Customers by Region")
plt.ylabel("Customers")

plt.tight_layout()

plt.savefig(
    "output/charts/customers_by_region.png"
)

plt.close()

tickets["ticket_category"].value_counts().plot(
    kind="bar",
    figsize=(7,4)
)

plt.title("Ticket Categories")
plt.ylabel("Tickets")

plt.tight_layout()

plt.savefig(
    "output/charts/ticket_categories.png"
)

plt.close()
tickets["priority"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    figsize=(6,6)
)

plt.ylabel("")

plt.title("Ticket Priority Distribution")

plt.savefig(
    "output/charts/priority_distribution.png"
)

plt.close()
tickets["resolution_time"].plot(
    kind="hist",
    bins=20,
    figsize=(6,4)
)

plt.title("Resolution Time Distribution")
plt.xlabel("Hours")

plt.tight_layout()

plt.savefig(
    "output/charts/resolution_time.png"
)

plt.close()
tickets["csat_score"].plot(
    kind="hist",
    bins=5,
    figsize=(6,4)
)

plt.title("CSAT Distribution")
plt.xlabel("Score")

plt.tight_layout()

plt.savefig(
    "output/charts/csat_distribution.png"
)

plt.close()
customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

monthly = customers.groupby(
    customers["signup_date"].dt.to_period("M")
).size()

monthly.index = monthly.index.astype(str)

monthly.plot(
    figsize=(8,4)
)

plt.title("Monthly Customer Signups")
plt.ylabel("Customers")

plt.tight_layout()

plt.savefig(
    "output/charts/monthly_signups.png"
)

plt.close()