import os
import pandas as pd
import numpy as np

from kpis.kpi_functions import *
from kpis.kpi_validation import validate_kpis


def create_sample_dataset():
    """
    Create sample transaction data.
    """

    np.random.seed(42)

    customers = 100

    df = pd.DataFrame({

        "customer_id":
            np.arange(1, customers + 1),

        "customer_type":
            np.random.choice(

                [
                    "Enterprise",
                    "SMB",
                    "Startup"
                ],

                customers

            ),

        "product":
            np.random.choice(

                [
                    "Basic",
                    "Pro",
                    "Premium"
                ],

                customers

            ),

        "amount":
            np.random.randint(

                50,
                300,
                customers

            ),

        "payment_status":
            np.random.choice(

                [
                    "Success",
                    "Failed"
                ],

                customers,

                p=[0.96, 0.04]

            ),

        "transaction_date":
            pd.to_datetime("today")
            -
            pd.to_timedelta(

                np.random.randint(
                    0,
                    60,
                    customers
                ),

                unit="D"

            )

    })

    return df


def kpi_decomposition(df):
    """
    Show KPI decomposition.
    """

    print("\n" + "=" * 65)
    print("KPI DECOMPOSITION")
    print("=" * 65)

    total_revenue = df["amount"].sum()

    revenue_by_segment = (

        df

        .groupby("customer_type")

        ["amount"]

        .sum()

    )

    revenue_by_product = (

        df

        .groupby("product")

        ["amount"]

        .sum()

    )

    print(

        f"\nTotal Revenue : "

        f"${total_revenue:,.2f}"

    )

    print("\nRevenue by Segment")

    print(revenue_by_segment)

    print("\nRevenue by Product")

    print(revenue_by_product)

    os.makedirs(

        "output",

        exist_ok=True

    )

    with open(

        "output/kpi_decomposition.txt",

        "w",

        encoding="utf-8"

    ) as file:

        file.write(

            f"Total Revenue\n"

            f"${total_revenue:,.2f}\n\n"

        )

        file.write(

            "Revenue by Segment\n"

        )

        file.write(

            revenue_by_segment.to_string()

        )

        file.write("\n\n")

        file.write(

            "Revenue by Product\n"

        )

        file.write(

            revenue_by_product.to_string()

        )

    print(

        "\nDecomposition report saved."
    )


def main():

    print("=" * 70)
    print("KPI DEFINITION & BUSINESS METRIC DESIGN")
    print("=" * 70)

    df = create_sample_dataset()

    print("\nSample Dataset\n")

    print(df.head())

    print("\n")

    validate_kpis(df)

    kpi_decomposition(df)

    print("\n" + "=" * 65)
    print("TESTING")
    print("=" * 65)

    print(

        f"Transactions : {len(df)}"

    )

    print(

        f"Customers : "

        f"{df['customer_id'].nunique()}"

    )

    print(

        f"Customer Types : "

        f"{df['customer_type'].nunique()}"

    )

    print(

        "\nPipeline Completed Successfully."

    )


if __name__ == "__main__":
    main()