import os
import sqlite3

import numpy as np
import pandas as pd

def create_sample_data():

    np.random.seed(42)

    # Customers Table
    customers = pd.DataFrame({

        "customer_id": range(1, 51),

        "customer_type": np.random.choice(
            ["Enterprise", "SMB", "Startup"],
            50
        )

    })

    # Transactions Table
    transactions = pd.DataFrame({

        "order_id": range(1001, 1201),

        "customer_id": np.random.randint(
            1,
            51,
            200
        ),

        "transaction_date": pd.date_range(
            "2026-01-01",
            periods=200,
            freq="D"
        ),

        "amount": np.random.randint(
            500,
            10000,
            200
        )

    })

    transactions = transactions.merge(
        customers,
        on="customer_id"
    )

    # Users Table
    users = pd.DataFrame({

        "user_id": range(1, 101),

        "created_at": pd.date_range(
            "2026-01-01",
            periods=100,
            freq="D"
        ),

        "email_verified_at": pd.date_range(
            "2026-01-02",
            periods=100,
            freq="D"
        ),

        "first_purchase_at": pd.date_range(
            "2026-01-05",
            periods=100,
            freq="D"
        )

    })

    return customers, transactions, users

def setup_database():

    connection = sqlite3.connect(
        "business_metrics.db"
    )

    return connection

def load_tables(
    connection,
    customers,
    transactions,
    users
):

    customers.to_sql(

        "customers",

        connection,

        if_exists="replace",

        index=False

    )

    transactions.to_sql(

        "transactions",

        connection,

        if_exists="replace",

        index=False

    )

    users.to_sql(

        "users",

        connection,

        if_exists="replace",

        index=False

    )

    print("✓ Database tables created.")
def load_query(query_name):

    with open(

        f"queries/{query_name}.sql",

        "r"

    ) as file:

        return file.read()
def execute_query(

    connection,

    query_name

):

    query = load_query(

        query_name

    )

    result = pd.read_sql(

        query,

        connection

    )

    print("\n" + "=" * 60)

    print(query_name.upper())

    print("=" * 60)

    print(result.head())

    return result

def validate_metrics(
    mau_df,
    revenue_df,
    funnel_df
):
    """
    Validate metric computation results.
    """

    # Check for null values
    assert mau_df.isnull().sum().sum() == 0, \
        "MAU contains null values."

    assert revenue_df.isnull().sum().sum() == 0, \
        "Revenue contains null values."

    assert funnel_df.isnull().sum().sum() == 0, \
        "Funnel contains null values."

    # Revenue validation
    assert (
        revenue_df["monthly_revenue"] > 0
    ).all(), "Revenue must be greater than zero."

    # Conversion percentage validation
    assert (
        (funnel_df["conversion_pct"] >= 0)
        &
        (funnel_df["conversion_pct"] <= 100)
    ).all(), "Conversion percentage out of range."

    # Logical consistency
    for _, row in revenue_df.iterrows():

        assert row["order_count"] > 0, \
            "Order count cannot be zero."

        assert row["unique_customers"] > 0, \
            "Unique customers cannot be zero."

    print("\n" + "=" * 60)
    print("✓ ALL METRICS VALIDATED SUCCESSFULLY")
    print("=" * 60)

    return True

def main():

    customers, transactions, users = create_sample_data()

    connection = setup_database()

    load_tables(
        connection,
        customers,
        transactions,
        users
    )

    mau = execute_query(
        connection,
        "monthly_active_users"
    )

    revenue = execute_query(
        connection,
        "revenue_by_segment"
    )

    funnel = execute_query(
        connection,
        "conversion_funnel"
    )

    validate_metrics(
        mau,
        revenue,
        funnel
    )

    connection.close()

    print("\nAssignment Completed Successfully.")
if __name__ == "__main__":
    main()