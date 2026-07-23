import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os


def create_sample_dataset():
    """
    Create sample revenue dataset with
    intentionally skewed values.
    """

    data = {

        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110,
            111,112,113,114,115
        ],

        "revenue": [
            5000,
            7500,
            8500,
            9500,
            12000,
            15000,
            18000,
            22000,
            28000,
            35000,
            75000,
            120000,
            180000,
            300000,
            500000
        ]

    }

    return pd.DataFrame(data)


def plot_distributions(df):
    """
    Plot Histogram and KDE
    for revenue distribution.
    """

    print("\n" + "=" * 60)
    print("DISTRIBUTION PLOTS")
    print("=" * 60)

    os.makedirs(
        "output",
        exist_ok=True
    )

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(14,5)
    )

    # Histogram
    axes[0].hist(
        df["revenue"],
        bins=10,
        edgecolor="black"
    )

    axes[0].set_title(
        "Revenue Distribution (Histogram)"
    )

    axes[0].set_xlabel("Revenue")

    axes[0].set_ylabel("Frequency")

    # KDE Plot
    df["revenue"].plot(
        kind="density",
        ax=axes[1]
    )

    axes[1].set_title(
        "Revenue Distribution (KDE)"
    )

    axes[1].set_xlabel("Revenue")

    plt.tight_layout()

    plt.savefig(
        "output/revenue_distribution.png"
    )

    plt.close()

    print(
        "Distribution plot saved to "
        "output/revenue_distribution.png"
    )

    return df
def analyze_distribution(df):
    """
    Compute skewness and kurtosis
    for the revenue distribution.
    """

    print("\n" + "=" * 60)
    print("DISTRIBUTION STATISTICS")
    print("=" * 60)

    skewness = stats.skew(df["revenue"])

    kurtosis = stats.kurtosis(df["revenue"])

    print(f"Skewness : {skewness:.2f}")

    print(f"Kurtosis : {kurtosis:.2f}")

    if abs(skewness) > 1:

        print(
            "Highly skewed distribution - "
            "Median is more reliable than Mean."
        )

    else:

        print(
            "Distribution is approximately symmetric."
        )

    if kurtosis > 3:

        print(
            "Heavy tails detected - "
            "Expect extreme outliers."
        )

    else:

        print(
            "No significant heavy tails detected."
        )

    return skewness, kurtosis


def identify_patterns(df):
    """
    Identify abnormal distribution
    patterns using descriptive
    statistics and percentiles.
    """

    print("\n" + "=" * 60)
    print("ABNORMAL PATTERN ANALYSIS")
    print("=" * 60)

    print("\nSummary Statistics")

    print(df["revenue"].describe())

    percentiles = df["revenue"].quantile(

        [
            0.25,
            0.50,
            0.75,
            0.90,
            0.95,
            0.99
        ]

    )

    print("\nPercentiles")

    print(percentiles)

    gap = (

        percentiles.loc[0.90]

        -

        percentiles.loc[0.75]

    )

    print(f"\nGap (75th → 90th Percentile): {gap:.2f}")

    if gap > percentiles.loc[0.75] * 0.5:

        print(
            "Possible hidden customer segments "
            "or bimodal behaviour detected."
        )

    else:

        print(
            "Distribution appears relatively continuous."
        )

    return percentiles
def compare_segments(df):
    """
    Compare high-value and
    low-value customer
    distributions.
    """

    print("\n" + "=" * 60)
    print("SEGMENT COMPARISON")
    print("=" * 60)

    high_value = df[
        df["revenue"] >
        df["revenue"].quantile(0.75)
    ]

    low_value = df[
        df["revenue"] <
        df["revenue"].quantile(0.25)
    ]

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(14,5)
    )

    axes[0].hist(
        high_value["revenue"],
        bins=5,
        alpha=0.7,
        label="High Value"
    )

    axes[0].hist(
        low_value["revenue"],
        bins=5,
        alpha=0.7,
        label="Low Value"
    )

    axes[0].set_title(
        "Revenue: High vs Low Value Customers"
    )

    axes[0].legend()

    axes[1].boxplot(
    [
        low_value["revenue"],
        high_value["revenue"]
    ],
    tick_labels=[
        "Low",
        "High"
    ]
)

    axes[1].set_title(
        "Revenue Comparison"
    )

    plt.tight_layout()

    plt.savefig(
        "output/revenue_segments.png"
    )

    plt.close()

    print(
        f"High-value Mean   : {high_value['revenue'].mean():.2f}"
    )

    print(
        f"High-value Median : {high_value['revenue'].median():.2f}"
    )

    print(
        f"Low-value Mean    : {low_value['revenue'].mean():.2f}"
    )

    print(
        f"Low-value Median  : {low_value['revenue'].median():.2f}"
    )

    print(
        "\nSegment comparison plot saved to "
        "output/revenue_segments.png"
    )


def business_interpretation(df, skewness, kurtosis):
    """
    Generate business
    interpretation report.
    """

    print("\n" + "=" * 60)
    print("BUSINESS INTERPRETATION")
    print("=" * 60)

    interpretation = f"""
Revenue Distribution Analysis

Skewness : {skewness:.2f}
=> {"Highly Right Skewed" if skewness > 1 else "Moderately Distributed"}

Mean Revenue : {df['revenue'].mean():.2f}

Median Revenue : {df['revenue'].median():.2f}

Interpretation:
{"Most customers generate low revenue while a small number of enterprise customers contribute very high revenue." if skewness > 1 else "Revenue is fairly balanced among customers."}

Kurtosis : {kurtosis:.2f}

=> {"Heavy Tails (Outliers Present)" if kurtosis > 3 else "Normal Distribution"}

Maximum Revenue : {df['revenue'].max():.2f}

99th Percentile : {df['revenue'].quantile(0.99):.2f}

Business Action:
{"Segment customers into Small, Medium and Enterprise groups for targeted marketing and pricing strategies." if skewness > 1 else "Uniform customer strategy is sufficient."}
"""

    print(interpretation)

    with open(
        "output/business_interpretation.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(interpretation)

    print(
        "Business interpretation saved successfully."
    )


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("=" * 70)
    print("DISTRIBUTION ANALYSIS FOR BUSINESS TRENDS")
    print("=" * 70)

    df = create_sample_dataset()

    print("\nSample Dataset")

    print(df)

    # Task 1
    plot_distributions(df)

    # Task 2
    skewness, kurtosis = analyze_distribution(df)

    # Task 3
    identify_patterns(df)

    # Task 4
    compare_segments(df)

    # Task 5
    business_interpretation(
        df,
        skewness,
        kurtosis
    )

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(f"Total Customers : {len(df)}")

    print(f"Maximum Revenue : {df['revenue'].max()}")

    print(f"Minimum Revenue : {df['revenue'].min()}")

    print(f"Average Revenue : {df['revenue'].mean():.2f}")

    print(f"Median Revenue : {df['revenue'].median():.2f}")

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()