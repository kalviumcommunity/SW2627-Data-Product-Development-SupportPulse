import sqlite3
import numpy as np
import pandas as pd

def create_sample_data():

    np.random.seed(42)

    # Customers
    customers = pd.DataFrame({

        "customer_id": range(1, 51),

        "customer_type": np.random.choice(
            ["Enterprise", "SMB", "Startup"],
            50
        ),

        "signup_date": pd.date_range(
            "2025-01-01",
            periods=50
        )

    })

    # Products
    products = pd.DataFrame({

        "product_id": range(1, 11),

        "product_name": [
            f"Product_{i}"
            for i in range(1,11)
        ]

    })

    # Orders
    orders = pd.DataFrame({

        "order_id": range(1001,1151),

        "customer_id": np.random.randint(
            1,
            55,
            150
        ),

        "order_date": pd.date_range(
            "2026-01-01",
            periods=150
        ),

        "order_amount": np.random.randint(
            500,
            5000,
            150
        )

    })

    # Order Items
    order_items = pd.DataFrame({

        "order_item_id": range(1,301),

        "order_id": np.random.choice(
            orders["order_id"],
            300
        ),

        "product_id": np.random.randint(
            1,
            11,
            300
        ),

        "quantity": np.random.randint(
            1,
            5,
            300
        ),

        "unit_price": np.random.randint(
            100,
            1500,
            300
        )

    })

    return customers, orders, order_items, products
def setup_database():

    connection = sqlite3.connect(
        "joins_analysis.db"
    )

    return connection
def load_tables(
    connection,
    customers,
    orders,
    order_items,
    products
):

    customers.to_sql(
        "customers",
        connection,
        if_exists="replace",
        index=False
    )

    orders.to_sql(
        "orders",
        connection,
        if_exists="replace",
        index=False
    )

    order_items.to_sql(
        "order_items",
        connection,
        if_exists="replace",
        index=False
    )

    products.to_sql(
        "products",
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
def compare_row_counts(
    customers,
    orders,
    left_join_df
):

    customers_count = len(customers)

    orders_count = len(orders)

    joined_count = len(left_join_df)

    print("\n" + "=" * 60)
    print("ROW COUNT VALIDATION")
    print("=" * 60)

    print(f"Customers : {customers_count}")
    print(f"Orders    : {orders_count}")
    print(f"LEFT JOIN : {joined_count}")

    print(
        f"Difference : {joined_count-customers_count}"
    )
def unmatched_analysis(
    no_orders,
    orphan_orders,
    customers
):

    print("\n" + "=" * 60)
    print("UNMATCHED RECORDS")
    print("=" * 60)

    print(
        f"Customers without orders : {len(no_orders)}"
    )

    print(
        f"Orphaned orders : {len(orphan_orders)}"
    )

    pct = (
        len(no_orders) /
        len(customers)
    ) * 100

    print(
        f"Percentage : {pct:.2f}%"
    )

    if len(orphan_orders) > 0:

        print(
            "Investigate customer_id mismatch."
        )
def validate_joins(
    inner_df,
    left_df,
    full_df,
    multi_df
):
    """
    Validate join relationships.
    """

    assert len(inner_df) > 0, \
        "INNER JOIN returned no rows."

    assert len(left_df) >= len(inner_df), \
        "LEFT JOIN should return at least as many rows as INNER JOIN."

    assert len(full_df) >= len(left_df), \
        "FULL OUTER JOIN should return at least as many rows as LEFT JOIN."

    assert len(multi_df) > 0, \
        "Multi-table JOIN returned no rows."

    print("\n" + "=" * 60)
    print("JOIN VALIDATION")
    print("=" * 60)

    print("✓ INNER JOIN validated")
    print("✓ LEFT JOIN validated")
    print("✓ FULL OUTER JOIN validated")
    print("✓ Multi-table JOIN validated")
def join_documentation():

    documentation = """
============================================================
JOIN STRATEGY DOCUMENTATION
============================================================

1. Customers LEFT JOIN Orders
--------------------------------
Purpose:
Retrieve all customers and their order history.

Business Use:
Customer Lifetime Value (CLV), customer segmentation.

Expected Row Change:
One customer may have multiple orders, so rows can increase.

------------------------------------------------------------

2. Orders LEFT JOIN Order Items
--------------------------------
Purpose:
Retrieve every product purchased in each order.

Business Use:
Revenue by product, inventory analysis.

Expected Row Change:
One order may contain multiple products.

------------------------------------------------------------

3. Multi-table JOIN
--------------------------------
Customers
    ↓
Orders
    ↓
Order Items
    ↓
Products

Purpose:
Complete order analysis with customer and product information.

Risk:
Duplicate rows due to one-to-many relationships.

Validation:
Aggregate carefully to avoid double-counting.

============================================================
"""

    print(documentation)

def main():

    customers, orders, order_items, products = create_sample_data()

    connection = setup_database()

    load_tables(
        connection,
        customers,
        orders,
        order_items,
        products
    )

    left_validation = execute_query(
        connection,
        "left_join_validation"
    )

    no_orders = execute_query(
        connection,
        "unmatched_customers"
    )

    orphan_orders = execute_query(
        connection,
        "orphan_orders"
    )

    inner = execute_query(
        connection,
        "inner_join"
    )

    left = execute_query(
        connection,
        "left_join"
    )

    full = execute_query(
        connection,
        "full_outer_join"
    )

    multi = execute_query(
        connection,
        "multi_table_join"
    )

    compare_row_counts(
        customers,
        orders,
        left_validation
    )

    unmatched_analysis(
        no_orders,
        orphan_orders,
        customers
    )

    validate_joins(
        inner,
        left,
        full,
        multi
    )

    join_documentation()

    connection.close()

    print("\nAssignment Completed Successfully.")


if __name__ == "__main__":
    main()