import pandas as pd
import numpy as np
import os


def create_sample_dataset():
    """
    Create sample customer dataset
    for GroupBy analysis.
    """

    data = {

        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110,
            111,112,113,114,115
        ],

        "customer_type": [
            "Enterprise","Enterprise","Enterprise",
            "SMB","SMB","SMB",
            "Startup","Startup","Startup",
            "Startup","Enterprise",
            "SMB","Startup","Enterprise","SMB"
        ],

        "product": [
            "CRM","Analytics","CRM",
            "CRM","Support","Analytics",
            "Support","CRM","Analytics",
            "Support","Analytics",
            "CRM","Support","CRM","Analytics"
        ],

        "revenue": [
            250000,
            180000,
            220000,
            80000,
            65000,
            70000,
            35000,
            30000,
            28000,
            25000,
            300000,
            75000,
            40000,
            275000,
            60000
        ],

        "support_tickets": [
            1,2,1,
            5,6,4,
            7,8,6,
            7,2,
            5,8,1,6
        ],

        "churn": [
            0,0,0,
            1,0,1,
            1,0,1,
            1,0,
            1,1,0,0
        ]

    }

    return pd.DataFrame(data)


def segment_aggregation(df):
    """
    Perform single-level GroupBy
    with multiple aggregations.
    """

    print("\n" + "=" * 60)
    print("SEGMENT METRICS")
    print("=" * 60)

    segment_metrics = df.groupby(
        "customer_type"
    ).agg({

        "churn": "mean",

        "revenue": "sum",

        "customer_id": "count",

        "support_tickets": "mean"

    })

    segment_metrics.columns = [

        "churn_rate",

        "total_revenue",

        "customer_count",

        "avg_support_tickets"

    ]

    print(segment_metrics)

    return segment_metrics
def multi_level_groupby(df):
    """
    Perform multi-level GroupBy
    using customer_type and product.
    """

    print("\n" + "=" * 60)
    print("MULTI-LEVEL GROUPBY")
    print("=" * 60)

    product_segment = df.groupby(
        ["customer_type", "product"]
    ).agg({

        "revenue": "sum",

        "customer_id": "count"

    })

    product_segment.columns = [

        "total_revenue",

        "customer_count"

    ]

    print("\nGrouped Result\n")

    print(product_segment)

    print("\nPivot View\n")

    product_segment_pivot = product_segment.unstack()

    print(product_segment_pivot)

    return product_segment


def create_pivot_table(df):
    """
    Create pivot table
    showing revenue by
    customer type and product.
    """

    print("\n" + "=" * 60)
    print("PIVOT TABLE")
    print("=" * 60)

    pivot = pd.pivot_table(

        df,

        values="revenue",

        index="customer_type",

        columns="product",

        aggfunc="sum",

        fill_value=0

    )

    print(pivot)

    return pivot


def rank_segments(segment_metrics):
    """
    Rank customer segments
    based on churn rate and
    revenue contribution.
    """

    print("\n" + "=" * 60)
    print("SEGMENT RANKING")
    print("=" * 60)

    segment_metrics["churn_rank"] = (

        segment_metrics["churn_rate"]

        .rank(
            ascending=False,
            method="dense"
        )

    )

    total_revenue = (

        segment_metrics["total_revenue"]

        .sum()

    )

    segment_metrics["revenue_contribution"] = (

        segment_metrics["total_revenue"]

        /

        total_revenue

        *

        100

    )

    worst_first = (

        segment_metrics

        .sort_values(
            by="churn_rate",
            ascending=False
        )

    )

    print("\nSegments Ranked by Churn\n")

    print(worst_first)

    print("\nRevenue Contribution (%)\n")

    print(

        segment_metrics[
            [
                "revenue_contribution",
                "churn_rate"
            ]
        ]

    )

    return segment_metrics
def generate_segment_insights(segment_metrics):
    """
    Generate actionable business
    insights for each customer segment.
    """

    print("\n" + "=" * 60)
    print("SEGMENT INSIGHTS")
    print("=" * 60)

    os.makedirs(
        "output",
        exist_ok=True
    )

    insights = []

    for segment in segment_metrics.index:

        row = segment_metrics.loc[segment]

        insight = {

            "segment":
                segment,

            "customer_count":
                int(row["customer_count"]),

            "churn_rate":
                f"{row['churn_rate']:.1%}",

            "total_revenue":
                f"${row['total_revenue']:.0f}",

            "revenue_contribution":
                f"{row['revenue_contribution']:.1f}%",

            "action": ""

        }

        if row["churn_rate"] > 0.10:

            insight["action"] = (
                "HIGH PRIORITY: Churn above 10%. "
                "Investigate customer pain points."
            )

        elif row["churn_rate"] < 0.02:

            insight["action"] = (
                "Healthy segment. "
                "Maintain current service level."
            )

        else:

            insight["action"] = (
                "Monitor performance regularly."
            )

        insights.append(insight)

    insights_df = pd.DataFrame(insights)

    print(insights_df.to_string(index=False))

    insights_df.to_csv(
        "output/segment_insights.csv",
        index=False
    )

    print(
        "\nSegment insights saved successfully."
    )

    return insights_df


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("=" * 70)
    print("GROUPBY AGGREGATION & SEGMENT INSIGHTS")
    print("=" * 70)

    df = create_sample_dataset()

    print("\nSample Dataset\n")

    print(df)

    # Task 1
    segment_metrics = segment_aggregation(df)

    # Task 2
    multi_level_groupby(df)

    # Task 3
    create_pivot_table(df)

    # Task 4
    segment_metrics = rank_segments(segment_metrics)

    # Task 5
    insights_df = generate_segment_insights(
        segment_metrics
    )

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(
        f"Total Customers : {len(df)}"
    )

    print(
        f"Customer Segments : "
        f"{df['customer_type'].nunique()}"
    )

    print(
        f"Products : "
        f"{df['product'].nunique()}"
    )

    print(
        f"Generated Insights : "
        f"{len(insights_df)}"
    )

    print(
        "\nPipeline Completed Successfully."
    )


if __name__ == "__main__":
    main()