import pandas as pd


def percentage_change(current, previous):
    """Calculate percentage change."""

    if previous == 0:
        return 0

    return ((current - previous) / previous) * 100


def get_trend_indicator(change, inverse=False):
    """Return trend arrow and color."""

    if inverse:
        if change < -2:
            return "↓", "green"
        elif change > 2:
            return "↑", "red"
        else:
            return "→", "orange"

    else:
        if change > 2:
            return "↑", "green"
        elif change < -2:
            return "↓", "red"
        else:
            return "→", "orange"


def calculate_kpis(customers, tickets, transactions):
    """Calculate dashboard KPIs."""

    # Convert date
    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"]
    )

    # Month column
    transactions["month"] = (
        transactions["transaction_date"]
        .dt.to_period("M")
    )

    months = sorted(
        transactions["month"].unique()
    )

    current_month = months[-1]

    if len(months) > 1:
        previous_month = months[-2]
    else:
        previous_month = current_month

    current_tx = transactions[
        transactions["month"] == current_month
    ]

    previous_tx = transactions[
        transactions["month"] == previous_month
    ]

    # Revenue
    current_revenue = current_tx["amount"].sum()
    previous_revenue = previous_tx["amount"].sum()

    revenue_change = percentage_change(
        current_revenue,
        previous_revenue
    )

    # Active Customers
    current_users = current_tx[
        "customer_id"
    ].nunique()

    previous_users = previous_tx[
        "customer_id"
    ].nunique()

    users_change = percentage_change(
        current_users,
        previous_users
    )

    # Average Order Value
    current_aov = current_tx[
        "amount"
    ].mean()

    previous_aov = previous_tx[
        "amount"
    ].mean()

    aov_change = percentage_change(
        current_aov,
        previous_aov
    )

    # Churn Rate
    current_churn = (
        customers["churn_status"].mean() * 100
    )

    previous_churn = current_churn

    churn_change = percentage_change(
        current_churn,
        previous_churn
    )

    # Customer Satisfaction
    current_csat = tickets[
        "csat_score"
    ].mean()

    previous_csat = current_csat

    csat_change = percentage_change(
        current_csat,
        previous_csat
    )

    return {

        "Revenue": (
            current_revenue,
            revenue_change
        ),

        "Active Customers": (
            current_users,
            users_change
        ),

        "Average Order Value": (
            current_aov,
            aov_change
        ),

        "Churn Rate": (
            current_churn,
            churn_change
        ),

        "Customer Satisfaction": (
            current_csat,
            csat_change
        )

    }