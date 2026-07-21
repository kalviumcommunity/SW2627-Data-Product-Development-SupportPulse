import pandas as pd
import numpy as np
import json
import os


def profile_nulls_and_duplicates(df):
    """
    Compute null percentage and duplicate counts.
    """
    profile = {
        "null_counts": {},
        "null_percentages": {},
        "exact_duplicate_count": 0,
        "duplicate_percentage": 0
    }

    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100

        profile["null_counts"][col] = int(null_count)
        profile["null_percentages"][col] = round(null_pct, 2)

    duplicate_count = df.duplicated().sum()

    profile["exact_duplicate_count"] = int(duplicate_count)
    profile["duplicate_percentage"] = round(
        (duplicate_count / len(df)) * 100,
        2
    )

    return profile


def profile_numerical_columns(df):
    """
    Generate statistics for numerical columns.
    """
    numerical_cols = df.select_dtypes(include=[np.number]).columns

    stats = {}

    for col in numerical_cols:
        stats[col] = {
            "min": round(df[col].min(), 2),
            "max": round(df[col].max(), 2),
            "mean": round(df[col].mean(), 2),
            "median": round(df[col].median(), 2),
            "std": round(df[col].std(), 2),
            "null_count": int(df[col].isnull().sum())
        }

    return pd.DataFrame(stats).T


def profile_categorical_columns(df, top_n=5):
    """
    Generate categorical summaries.
    """
    categorical_cols = df.select_dtypes(include=["object"]).columns

    profile = {}

    for col in categorical_cols:
        profile[col] = {
            "unique_count": int(df[col].nunique()),
            "top_values": df[col].value_counts().head(top_n).to_dict(),
            "null_count": int(df[col].isnull().sum())
        }

    return profile


def identify_quality_issues(
    df,
    null_threshold=30,
    duplicate_threshold=5
):
    """
    Identify common quality problems.
    """

    issues = []

    # High Nulls
    null_percentages = (df.isnull().sum() / len(df)) * 100

    for col, pct in null_percentages.items():
        if pct > null_threshold:
            issues.append({
                "type": "High Nulls",
                "column": col,
                "severity": "HIGH",
                "value": f"{pct:.2f}% missing",
                "recommendation":
                    "Consider imputation or dropping the column."
            })

    # Duplicate rows
    duplicate_count = df.duplicated().sum()
    duplicate_pct = (duplicate_count / len(df)) * 100

    if duplicate_pct > duplicate_threshold:
        issues.append({
            "type": "High Duplicates",
            "column": "Entire Dataset",
            "severity": "HIGH",
            "value": f"{duplicate_pct:.2f}% duplicate rows",
            "recommendation":
                "Remove duplicate records before analysis."
        })

    # Negative values in amount columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns

    for col in numerical_cols:

        if "amount" in col.lower():

            if (df[col] < 0).any():
                issues.append({
                    "type": "Invalid Range",
                    "column": col,
                    "severity": "MEDIUM",
                    "value": "Negative values found",
                    "recommendation":
                        "Verify negative values."
                })

    return issues


def generate_profile_report(df, dataset_name):
    """
    Generate full profiling report.
    """

    report = {
        "dataset": dataset_name,
        "record_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "nulls_and_duplicates":
            profile_nulls_and_duplicates(df),
        "numerical_statistics":
            profile_numerical_columns(df).to_dict(),
        "categorical_statistics":
            profile_categorical_columns(df),
        "quality_issues":
            identify_quality_issues(df)
    }

    os.makedirs("output", exist_ok=True)

    with open(
        "output/profile_report.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            report,
            f,
            indent=4,
            default=str
        )

    print("\n" + "=" * 60)
    print("DATA QUALITY PROFILE")
    print("=" * 60)
    print(f"Dataset : {dataset_name}")
    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")
    print()

    print(
        f"Quality Issues Found : {len(report['quality_issues'])}"
    )

    print()

    if report["quality_issues"]:

        for issue in report["quality_issues"]:

            print(
                f"[{issue['severity']}] "
                f"{issue['type']} "
                f"-> {issue['column']}"
            )

            print(f"Value : {issue['value']}")

            print(
                f"Recommendation : "
                f"{issue['recommendation']}\n"
            )

    else:
        print("No major quality issues found.")

    print("=" * 60)

    return report


def main():

    dataset_path = "data/raw/quality_test.csv"

    if not os.path.exists(dataset_path):
        print("Dataset not found!")
        return

    df = pd.read_csv(dataset_path)

    generate_profile_report(
        df,
        dataset_path
    )


if __name__ == "__main__":
    main()