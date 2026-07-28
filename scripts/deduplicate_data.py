import pandas as pd
import numpy as np
import os
import json
from datetime import datetime


def detect_exact_duplicates(df):
    """
    Find rows where all values are identical.
    Returns:
        (count, duplicate_rows_dataframe)
    """

    exact_dups = df.duplicated().sum()

    dup_rows = (
        df[df.duplicated(keep=False)]
        .sort_values(by=df.columns.tolist())
    )

    print("\n" + "=" * 60)
    print("EXACT DUPLICATE DETECTION")
    print("=" * 60)
    print(f"Exact duplicates found : {exact_dups}")
    print(f"Duplicate rows         : {len(dup_rows)}")

    if len(dup_rows) > 0:
        print("\nSample Duplicate Rows")
        print(dup_rows.head(10).to_string(index=False))

    return exact_dups, dup_rows


def detect_near_duplicates(df, key_columns):
    """
    Find records sharing the same key columns.
    """

    duplicate_keys = df[
        df.duplicated(
            subset=key_columns,
            keep=False
        )
    ]

    print("\n" + "=" * 60)
    print("NEAR DUPLICATE DETECTION")
    print("=" * 60)

    print(
        f"Records with duplicate keys : "
        f"{len(duplicate_keys)}"
    )

    print(
        f"Unique duplicate groups     : "
        f"{len(duplicate_keys.groupby(key_columns))}"
    )

    if len(duplicate_keys) > 0:

        print("\nSample Groups")

        for keys, group in list(
            duplicate_keys.groupby(key_columns)
        )[:3]:

            print(f"\nKey : {keys}")
            print(group.to_string(index=False))

    return duplicate_keys


def remove_exact_duplicates(
    df,
    keep="first"
):
    """
    Remove exact duplicate rows.
    """

    rows_before = len(df)

    df_dedup = df.drop_duplicates(
        keep=keep
    )

    rows_after = len(df_dedup)

    rows_removed = rows_before - rows_after

    removal_pct = (
        rows_removed / rows_before
    ) * 100

    print("\n" + "=" * 60)
    print("EXACT DUPLICATE REMOVAL")
    print("=" * 60)

    print(f"Keep Strategy : {keep}")
    print(f"Rows Before   : {rows_before}")
    print(f"Rows After    : {rows_after}")
    print(
        f"Removed       : "
        f"{rows_removed} ({removal_pct:.2f}%)"
    )

    return df_dedup

def remove_near_duplicates(
    df,
    key_columns,
    keep_strategy="most_complete"
):
    """
    Remove near-duplicates based on key columns.
    """

    rows_before = len(df)

    if keep_strategy == "most_complete":

        def keep_most_complete(group):
            null_counts = group.isnull().sum(axis=1)
            best_idx = null_counts.idxmin()
            return group.loc[[best_idx]]

        df_dedup = (
            df.groupby(
                key_columns,
                group_keys=False
            )
            .apply(keep_most_complete)
            .reset_index(drop=True)
        )

    elif keep_strategy == "last":

        df_dedup = df.drop_duplicates(
            subset=key_columns,
            keep="last"
        )

    else:

        df_dedup = df.drop_duplicates(
            subset=key_columns,
            keep="first"
        )

    rows_after = len(df_dedup)

    rows_removed = rows_before - rows_after

    removal_pct = (
        rows_removed / rows_before
    ) * 100

    print("\n" + "=" * 60)
    print("NEAR DUPLICATE REMOVAL")
    print("=" * 60)
    print(f"Keep Strategy : {keep_strategy}")
    print(f"Key Columns   : {key_columns}")
    print(f"Rows Before   : {rows_before}")
    print(f"Rows After    : {rows_after}")
    print(
        f"Removed       : "
        f"{rows_removed} ({removal_pct:.2f}%)"
    )

    return df_dedup


def log_removed_duplicates(
    df_original,
    df_dedup
):
    """
    Save removed records to audit file.
    """

    os.makedirs("output", exist_ok=True)

    removed_mask = (
        ~df_original.index.isin(df_dedup.index)
    )

    removed_records = df_original[
        removed_mask
    ]

    print("\n" + "=" * 60)
    print("AUDIT LOGGING")
    print("=" * 60)
    print(
        f"Records Removed : {len(removed_records)}"
    )

    removed_records.to_csv(
        "output/removed_duplicates_audit.csv",
        index=False
    )

    audit_summary = {

        "removal_timestamp":
            datetime.now().isoformat(),

        "total_removed":
            int(len(removed_records)),

        "reason":
            "Duplicate detection",

        "audit_file":
            "output/removed_duplicates_audit.csv",

        "audit_note":
            "All removed records logged."
    }

    with open(
        "output/dedup_audit_summary.json",
        "w"
    ) as f:

        json.dump(
            audit_summary,
            f,
            indent=2
        )

    print("✓ Audit files generated")

    return (
        removed_records,
        audit_summary
    )


def compare_before_after(
    df_original,
    df_dedup
):
    """
    Compare dataset before and after deduplication.
    """

    comparison = {

        "rows_before":
            len(df_original),

        "rows_after":
            len(df_dedup),

        "rows_removed":
            len(df_original) - len(df_dedup),

        "removal_percentage":
            round(
                (
                    (
                        len(df_original)
                        - len(df_dedup)
                    )
                    / len(df_original)
                ) * 100,
                2
            ),

        "columns":
            len(df_original.columns),

        "nulls_before":
            int(
                df_original
                .isnull()
                .sum()
                .sum()
            ),

        "nulls_after":
            int(
                df_dedup
                .isnull()
                .sum()
                .sum()
            ),

        "timestamp":
            datetime.now().isoformat()
    }

    print("\n" + "=" * 70)
    print("DEDUPLICATION SUMMARY")
    print("=" * 70)

    for key, value in comparison.items():
        print(f"{key:20}: {value}")

    with open(
        "output/dedup_summary.json",
        "w"
    ) as f:

        json.dump(
            comparison,
            f,
            indent=2
        )

    return comparison
if __name__ == "__main__":

    os.makedirs("output", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Load dataset
    df_original = pd.read_csv(
        "data/raw/data_with_dupes.csv"
    )

    print("\n" + "=" * 70)
    print("STARTING DEDUPLICATION WORKFLOW")
    print("=" * 70)
    print(f"Initial Records : {len(df_original)}")

    # Step 1
    print("\n[1/6] Detect Exact Duplicates")
    exact_count, exact_rows = detect_exact_duplicates(
        df_original
    )

    # Step 2
    print("\n[2/6] Detect Near Duplicates")
    detect_near_duplicates(
        df_original,
        [
            "customer_id",
            "transaction_date"
        ]
    )

    # Step 3
    print("\n[3/6] Remove Exact Duplicates")

    df_exact = remove_exact_duplicates(
        df_original,
        keep="first"
    )

    # Step 4
    print("\n[4/6] Remove Near Duplicates")

    df_final = remove_near_duplicates(
        df_exact,
        key_columns=[
            "customer_id",
            "transaction_date"
        ],
        keep_strategy="most_complete"
    )

    # Step 5
    print("\n[5/6] Audit Logging")

    log_removed_duplicates(
        df_original,
        df_final
    )

    # Step 6
    print("\n[6/6] Summary")

    compare_before_after(
        df_original,
        df_final
    )

    df_final.to_csv(
        "data/processed/deduplicated_data.csv",
        index=False
    )

    print("\n✓ Deduplicated dataset saved.")