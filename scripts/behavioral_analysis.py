import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def create_sample_dataset():
    """
    Create a sample customer dataset
    for behavioural analysis.
    """

    data = {

        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110,
            111,112,113,114,115
        ],

        "customer_type": [

            "Enterprise",
            "Enterprise",
            "Enterprise",
            "SMB",
            "SMB",
            "SMB",
            "Startup",
            "Startup",
            "Startup",
            "Startup",
            "Enterprise",
            "SMB",
            "Startup",
            "Enterprise",
            "SMB"

        ],

        "lifetime_value": [

            180000,
            220000,
            195000,
            12000,
            9000,
            15000,
            3000,
            4500,
            2500,
            5000,
            210000,
            11000,
            3500,
            205000,
            14000

        ],

        "support_tickets": [

            1,2,1,
            6,5,7,
            8,7,6,
            9,2,
            5,7,1,6

        ],

        "retention_days": [

            720,
            680,
            700,
            220,
            200,
            250,
            110,
            130,
            90,
            100,
            690,
            240,
            120,
            710,
            230

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


def compute_segment_metrics(df):
    """
    Compute behavioural metrics
    for each customer segment.
    """

    print("\n" + "=" * 65)
    print("SEGMENT METRICS")
    print("=" * 65)

    segment_metrics = (

        df

        .groupby("customer_type")

        .agg({

            "lifetime_value": "mean",

            "churn": "mean",

            "support_tickets": "mean",

            "retention_days": "mean",

            "customer_id": "count"

        })

    )

    segment_metrics.columns = [

        "avg_ltv",

        "churn_rate",

        "avg_tickets",

        "avg_retention",

        "count"

    ]

    print(segment_metrics)

    return segment_metrics
def create_summary_table(segment_metrics):
    """
    Create a formatted summary table
    with rankings.
    """

    print("\n" + "=" * 65)
    print("SEGMENT SUMMARY")
    print("=" * 65)

    segment_summary = segment_metrics.copy()

    segment_summary["ltv_rank"] = (
        segment_summary["avg_ltv"]
        .rank(
            ascending=False,
            method="dense"
        )
    )

    segment_summary["churn_rank"] = (
        segment_summary["churn_rate"]
        .rank(
            ascending=True,
            method="dense"
        )
    )

    display_summary = segment_summary.copy()

    display_summary["avg_ltv"] = (
        display_summary["avg_ltv"]
        .apply(lambda x: f"${x:,.0f}")
    )

    display_summary["churn_rate"] = (
        display_summary["churn_rate"]
        .apply(lambda x: f"{x:.1%}")
    )

    display_summary["avg_retention"] = (
        display_summary["avg_retention"]
        .apply(lambda x: f"{x:.0f} days")
    )

    print(

        display_summary[
            [
                "avg_ltv",
                "ltv_rank",
                "churn_rate",
                "churn_rank",
                "count"
            ]
        ]

    )

    return segment_summary


def create_heatmap(segment_metrics):
    """
    Create heatmap comparing
    behavioural metrics.
    """

    print("\n" + "=" * 65)
    print("SEGMENT HEATMAP")
    print("=" * 65)

    os.makedirs(
        "output",
        exist_ok=True
    )

    heatmap_data = segment_metrics[
        [
            "avg_ltv",
            "churn_rate",
            "avg_tickets"
        ]
    ].copy()

    plt.figure(figsize=(8, 5))

    sns.heatmap(

        heatmap_data,

        annot=True,

        fmt=".2f",

        cmap="RdYlGn",

        linewidths=0.5,

        cbar_kws={
            "label": "Metric Value"
        }

    )

    plt.title("Customer Segment Comparison")

    plt.tight_layout()

    plt.savefig(

        "output/segment_heatmap.png",

        dpi=300,

        bbox_inches="tight"

    )

    plt.close()

    print(
        "Heatmap saved successfully."
    )
def analyze_performance(segment_metrics):
    """
    Identify top and bottom
    performing customer segments.
    """

    print("\n" + "=" * 65)
    print("TOP & BOTTOM PERFORMER ANALYSIS")
    print("=" * 65)

    top_segment = segment_metrics["avg_ltv"].idxmax()
    top_value = segment_metrics.loc[top_segment, "avg_ltv"]

    high_churn = segment_metrics["churn_rate"].idxmax()
    high_churn_rate = segment_metrics.loc[high_churn, "churn_rate"]

    best_retention = segment_metrics["avg_retention"].idxmax()
    retention_days = segment_metrics.loc[
        best_retention,
        "avg_retention"
    ]

    insights = f"""
HIGHEST VALUE SEGMENT
---------------------
Segment : {top_segment}
Average LTV : ${top_value:,.0f}

HIGHEST CHURN SEGMENT
---------------------
Segment : {high_churn}
Churn Rate : {high_churn_rate:.1%}

BEST RETENTION SEGMENT
----------------------
Segment : {best_retention}
Average Retention : {retention_days:.0f} days
"""

    print(insights)

    return insights


def generate_business_summary(segment_metrics):
    """
    Generate business recommendations
    for each customer segment.
    """

    print("\n" + "=" * 65)
    print("BUSINESS INSIGHTS")
    print("=" * 65)

    os.makedirs(
        "output",
        exist_ok=True
    )

    summary = []

    for segment in segment_metrics.index:

        row = segment_metrics.loc[segment]

        if segment == "Enterprise":

            action = (
                "Highest customer value with low churn. "
                "Maintain premium support and strengthen "
                "long-term relationships."
            )

        elif segment == "SMB":

            action = (
                "Moderate customer value with higher churn. "
                "Improve onboarding, customer engagement, "
                "and retention programs."
            )

        else:

            action = (
                "Lowest customer value with frequent support "
                "requests. Invest in self-service resources "
                "and customer education."
            )

        summary.append({

            "Segment": segment,

            "Average LTV":
                f"${row['avg_ltv']:,.0f}",

            "Churn Rate":
                f"{row['churn_rate']:.1%}",

            "Average Tickets":
                f"{row['avg_tickets']:.1f}",

            "Average Retention":
                f"{row['avg_retention']:.0f} days",

            "Recommendation":
                action

        })

    business_summary = pd.DataFrame(summary)

    print(
        business_summary.to_string(index=False)
    )

    business_summary.to_csv(

        "output/business_summary.csv",

        index=False

    )

    with open(

        "output/business_summary.txt",

        "w",

        encoding="utf-8"

    ) as file:

        file.write(
            business_summary.to_string(index=False)
        )

    print(
        "\nBusiness summary saved successfully."
    )

    return business_summary


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("=" * 70)
    print("BEHAVIOURAL ANALYSIS & USER SEGMENTATION")
    print("=" * 70)

    df = create_sample_dataset()

    print("\nSample Dataset\n")

    print(df)

    segment_metrics = compute_segment_metrics(df)

    segment_metrics = create_summary_table(
        segment_metrics
    )

    create_heatmap(segment_metrics)

    analyze_performance(segment_metrics)

    business_summary = generate_business_summary(
        segment_metrics
    )

    print("\n" + "=" * 65)
    print("TESTING")
    print("=" * 65)

    print(
        f"Total Customers : {len(df)}"
    )

    print(
        f"Customer Segments : "
        f"{df['customer_type'].nunique()}"
    )

    print(
        f"Business Recommendations : "
        f"{len(business_summary)}"
    )

    print(
        "\nPipeline Completed Successfully."
    )


if __name__ == "__main__":
    main()