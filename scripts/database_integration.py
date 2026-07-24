import os
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import inspect

def create_sample_dataset():
    """
    Create a cleaned customer dataset.
    """

    np.random.seed(42)

    total = 100

    df = pd.DataFrame({

        "customer_id":
            range(1, total + 1),

        "customer_name":
            [f"Customer_{i}" for i in range(1, total + 1)],

        "email":
            [f"user{i}@mail.com" for i in range(1, total + 1)],

        "customer_type":
            np.random.choice(
                ["Enterprise", "SMB", "Startup"],
                total
            ),

        "signup_date":
            pd.date_range(
                "2025-01-01",
                periods=total
            ),

        "lifetime_value":
            np.random.randint(
                1000,
                20000,
                total
            )

    })

    return df
def setup_database():

    """
    Create SQLite database connection.
    """

    engine = create_engine(
        "sqlite:///analytics.db"
    )

    with engine.connect():

        print(
            "✓ Database connection successful."
        )

    return engine   

def load_dataframe(
    df,
    engine
):
    """
    Load cleaned data into SQL table.
    """

    table_name = "customers_cleaned"

    df.to_sql(

        table_name,

        engine,

        if_exists="replace",

        index=False

    )

    print(
        "\nTable Loaded Successfully."
    )

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    print(
        "\nAvailable Tables"
    )

    print(tables)

    count = pd.read_sql(

        f"""
        SELECT COUNT(*) AS row_count
        FROM {table_name}
        """,

        engine

    )

    print(
        "\nRows Loaded :",
        count.iloc[0]["row_count"]
    )

    return table_name

def validate_schema(engine, table_name):
    """
    Inspect table schema and validate datatypes.
    """

    inspector = inspect(engine)

    columns = inspector.get_columns(table_name)

    print("\n" + "=" * 60)
    print("TABLE SCHEMA")
    print("=" * 60)

    for col in columns:

        nullable = (
            "NOT NULL"
            if col["nullable"] is False
            else "NULL"
        )

        print(
            f"{col['name']:<20}"
            f"{str(col['type']):<20}"
            f"{nullable}"
        )

    print("\nDatatype Validation")

    expected_types = {

        "customer_id": "INTEGER",

        "email": "VARCHAR",

        "signup_date": "DATE"

    }

    for column_name, expected in expected_types.items():

        actual = None

        for column in columns:

            if column["name"] == column_name:

                actual = str(column["type"])

                break

        if actual is None:

            print(f"✗ {column_name} not found")

            continue

        if expected in actual.upper():

            print(f"✓ {column_name} -> {actual}")

        else:

            print(f"✗ {column_name} -> {actual}")
def query_enterprise_customers(
    engine,
    table_name
):
    """
    Retrieve Enterprise customers.
    """

    query = f"""
    SELECT *
    FROM {table_name}
    WHERE customer_type='Enterprise'
    """

    results = pd.read_sql(
        query,
        engine
    )

    print("\n" + "=" * 60)
    print("ENTERPRISE CUSTOMERS")
    print("=" * 60)

    print(
        f"Retrieved {len(results)} rows."
    )

    print(results.head())

    return results
def customer_summary(
    engine,
    table_name
):
    """
    Aggregate customer statistics.
    """

    query = f"""
    SELECT

        customer_type,

        COUNT(*) AS customer_count,

        ROUND(
            AVG(lifetime_value),
            2
        ) AS avg_lifetime_value

    FROM {table_name}

    GROUP BY customer_type

    ORDER BY avg_lifetime_value DESC
    """

    summary = pd.read_sql(
        query,
        engine
    )

    print("\n" + "=" * 60)
    print("CUSTOMER SUMMARY")
    print("=" * 60)

    print(summary)

    return summary
def load_cleaned_data_to_database(
    df,
    table_name,
    database_path="analytics.db"
):
    """
    Load cleaned DataFrame into SQLite database.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned dataset.

    table_name : str
        SQL table name.

    database_path : str
        SQLite database filename.
    """

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    count = pd.read_sql(
        f"""
        SELECT COUNT(*) AS total
        FROM {table_name}
        """,
        engine
    )

    rows_loaded = count.iloc[0]["total"]

    print(
        f"\n✓ Loaded {rows_loaded} rows into '{table_name}'."
    )

    return engine

def verify_database(
    engine,
    table_name
):
    """
    Verify database contents.
    """

    sample = pd.read_sql(
        f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
        """,
        engine
    )

    print("\n" + "=" * 60)
    print("DATABASE SAMPLE")
    print("=" * 60)

    print(sample)

    return sample


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    # Create sample cleaned data
    df = create_sample_dataset()

    print("\nDataset Preview")
    print(df.head())

    # Initial database setup
    engine = setup_database()

    table_name = load_dataframe(
        df,
        engine
    )

    # Validate schema
    validate_schema(
        engine,
        table_name
    )

    # Run SQL queries
    query_enterprise_customers(
        engine,
        table_name
    )

    customer_summary(
        engine,
        table_name
    )

    # Repeatable loader
    reusable_engine = load_cleaned_data_to_database(
        df,
        table_name
    )

    verify_database(
        reusable_engine,
        table_name
    )

    print("\nSQL Integration Completed Successfully.")


if __name__ == "__main__":
    main()