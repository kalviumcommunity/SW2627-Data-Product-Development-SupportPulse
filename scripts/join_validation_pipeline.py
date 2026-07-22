import pandas as pd
import numpy as np
import json
import os


def create_customer_dataset():
    """
    Create sample customer dataset.
    """

    customers = pd.DataFrame({

        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110
        ],

        "customer_name": [
            "John","Alice","Bob","David","Eva",
            "Sam","Rose","Kevin","Tom","Nancy"
        ],

        "city": [
            "Chennai",
            "Bangalore",
            "Hyderabad",
            "Mumbai",
            "Delhi",
            "Pune",
            "Kolkata",
            "Coimbatore",
            "Madurai",
            "Trichy"
        ]

    })

    return customers


def create_orders_dataset():
    """
    Create sample orders dataset.
    """

    orders = pd.DataFrame({

        "order_id": [
            1001,1002,1003,1004,1005,
            1006,1007,1008,1009,1010,
            1011,1012
        ],

        "customer_id": [
            101,
            101,
            102,
            103,
            103,
            105,
            106,
            110,
            111,
            112,
            103,
            108
        ],

        "amount": [
            1200,
            800,
            3500,
            900,
            1400,
            5000,
            2700,
            1800,
            2200,
            3000,
            1500,
            2500
        ]

    })

    return orders


def validate_row_counts(
    customers,
    orders
):
    """
    Display row counts before merge.
    """

    print("\n" + "=" * 60)
    print("ROW COUNT VALIDATION")
    print("=" * 60)

    print(
        f"Customers Table : {len(customers)}"
    )

    print(
        f"Orders Table : {len(orders)}"
    )


def perform_left_join(
    customers,
    orders
):
    """
    Perform explicit left join.
    """

    print("\n" + "=" * 60)
    print("LEFT JOIN")
    print("=" * 60)

    merged = pd.merge(

        customers,
        orders,

        on="customer_id",

        how="left"

    )

    print(
        f"Merged Rows : {len(merged)}"
    )

    print(
        f"Row Change : "
        f"{len(merged)-len(customers)}"
    )

    print("\nMerged Dataset")

    print(merged)

    return merged

def detect_unmatched_keys(
    customers,
    orders
):
    """
    Find customers with no orders
    and orders with no matching customer.
    """

    print("\n" + "=" * 60)
    print("UNMATCHED KEY VALIDATION")
    print("=" * 60)

    unmatched_customers = customers[
        ~customers["customer_id"].isin(
            orders["customer_id"]
        )
    ]

    unmatched_orders = orders[
        ~orders["customer_id"].isin(
            customers["customer_id"]
        )
    ]

    print(
        f"Customers without Orders : "
        f"{len(unmatched_customers)}"
    )

    print(
        f"Orphaned Orders : "
        f"{len(unmatched_orders)}"
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    unmatched_customers.to_csv(
        "output/unmatched_customers.csv",
        index=False
    )

    unmatched_orders.to_csv(
        "output/unmatched_orders.csv",
        index=False
    )

    return (
        unmatched_customers,
        unmatched_orders
    )


def compare_join_types(
    customers,
    orders
):
    """
    Compare Inner, Left and Outer joins.
    """

    print("\n" + "=" * 60)
    print("JOIN TYPE COMPARISON")
    print("=" * 60)

    inner = pd.merge(
        customers,
        orders,
        on="customer_id",
        how="inner"
    )

    left = pd.merge(
        customers,
        orders,
        on="customer_id",
        how="left"
    )

    outer = pd.merge(
        customers,
        orders,
        on="customer_id",
        how="outer"
    )

    print(f"Inner Join Rows : {len(inner)}")
    print(f"Left Join Rows : {len(left)}")
    print(f"Outer Join Rows : {len(outer)}")

    return inner, left, outer


def validate_duplicates(
    merged
):
    """
    Validate duplicate customer IDs
    created due to multiple orders.
    """

    print("\n" + "=" * 60)
    print("DUPLICATE VALIDATION")
    print("=" * 60)

    print("\nColumns after Merge")

    print(list(merged.columns))

    key_counts = (
        merged["customer_id"]
        .value_counts()
    )

    print("\nOrders per Customer")

    print(key_counts)

    print(
        f"\nMaximum Orders "
        f"by One Customer : "
        f"{key_counts.max()}"
    )

    duplicate_customers = key_counts[
        key_counts > 1
    ]

    print("\nCustomers with Multiple Orders")

    print(duplicate_customers)

    return duplicate_customers

def create_join_report(
    customers,
    orders,
    merged,
    unmatched_customers,
    unmatched_orders
):
    """
    Create a structured join validation report.
    """

    print("\n" + "=" * 60)
    print("JOIN VALIDATION REPORT")
    print("=" * 60)

    join_report = {

        "join_type": "left",

        "left_table": "customers",

        "right_table": "orders",

        "join_key": "customer_id",

        "left_rows": len(customers),

        "right_rows": len(orders),

        "result_rows": len(merged),

        "unmatched_left": len(unmatched_customers),

        "unmatched_right": len(unmatched_orders),

        "reasoning":
        "Left join preserves all customers while adding order information where available."

    }

    print(json.dumps(join_report, indent=4))

    report_df = pd.DataFrame(
        [join_report]
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    report_df.to_csv(
        "output/join_validation_report.csv",
        index=False
    )

    with open(
        "output/join_validation_report.json",
        "w"
    ) as file:

        json.dump(
            join_report,
            file,
            indent=4
        )

    return report_df


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("=" * 70)
    print("MULTI-SOURCE MERGING & JOIN VALIDATION")
    print("=" * 70)

    customers = create_customer_dataset()

    orders = create_orders_dataset()

    validate_row_counts(
        customers,
        orders
    )

    merged = perform_left_join(
        customers,
        orders
    )

    unmatched_customers, unmatched_orders = detect_unmatched_keys(
        customers,
        orders
    )

    compare_join_types(
        customers,
        orders
    )

    validate_duplicates(
        merged
    )

    create_join_report(
        customers,
        orders,
        merged,
        unmatched_customers,
        unmatched_orders
    )

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(
        f"Customers : {len(customers)}"
    )

    print(
        f"Orders : {len(orders)}"
    )

    print(
        f"Merged Rows : {len(merged)}"
    )

    print(
        f"Customers without Orders : "
        f"{len(unmatched_customers)}"
    )

    print(
        f"Orphaned Orders : "
        f"{len(unmatched_orders)}"
    )

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()