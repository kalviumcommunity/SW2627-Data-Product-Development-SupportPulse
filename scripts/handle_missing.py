import os
import json
import pandas as pd
import numpy as np


def analyze_missing_values(df):
    """
    Compute null counts and percentages before treatment.
    """
    missing_analysis = pd.DataFrame({
        "column": df.columns,
        "null_count": df.isnull().sum().values,
        "null_percentage": (
            df.isnull().sum() / len(df) * 100
        ).round(2).values,
        "data_type": df.dtypes.values
    })

    print("=" * 70)
    print("BEFORE IMPUTATION - Missing Value Analysis")
    print("=" * 70)
    print(missing_analysis.to_string(index=False))
    print(f"\nTotal Rows : {len(df)}")
    print(f"Total Cells: {len(df) * len(df.columns)}")
    print(f"Missing Cells: {df.isnull().sum().sum()}")
    print("=" * 70)

    return missing_analysis


def drop_rows_with_nulls(df, critical_cols):
    """
    Drop rows with missing values in critical columns.
    """
    rows_before = len(df)

    df = df.dropna(subset=critical_cols)

    rows_after = len(df)

    print(
        f"Dropped {rows_before - rows_after} rows "
        f"because {critical_cols} contained NULL values."
    )

    return df


def impute_mean_median(df, numerical_cols, strategy="median"):
    """
    Fill numerical columns using mean or median.
    """
    df = df.copy()

    for col in numerical_cols:

        if col in df.columns:

            if df[col].isnull().sum() > 0:

                if strategy == "median":
                    fill_value = df[col].median()
                else:
                    fill_value = df[col].mean()

                count = df[col].isnull().sum()

                df[col] = df[col].fillna(fill_value)

                print(
                    f"{col}: Filled {count} NULL values "
                    f"using {strategy} ({fill_value})"
                )

    return df


def impute_mode(df, categorical_cols):
    """
    Fill categorical columns with mode.
    """
    df = df.copy()

    for col in categorical_cols:

        if col in df.columns:

            if df[col].isnull().sum() > 0:

                mode_value = df[col].mode()[0]

                count = df[col].isnull().sum()

                df[col] = df[col].fillna(mode_value)

                print(
                    f"{col}: Filled {count} NULL values "
                    f"using mode ({mode_value})"
                )

    return df


def impute_forward_fill(df, datetime_cols):
    """
    Forward fill datetime columns.
    """
    df = df.copy()

    for col in datetime_cols:

        if col in df.columns:

            if df[col].isnull().sum() > 0:

                count = df[col].isnull().sum()

                df[col] = df[col].ffill()

                print(
                    f"{col}: Forward filled {count} NULL values"
                )

    return df


def document_imputation_decisions(df_before, df_after):
    """
    Save imputation decisions.
    """

    decisions = {
        "numerical_columns": {
            "strategy": "Median",
            "reason":
                "Median is resistant to outliers."
        },
        "categorical_columns": {
            "strategy": "Mode",
            "reason":
                "Mode preserves the most common category."
        },
        "datetime_columns": {
            "strategy": "Forward Fill",
            "reason":
                "Assumes previous value remains valid."
        },
        "critical_columns": {
            "strategy": "Drop Rows",
            "reason":
                "Primary identifiers should never be imputed."
        },
        "before_nulls":
            int(df_before.isnull().sum().sum()),
        "after_nulls":
            int(df_after.isnull().sum().sum())
    }

    os.makedirs("output", exist_ok=True)

    with open(
        "output/imputation_decisions.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            decisions,
            file,
            indent=4
        )

    print("\nImputation decisions saved.")


def validate_imputation(df_before, df_after):
    """
    Compare before and after metrics.
    """

    print("\n" + "=" * 70)
    print("AFTER IMPUTATION")
    print("=" * 70)

    print(f"Rows Before : {len(df_before)}")
    print(f"Rows After  : {len(df_after)}")

    print()

    print(
        f"Nulls Before : "
        f"{df_before.isnull().sum().sum()}"
    )

    print(
        f"Nulls After  : "
        f"{df_after.isnull().sum().sum()}"
    )

    print("\nRemaining NULL values:")

    print(df_after.isnull().sum())

    print("=" * 70)


def main():

    path = "data/raw/missing_data.csv"

    if not os.path.exists(path):
        print("Dataset not found!")
        return

    df = pd.read_csv(path)

    print("\nStep 1 - Analyze Missing Values\n")

    analyze_missing_values(df)

    print("\nStep 2 - Applying Imputation\n")

    critical_cols = []

    if "customer_id" in df.columns:
        critical_cols.append("customer_id")

    df_after = drop_rows_with_nulls(
        df,
        critical_cols
    )

    numerical_cols = list(
        df_after.select_dtypes(
            include=[np.number]
        ).columns
    )

    if "customer_id" in numerical_cols:
        numerical_cols.remove("customer_id")

    df_after = impute_mean_median(
        df_after,
        numerical_cols,
        strategy="median"
    )

    categorical_cols = list(
        df_after.select_dtypes(
            include=["object"]
        ).columns
    )

    datetime_cols = []

    for col in categorical_cols:

        if "date" in col.lower():

            datetime_cols.append(col)

    categorical_cols = [
        col
        for col in categorical_cols
        if col not in datetime_cols
    ]

    df_after = impute_mode(
        df_after,
        categorical_cols
    )

    df_after = impute_forward_fill(
        df_after,
        datetime_cols
    )

    print("\nStep 3 - Document Decisions\n")

    document_imputation_decisions(
        df,
        df_after
    )

    print("\nStep 4 - Validation\n")

    validate_imputation(
        df,
        df_after
    )

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df_after.to_csv(
        "data/processed/cleaned_data.csv",
        index=False
    )

    print(
        "\nCleaned dataset saved to "
        "data/processed/cleaned_data.csv"
    )


if __name__ == "__main__":
    main()