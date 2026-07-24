import sqlite3
import pandas as pd
import numpy as np

def create_sample_data():

    np.random.seed(42)

    # Customers table
    customers = pd.DataFrame({

        "customer_id": range(1, 51),

        "customer_type": np.random.choice(
            ["Enterprise", "SMB", "Startup"],
            50
        ),

        "industry": np.random.choice(
            ["Healthcare", "Finance", "Retail", "Education"],
            50
        )

    })

    # Transactions table
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
        ),

        "transaction_status": np.random.choice(
            ["completed", "pending"],
            200,
            p=[0.9, 0.1]
        )

    })

    transactions = transactions.merge(
        customers,
        on="customer_id"
    )

    return customers, transactions
def setup_database():

    connection = sqlite3.connect(
        "filtering_grouping.db"
    )

    return connection
def load_tables(
    connection,
    customers,
    transactions
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

    print("✓ Tables Loaded Successfully")

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

    query = load_query(query_name)

    result = pd.read_sql(
        query,
        connection
    )

    print("\n" + "=" * 60)
    print(query_name.upper())
    print("=" * 60)

    print(result.head())

    return result

def validate_results(
    where_df,
    group_df,
    having_df,
    combined_df,
    ranking_df
):
    """
    Validate query results.
    """

    # Ensure queries returned data
    assert len(where_df) > 0, \
        "WHERE query returned no rows."

    assert len(group_df) > 0, \
        "GROUP BY query returned no rows."

    assert len(having_df) > 0, \
        "HAVING query returned no rows."

    assert len(combined_df) > 0, \
        "WHERE + HAVING query returned no rows."

    assert len(ranking_df) > 0, \
        "Ranking query returned no rows."

    # Revenue checks
    assert (
        where_df["annual_revenue"] > 0
    ).all(), "Invalid annual revenue."

    assert (
        group_df["monthly_revenue"] > 0
    ).all(), "Invalid monthly revenue."

    # HAVING logic validation
    assert (
        having_df["annual_revenue"] > 10000
    ).all(), "HAVING condition failed."

    assert (
        having_df["transaction_count"] >= 5
    ).all(), "Transaction count condition failed."

    # Ranking validation
    assert (
        ranking_df["revenue_rank"] >= 1
    ).all(), "Invalid rank values."

    print("\n" + "=" * 60)
    print("✓ ALL QUERY RESULTS VALIDATED")
    print("=" * 60)

    return True
def main():

    customers, transactions = create_sample_data()

    connection = setup_database()

    load_tables(
        connection,
        customers,
        transactions
    )

    where_df = execute_query(
        connection,
        "where_filtering"
    )

    group_df = execute_query(
        connection,
        "groupby_aggregation"
    )

    having_df = execute_query(
        connection,
        "having_filtering"
    )

    combined_df = execute_query(
        connection,
        "where_having_combined"
    )

    ranking_df = execute_query(
        connection,
        "orderby_ranking"
    )

    validate_results(
        where_df,
        group_df,
        having_df,
        combined_df,
        ranking_df
    )

    connection.close()

    print("\nAssignment Completed Successfully.")


if __name__ == "__main__":
    main()