import pandas as pd
import numpy as np
from scipy import stats
import os


def create_sample_dataset():
    """
    Create sample customer revenue dataset
    with intentional outliers.
    """

    data = {
        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110,
            111,112,113,114,115
        ],

        "age": [
            22,35,41,28,31,
            45,38,29,52,40,
            27,33,36,150,25
        ],

        "revenue": [
            250,320,400,500,450,
            380,420,510,460,390,
            430,520,470,5000,410
        ]
    }

    return pd.DataFrame(data)


def detect_zscore_outliers(df):
    """
    Detect outliers using Z-Score.
    """

    print("\n" + "=" * 60)
    print("Z-SCORE OUTLIER DETECTION")
    print("=" * 60)

    df["revenue_zscore"] = np.abs(
        stats.zscore(df["revenue"])
    )

    z_outliers = df[
        df["revenue_zscore"] > 3
    ]

    print("\nRevenue Z-Scores")
    print(df[
        [
            "customer_id",
            "revenue",
            "revenue_zscore"
        ]
    ])

    print("\nDetected Z-Score Outliers")
    print(z_outliers)

    print(
        f"\nTotal Z-Score Outliers : {len(z_outliers)}"
    )

    return df


def detect_iqr_outliers(df):
    """
    Detect outliers using IQR.
    """

    print("\n" + "=" * 60)
    print("IQR OUTLIER DETECTION")
    print("=" * 60)

    Q1 = df["revenue"].quantile(0.25)
    Q3 = df["revenue"].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df["is_outlier_iqr"] = (
        (df["revenue"] < lower) |
        (df["revenue"] > upper)
    )

    print(f"Q1 : {Q1}")
    print(f"Q3 : {Q3}")
    print(f"IQR : {IQR}")

    print(f"Lower Bound : {lower}")
    print(f"Upper Bound : {upper}")

    print("\nIQR Outliers")

    print(
        df[
            df["is_outlier_iqr"]
        ]
    )

    return df, lower, upper

def cap_outliers(df, lower, upper):
    """
    Cap revenue outliers using IQR boundaries.
    """

    print("\n" + "=" * 60)
    print("OUTLIER CAPPING")
    print("=" * 60)

    df["revenue_capped"] = df["revenue"].clip(
        lower=lower,
        upper=upper
    )

    print("\nBefore Capping")
    print(
        f"Minimum Revenue : {df['revenue'].min()}"
    )

    print(
        f"Maximum Revenue : {df['revenue'].max()}"
    )

    print("\nAfter Capping")
    print(
        f"Minimum Revenue : {df['revenue_capped'].min()}"
    )

    print(
        f"Maximum Revenue : {df['revenue_capped'].max()}"
    )

    return df


def flag_outliers(df):
    """
    Combine Z-score and IQR methods
    to flag anomalies.
    """

    print("\n" + "=" * 60)
    print("OUTLIER FLAGGING")
    print("=" * 60)

    df["is_outlier"] = (
        df["is_outlier_iqr"] |
        (df["revenue_zscore"] > 3)
    )

    normal = df[
        ~df["is_outlier"]
    ]

    anomalies = df[
        df["is_outlier"]
    ]

    print(f"Normal Records : {len(normal)}")
    print(f"Outlier Records : {len(anomalies)}")

    print("\nDetected Outliers")
    print(
        anomalies[
            [
                "customer_id",
                "age",
                "revenue",
                "revenue_capped",
                "is_outlier"
            ]
        ]
    )

    return df, normal, anomalies


def compare_before_after(df):
    """
    Compare statistics before and
    after capping.
    """

    print("\n" + "=" * 60)
    print("STATISTICAL COMPARISON")
    print("=" * 60)

    comparison = pd.DataFrame({

        "Original": [
            df["revenue"].min(),
            df["revenue"].max(),
            df["revenue"].mean(),
            df["revenue"].median(),
            df["revenue"].std()
        ],

        "Capped": [
            df["revenue_capped"].min(),
            df["revenue_capped"].max(),
            df["revenue_capped"].mean(),
            df["revenue_capped"].median(),
            df["revenue_capped"].std()
        ]

    },

    index=[
        "Minimum",
        "Maximum",
        "Mean",
        "Median",
        "Standard Deviation"
    ])

    print(comparison)

    os.makedirs(
        "output",
        exist_ok=True
    )

    comparison.to_csv(
        "output/statistical_comparison.csv"
    )

    return comparison


def save_processed_dataset(df):
    """
    Save cleaned dataset.
    """

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df.to_csv(
        "data/processed/outlier_processed.csv",
        index=False
    )

    print("\nProcessed dataset saved.")

def create_cleaning_log(df, lower, upper):
    """
    Create cleaning log documenting
    all outlier handling decisions.
    """

    print("\n" + "=" * 60)
    print("CLEANING LOG")
    print("=" * 60)

    cleaning_log = [{
        "column": "revenue",
        "method": "IQR",
        "action": "Cap",
        "threshold_lower": lower,
        "threshold_upper": upper,
        "affected_rows": int(df["is_outlier_iqr"].sum()),
        "date": pd.Timestamp.now(),
        "reason": "Extreme revenue values capped to reduce skew."
    }]

    log_df = pd.DataFrame(cleaning_log)

    os.makedirs("output", exist_ok=True)

    log_df.to_csv(
        "output/cleaning_log.csv",
        index=False
    )

    print(log_df)

    return log_df


def main():

    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("=" * 70)
    print("OUTLIER DETECTION PIPELINE")
    print("=" * 70)

    df = create_sample_dataset()

    df.to_csv(
        "data/raw/customer_revenue.csv",
        index=False
    )

    print("\nOriginal Dataset")
    print(df)

    # Task 1
    df = detect_zscore_outliers(df)

    # Task 2
    df, lower, upper = detect_iqr_outliers(df)

    # Task 3
    df = cap_outliers(df, lower, upper)

    # Task 4
    df, normal, anomalies = flag_outliers(df)

    compare_before_after(df)

    save_processed_dataset(df)

    # Task 5
    create_cleaning_log(df, lower, upper)

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(
        f"Original Maximum Revenue : {df['revenue'].max()}"
    )

    print(
        f"Capped Maximum Revenue : {df['revenue_capped'].max()}"
    )

    print(
        f"Total Z-Score Outliers : {(df['revenue_zscore'] > 3).sum()}"
    )

    print(
        f"Total IQR Outliers : {df['is_outlier_iqr'].sum()}"
    )

    print(
        f"Total Flagged Outliers : {df['is_outlier'].sum()}"
    )

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()