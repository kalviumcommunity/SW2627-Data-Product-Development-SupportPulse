import pandas as pd
import numpy as np
import os


def create_sample_dataset():
    """
    Create sample customer transaction dataset.
    """

    data = {

        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110
        ],

        "total_transactions": [
            12,35,5,50,18,
            8,27,40,15,60
        ],

        "days_as_customer": [
            365,
            90,
            180,
            120,
            450,
            30,
            600,
            90,
            300,
            60
        ],

        "total_spent": [
            25000,90000,7500,180000,45000,
            12000,68000,150000,30000,250000
        ],

        "days_since_last_purchase": [
            10,45,90,5,20,
            60,15,8,35,2
        ],

        "purchase_count": [
            12,35,5,50,18,
            8,27,40,15,60
        ]

    }

    return pd.DataFrame(data)


def compute_ratio_features(df):
    """
    Compute business ratio features.
    """

    print("\n" + "=" * 60)
    print("RATIO FEATURE ENGINEERING")
    print("=" * 60)

    df["transactions_per_month"] = (
        df["total_transactions"] /
        (df["days_as_customer"] / 30)
    )

    df["avg_spend_per_transaction"] = (
        df["total_spent"] /
        df["total_transactions"]
    )

    df["lifetime_value_per_month"] = (
        df["total_spent"] /
        (df["days_as_customer"] / 30)
    )

    print("\nRatio Features")

    print(df[[
        "transactions_per_month",
        "avg_spend_per_transaction",
        "lifetime_value_per_month"
    ]])

    print("\nStatistics")

    print(df[[
        "transactions_per_month",
        "avg_spend_per_transaction",
        "lifetime_value_per_month"
    ]].describe())

    return df

def create_engagement_tiers(df):
    """
    Create engagement tiers using
    equal-width bins.
    """

    print("\n" + "=" * 60)
    print("ENGAGEMENT TIER")
    print("=" * 60)

    df["engagement_tier"] = pd.cut(

        df["transactions_per_month"],

        bins=[0, 2, 10, float("inf")],

        labels=[
            "Low",
            "Medium",
            "High"
        ],

        include_lowest=True

    )

    print(df["engagement_tier"].value_counts())

    return df


def create_spend_quartiles(df):
    """
    Create spend quartiles using
    equal-frequency bins.
    """

    print("\n" + "=" * 60)
    print("SPEND QUARTILES")
    print("=" * 60)

    df["spend_quartile"] = pd.qcut(

        df["total_spent"],

        q=4,

        labels=[
            "Q1",
            "Q2",
            "Q3",
            "Q4"
        ]

    )

    print(df["spend_quartile"].value_counts())

    return df


def create_rfm_score(df):
    """
    Create RFM composite score.
    """

    print("\n" + "=" * 60)
    print("RFM SCORE")
    print("=" * 60)

    df["recency_score"] = pd.qcut(

        df["days_since_last_purchase"],

        q=5,

        labels=[
            5,
            4,
            3,
            2,
            1
        ]

    )

    df["frequency_score"] = pd.qcut(

        df["purchase_count"],

        q=5,

        labels=[
            1,
            2,
            3,
            4,
            5
        ]

    )

    df["monetary_score"] = pd.qcut(

        df["total_spent"],

        q=5,

        labels=[
            1,
            2,
            3,
            4,
            5
        ]

    )

    df["rfm_score"] = (

        df["recency_score"].astype(int)

        +

        df["frequency_score"].astype(int)

        +

        df["monetary_score"].astype(int)

    )

    print(df[[
        "recency_score",
        "frequency_score",
        "monetary_score",
        "rfm_score"
    ]])

    return df
def validate_features(df):
    """
    Validate engineered features.
    """

    print("\n" + "=" * 60)
    print("FEATURE VALIDATION")
    print("=" * 60)

    print("\nEngagement Tier Distribution")

    print(
        df["engagement_tier"]
        .value_counts()
    )

    print(
        f"\nRFM Score Range : "
        f"{df['rfm_score'].min()} - "
        f"{df['rfm_score'].max()}"
    )

    print("\nMissing Values")

    print(

        df[
            [
                "engagement_tier",
                "spend_quartile",
                "rfm_score"
            ]
        ].isna().sum()

    )

    return df


def save_processed_data(df):
    """
    Save engineered dataset.
    """

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df.to_csv(
        "data/processed/feature_engineered_data.csv",
        index=False
    )

    print(
        "\nFeature engineered dataset saved."
    )


def main():

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    print("=" * 70)
    print("FEATURE ENGINEERING PIPELINE")
    print("=" * 70)

    df = create_sample_dataset()

    df.to_csv(
        "data/raw/customer_transactions.csv",
        index=False
    )

    print("\nOriginal Dataset")

    print(df)

    # Task 1
    df = compute_ratio_features(df)

    # Task 2
    df = create_engagement_tiers(df)

    # Task 3
    df = create_spend_quartiles(df)

    # Task 4
    df = create_rfm_score(df)

    # Task 5
    df = validate_features(df)

    save_processed_data(df)

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(
        f"Total Records : {len(df)}"
    )

    print(
        f"Average Transactions/Month : "
        f"{df['transactions_per_month'].mean():.2f}"
    )

    print(
        f"Average Spend/Transaction : "
        f"{df['avg_spend_per_transaction'].mean():.2f}"
    )

    print(
        f"Highest RFM Score : "
        f"{df['rfm_score'].max()}"
    )

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()