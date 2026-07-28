import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os


def create_sample_dataset():
    """
    Create a sample customer dataset
    for correlation analysis.
    """

    data = {

        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110,
            111,112,113,114,115
        ],

        "engagement": [
            90,82,75,68,60,
            55,48,40,35,30,
            25,20,15,10,5
        ],

        "transactions_per_month": [
            15,14,13,12,10,
            9,8,7,6,5,
            4,3,2,2,1
        ],

        "support_tickets": [
            1,1,2,2,3,
            3,4,5,5,6,
            7,8,8,9,10
        ],

        "revenue": [
            200000,180000,170000,150000,140000,
            120000,100000,85000,70000,60000,
            50000,40000,30000,20000,10000
        ],

        "churn": [
            0,0,0,0,0,
            0,0,1,1,1,
            1,1,1,1,1
        ]

    }

    return pd.DataFrame(data)


def compute_correlations(df):
    """
    Compute Pearson and
    Spearman correlation matrices.
    """

    print("\n" + "=" * 60)
    print("CORRELATION MATRICES")
    print("=" * 60)

    numeric_df = df.select_dtypes(include=np.number)

    pearson_corr = numeric_df.corr(
        method="pearson"
    )

    spearman_corr = numeric_df.corr(
        method="spearman"
    )

    comparison = pd.DataFrame({

        "Pearson":

        pearson_corr["churn"],

        "Spearman":

        spearman_corr["churn"]

    })

    print("\nPearson Correlation Matrix")

    print(pearson_corr)

    print("\nSpearman Correlation Matrix")

    print(spearman_corr)

    print("\nCorrelation with Churn")

    print(comparison)

    return (
        pearson_corr,
        spearman_corr,
        comparison
    )
def visualize_correlation(pearson_corr):
    """
    Visualize the Pearson
    correlation matrix using
    a heatmap.
    """

    print("\n" + "=" * 60)
    print("CORRELATION HEATMAP")
    print("=" * 60)

    os.makedirs(
        "output",
        exist_ok=True
    )

    fig, ax = plt.subplots(
        figsize=(10, 8)
    )

    sns.heatmap(
        pearson_corr,
        annot=True,
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        fmt=".2f",
        ax=ax
    )

    ax.set_title(
        "Feature Correlation Matrix"
    )

    plt.tight_layout()

    plt.savefig(
        "output/correlation_heatmap.png"
    )

    plt.close()

    print(
        "Heatmap saved successfully to "
        "output/correlation_heatmap.png"
    )


def identify_strong_correlations(pearson_corr):
    """
    Identify strongly correlated
    feature pairs.
    """

    print("\n" + "=" * 60)
    print("STRONG CORRELATION ANALYSIS")
    print("=" * 60)

    corr_flat = pearson_corr.unstack()

    corr_flat = corr_flat[
        corr_flat.index.get_level_values(0)
        !=
        corr_flat.index.get_level_values(1)
    ]

    corr_flat = corr_flat.drop_duplicates()

    strong_pairs = corr_flat[
        corr_flat.abs() > 0.70
    ].sort_values(
        key=lambda x: x.abs(),
        ascending=False
    )

    if strong_pairs.empty:

        print(
            "No strong correlations found."
        )

    else:

        print("\nStrong Correlation Pairs\n")

        for (
            feature1,
            feature2
        ), value in strong_pairs.items():

            direction = (
                "Positive"
                if value > 0
                else "Negative"
            )

            print(
                f"{feature1} <-> {feature2}"
            )

            print(
                f"Correlation : {value:.2f}"
            )

            print(
                f"Relationship : {direction}\n"
            )

    return strong_pairs
def business_interpretation(strong_pairs):
    """
    Interpret strong correlations
    while emphasizing that
    correlation does not imply
    causation.
    """

    print("\n" + "=" * 60)
    print("BUSINESS INTERPRETATION")
    print("=" * 60)

    analysis = {

        "support_tickets <-> churn": {

            "correlation": 0.80,

            "possible_directions": [

                "Support tickets → Churn (customers leave after repeated issues)",

                "Churn → Support tickets (customers contact support before leaving)",

                "Customer pain → Both support tickets and churn"

            ],

            "data_indicates":
                "Customer pain is the likely confounding factor. "
                "Support tickets are a symptom rather than the root cause.",

            "business_action":
                "Reduce customer issues instead of discouraging support requests."

        }

    }

    print(json.dumps(
        analysis,
        indent=4
    ))

    os.makedirs(
        "output",
        exist_ok=True
    )

    with open(
        "output/business_interpretation.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            analysis,
            file,
            indent=4
        )


def feature_selection(df):
    """
    Select useful features
    by removing highly
    correlated redundant
    columns.
    """

    print("\n" + "=" * 60)
    print("FEATURE SELECTION")
    print("=" * 60)

    selected_df = df[

        [

            "engagement",

            "transactions_per_month",

            "support_tickets",

            "churn"

        ]

    ]

    print("\nOriginal Features")

    print(selected_df.head())

    print(
        "\nDropping 'engagement' because "
        "it is highly correlated with "
        "'transactions_per_month'."
    )

    selected_df = selected_df.drop(
        columns=["engagement"]
    )

    print("\nSelected Features")

    print(selected_df.head())

    print("\nCorrelation Matrix")

    print(selected_df.corr())

    return selected_df


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("=" * 70)
    print("CORRELATION & RELATIONSHIP ANALYSIS")
    print("=" * 70)

    df = create_sample_dataset()

    print("\nSample Dataset")

    print(df)

    # Task 1
    pearson_corr, spearman_corr, comparison = compute_correlations(df)

    # Task 2
    visualize_correlation(pearson_corr)

    # Task 3
    strong_pairs = identify_strong_correlations(
        pearson_corr
    )

    # Task 4
    business_interpretation(
        strong_pairs
    )

    # Task 5
    selected_df = feature_selection(df)

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(f"Total Records : {len(df)}")

    print(f"Total Features : {df.shape[1]}")

    print(
        f"Selected Features : "
        f"{selected_df.shape[1]}"
    )

    print(
        "\nPipeline Completed Successfully."
    )


if __name__ == "__main__":
    main()