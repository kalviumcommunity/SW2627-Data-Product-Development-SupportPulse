import pandas as pd
import numpy as np
import os


def create_sample_dataset():
    """
    Create sample transaction dataset.
    """

    data = {
        "customer_id": [
            101,101,102,103,104,
            105,106,107,108,109
        ],

        "transaction_date": [
            "2025-01-15 14:30:45",
            "2025-01-18 09:20:10",
            "2025-01-20 16:45:30",
            "2025-02-02 11:15:00",
            "2025-02-10 20:30:40",
            "2025-02-18 08:10:00",
            "2025-03-01 13:25:55",
            "2025-03-10 18:00:00",
            "2025-03-15 10:40:35",
            "2025-03-28 21:50:15"
        ],

        "amount": [
            250,400,300,450,500,
            200,350,600,700,550
        ]
    }

    return pd.DataFrame(data)


def parse_datetime(df):
    """
    Convert timestamp strings to datetime.
    """

    print("\n" + "="*60)
    print("DATETIME PARSING")
    print("="*60)

    format_string = "%Y-%m-%d %H:%M:%S"

    print("Using format:", format_string)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        format=format_string
    )

    print("\nDatatype")
    print(df["transaction_date"].dtype)

    return df


def extract_datetime_features(df):
    """
    Extract useful datetime features.
    """

    print("\n" + "="*60)
    print("FEATURE EXTRACTION")
    print("="*60)

    df["day_of_week"] = (
        df["transaction_date"]
        .dt.day_name()
    )

    df["hour"] = (
        df["transaction_date"]
        .dt.hour
    )

    df["week_num"] = (
        df["transaction_date"]
        .dt.isocalendar()
        .week
    )

    df["month"] = (
        df["transaction_date"]
        .dt.month
    )

    df["quarter"] = (
        df["transaction_date"]
        .dt.quarter
    )

    print("\nExtracted Columns")
    print(
        df[
            [
                "transaction_date",
                "day_of_week",
                "hour",
                "week_num",
                "month",
                "quarter"
            ]
        ]
    )

    return df


def show_hour_distribution(df):
    """
    Display hourly transaction volume.
    """

    hourly_volume = df.groupby("hour").size()

    print("\nHourly Distribution")
    print(hourly_volume)

    os.makedirs("output", exist_ok=True)

    hourly_volume.to_csv("output/hour_distribution.csv")

    return hourly_volume

def compute_days_since_last_purchase(df):
    """
    Compute days since customer's last purchase.
    """

    print("\n" + "=" * 60)
    print("DAYS SINCE LAST PURCHASE")
    print("=" * 60)

    today = pd.Timestamp.now()

    customer_last_purchase = (
        df.groupby("customer_id")["transaction_date"]
        .transform("max")
    )

    df["days_since_last_purchase"] = (
        today - customer_last_purchase
    ).dt.days

    print(df[
        [
            "customer_id",
            "transaction_date",
            "days_since_last_purchase"
        ]
    ])

    print("\nRecency Statistics")
    print(df["days_since_last_purchase"].describe())

    inactive_customers = df[
        df["days_since_last_purchase"] > 30
    ]

    print("\nCustomers inactive for more than 30 days")
    print(inactive_customers)

    return df


def weekly_resampling(df):
    """
    Weekly aggregation using resample.
    """

    print("\n" + "=" * 60)
    print("WEEKLY RESAMPLING")
    print("=" * 60)

    df_ts = df.set_index("transaction_date")

    weekly_metrics = (
        df_ts["amount"]
        .resample("W")
        .agg(["sum", "count", "mean"])
    )

    print(weekly_metrics)

    os.makedirs("output", exist_ok=True)

    weekly_metrics.to_csv(
        "output/weekly_revenue.csv"
    )

    return weekly_metrics


def day_hour_aggregation(df):
    """
    Aggregate transactions by day and hour.
    """

    print("\n" + "=" * 60)
    print("DAY × HOUR AGGREGATION")
    print("=" * 60)

    aggregation = (
        df.groupby(
            ["day_of_week", "hour"]
        )
        .agg(
            {
                "amount": [
                    "sum",
                    "count",
                    "mean"
                ]
            }
        )
    )

    print(aggregation)

    return aggregation


def create_pivot_table(df):
    """
    Create pivot table showing
    hour vs day of week.
    """

    print("\n" + "=" * 60)
    print("PIVOT TABLE")
    print("=" * 60)

    pivot = pd.pivot_table(
        df,
        values="amount",
        index="hour",
        columns="day_of_week",
        aggfunc="sum",
        fill_value=0
    )

    print(pivot)

    pivot.to_csv(
        "output/day_hour_pivot.csv"
    )

    return pivot


def identify_peak_activity(df):
    """
    Identify busiest hour.
    """

    peak = (
        df.groupby("hour")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n" + "=" * 60)
    print("PEAK ACTIVITY")
    print("=" * 60)

    print(peak)

    busiest_hour = peak.idxmax()

    print(
        f"\nPeak Activity Hour : {busiest_hour}:00"
    )

    return busiest_hour

def main():

    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("=" * 70)
    print("DATE & TIME FEATURE ENGINEERING PIPELINE")
    print("=" * 70)

    df = create_sample_dataset()

    df.to_csv(
        "data/raw/transactions.csv",
        index=False
    )

    print("\nOriginal Dataset")
    print(df)

    df = parse_datetime(df)

    df = extract_datetime_features(df)

    show_hour_distribution(df)

    weekly_resampling(df)

    df = compute_days_since_last_purchase(df)

    day_hour_aggregation(df)

    create_pivot_table(df)

    identify_peak_activity(df)

    df.to_csv(
        "data/processed/datetime_features.csv",
        index=False
    )

    # ------------------------
    # TESTING
    # ------------------------

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(f"Minimum Date : {df['transaction_date'].min()}")
    print(f"Maximum Date : {df['transaction_date'].max()}")

    print(
        f"Days Covered : "
        f"{(df['transaction_date'].max() - df['transaction_date'].min()).days}"
    )

    print(
        f"Hours Present : "
        f"{sorted(df['hour'].unique())}"
    )

    print(
        f"Weeks Present : "
        f"{df['week_num'].nunique()}"
    )

    print(
        f"Minimum Days Since Purchase : "
        f"{df['days_since_last_purchase'].min()}"
    )

    print(
        f"Maximum Days Since Purchase : "
        f"{df['days_since_last_purchase'].max()}"
    )

    print("\n✓ Processed dataset saved successfully.")


if __name__ == "__main__":
    main()