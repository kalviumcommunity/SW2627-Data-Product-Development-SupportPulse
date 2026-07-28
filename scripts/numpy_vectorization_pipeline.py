import pandas as pd
import numpy as np
import time
import os


def create_sample_dataset():
    """
    Create sample revenue dataset.
    """

    data = {

        "customer_id": [
            101,102,103,104,105,
            106,107,108,109,110
        ],

        "revenue": [
            25000,
            90000,
            7500,
            180000,
            45000,
            12000,
            68000,
            150000,
            30000,
            250000
        ]

    }

    return pd.DataFrame(data)


def normalize_with_loop(df):
    """
    Normalize revenue using
    Python loop.
    """

    print("\n" + "=" * 60)
    print("LOOP NORMALIZATION")
    print("=" * 60)

    revenue_min = df["revenue"].min()
    revenue_max = df["revenue"].max()

    normalized_loop = []

    for value in df["revenue"]:

        normalized_value = (

            value - revenue_min

        ) / (

            revenue_max - revenue_min

        )

        normalized_loop.append(
            normalized_value
        )

    df["normalized_loop"] = normalized_loop

    print(df[
        [
            "customer_id",
            "normalized_loop"
        ]
    ])

    return df


def normalize_with_numpy(df):
    """
    Normalize revenue using
    NumPy vectorization.
    """

    print("\n" + "=" * 60)
    print("NUMPY VECTORIZATION")
    print("=" * 60)

    revenue_array = df["revenue"].values

    normalized_np = (

        revenue_array - revenue_array.min()

    ) / (

        revenue_array.max() -
        revenue_array.min()

    )

    df["revenue_normalized"] = normalized_np

    print(df[
        [
            "customer_id",
            "revenue_normalized"
        ]
    ])

    return df   
def compute_zscore(df):
    """
    Compute Z-score normalization
    using NumPy.
    """

    print("\n" + "=" * 60)
    print("Z-SCORE NORMALIZATION")
    print("=" * 60)

    revenue_array = df["revenue"].values

    z_scores = (

        revenue_array - revenue_array.mean()

    ) / (

        revenue_array.std()

    )

    df["revenue_zscore"] = z_scores

    print(df[
        [
            "customer_id",
            "revenue_zscore"
        ]
    ])

    return df


def compute_rankings(df):
    """
    Rank customers by revenue
    using NumPy.
    """

    print("\n" + "=" * 60)
    print("REVENUE RANKING")
    print("=" * 60)

    revenue_array = df["revenue"].values

    rankings = np.argsort(-revenue_array)

    revenue_rank = np.empty_like(rankings)

    revenue_rank[rankings] = np.arange(
        1,
        len(rankings) + 1
    )

    df["revenue_rank"] = revenue_rank

    print(df[
        [
            "customer_id",
            "revenue",
            "revenue_rank"
        ]
    ].sort_values("revenue_rank"))

    return df


def compare_performance(df):
    """
    Compare execution time
    between Python loop
    and NumPy vectorization.
    """

    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)

    # Loop timing
    start = time.time()

    result_loop = []

    for value in df["revenue"]:

        result_loop.append(
            value * 1.10
        )

    loop_time = time.time() - start

    # NumPy timing
    start = time.time()

    result_np = (
        df["revenue"].values * 1.10
    )

    numpy_time = time.time() - start

    speedup = (
        loop_time / numpy_time
        if numpy_time > 0
        else float("inf")
    )

    print(f"Loop Time : {loop_time:.6f} seconds")

    print(f"NumPy Time : {numpy_time:.6f} seconds")

    print(f"Speedup : {speedup:.2f}x")

    return (
        result_loop,
        result_np,
        loop_time,
        numpy_time
    )
def validate_dataframe(df):
    """
    Validate DataFrame shape,
    columns and data types.
    """

    print("\n" + "=" * 60)
    print("DATAFRAME VALIDATION")
    print("=" * 60)

    print(f"\nShape : {df.shape}")

    print("\nData Types")

    print(df.dtypes)

    print("\nPreview")

    print(df.head())

    return df


def save_processed_data(df):
    """
    Save processed dataset.
    """

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df.to_csv(
        "data/processed/revenue_analysis.csv",
        index=False
    )

    print(
        "\nProcessed dataset saved successfully."
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
    print("NUMPY VECTORIZED COMPUTATION WORKFLOW")
    print("=" * 70)

    df = create_sample_dataset()

    df.to_csv(
        "data/raw/customer_revenue.csv",
        index=False
    )

    print("\nOriginal Dataset")

    print(df)

    # Task 1
    df = normalize_with_loop(df)

    df = normalize_with_numpy(df)

    # Task 2
    df = compute_zscore(df)

    # Task 3
    df = compute_rankings(df)

    # Task 4
    compare_performance(df)

    # Task 5
    validate_dataframe(df)

    save_processed_data(df)

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(
        f"Total Records : {len(df)}"
    )

    print(
        f"Maximum Revenue : "
        f"{df['revenue'].max()}"
    )

    print(
        f"Minimum Revenue : "
        f"{df['revenue'].min()}"
    )

    print(
        f"Highest Rank : "
        f"{df['revenue_rank'].min()}"
    )

    print(
        f"Lowest Rank : "
        f"{df['revenue_rank'].max()}"
    )

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()