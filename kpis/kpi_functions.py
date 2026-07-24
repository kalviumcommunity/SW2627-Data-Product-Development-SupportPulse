import pandas as pd
import numpy as np


def calculate_mau(df, days=30):
    """
    Monthly Active Users (MAU)
    """

    cutoff = (
        pd.Timestamp.now() -
        pd.Timedelta(days=days)
    )

    active_users = df[
        df["transaction_date"] >= cutoff
    ]["customer_id"].nunique()

    return active_users


def calculate_revenue_per_customer(df):
    """
    Average revenue per customer.
    """

    total_revenue = df["amount"].sum()

    unique_customers = (
        df["customer_id"].nunique()
    )

    if unique_customers == 0:
        return 0

    return (
        total_revenue /
        unique_customers
    )


def calculate_churn_rate(
    df,
    period_days=30
):
    """
    Customer churn rate.
    """

    today = pd.Timestamp.now()

    period_1_end = (
        today -
        pd.Timedelta(days=period_days)
    )

    period_1_start = (
        period_1_end -
        pd.Timedelta(days=period_days)
    )

    period_2_start = (
        today -
        pd.Timedelta(days=period_days)
    )

    active_period_1 = df[

        (
            df["transaction_date"] >=
            period_1_start
        )
        &
        (
            df["transaction_date"] <=
            period_1_end
        )

    ]["customer_id"].unique()

    active_period_2 = df[

        (
            df["transaction_date"] >=
            period_2_start
        )

    ]["customer_id"].unique()

    churned = len(

        [
            customer
            for customer in active_period_1
            if customer not in active_period_2
        ]

    )

    if len(active_period_1) == 0:
        return 0

    return (
        churned /
        len(active_period_1)
    )


def calculate_payment_success_rate(df):
    """
    Successful payment rate.
    """

    successful = len(

        df[
            df["payment_status"] ==
            "Success"
        ]

    )

    total = len(df)

    if total == 0:
        return 0

    return successful / total


def calculate_cac(
    marketing_cost,
    new_customers
):
    """
    Customer Acquisition Cost.
    """

    if new_customers == 0:
        return 0

    return (
        marketing_cost /
        new_customers
    )