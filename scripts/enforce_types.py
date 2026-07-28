import os
import pandas as pd
import numpy as np


def cast_columns_to_types(df, type_mapping):
    """
    Explicitly cast columns to specified data types.
    Returns converted dataframe and conversion log.
    """
    df_typed = df.copy()
    conversion_log = {}

    print("\n========== TYPE CASTING ==========\n")

    for col, target_dtype in type_mapping.items():

        if col not in df.columns:
            print(f"Warning: {col} not found.")
            continue

        original_dtype = str(df[col].dtype)

        try:
            df_typed[col] = df_typed[col].astype(target_dtype)

            conversion_log[col] = {
                "from": original_dtype,
                "to": str(target_dtype),
                "status": "Success"
            }

            print(f"✓ {col}: {original_dtype} → {target_dtype}")

        except Exception as e:

            conversion_log[col] = {
                "from": original_dtype,
                "to": str(target_dtype),
                "status": "Failed",
                "error": str(e)
            }

            print(f"✗ {col}: {e}")

    return df_typed, conversion_log


def convert_string_dates_to_datetime(
    df,
    date_columns,
    date_format="%Y-%m-%d"
):
    """
    Convert string dates into datetime.
    """

    df_typed = df.copy()

    print("\n========== DATE CONVERSION ==========\n")

    for col in date_columns:

        if col not in df.columns:
            print(f"Warning: {col} not found.")
            continue

        try:

            df_typed[col] = pd.to_datetime(
                df_typed[col],
                format=date_format,
                errors="coerce"
            )

            print(f"✓ {col} converted to datetime")

        except Exception as e:

            print(f"✗ {col}: {e}")

    return df_typed


def convert_currency_to_float(df, currency_columns):
    """
    Remove currency symbols and convert to float.
    """

    df_typed = df.copy()

    print("\n========== CURRENCY CONVERSION ==========\n")

    for col in currency_columns:

        if col not in df.columns:
            print(f"Warning: {col} not found.")
            continue

        try:

            df_typed[col] = (
                df_typed[col]
                .astype(str)
                .str.replace(r"[$,₹€£]", "", regex=True)
                .str.strip()
            )

            df_typed[col] = pd.to_numeric(
                df_typed[col],
                errors="coerce"
            )

            failed = (
                df_typed[col].isna().sum()
                - df[col].isna().sum()
            )

            if failed > 0:
                print(
                    f"⚠ {failed} values in {col} "
                    "could not be converted."
                )

            print(f"✓ {col} converted to float")

        except Exception as e:

            print(f"✗ {col}: {e}")

    return df_typed


def convert_integers_to_boolean(df, boolean_columns):
    """
    Convert integer/object boolean values to bool.
    """

    df_typed = df.copy()

    print("\n========== BOOLEAN CONVERSION ==========\n")

    mapping = {
        "yes": True,
        "no": False,
        "true": True,
        "false": False,
        "y": True,
        "n": False,
        "1": True,
        "0": False,
        1: True,
        0: False,
        True: True,
        False: False
    }

    for col in boolean_columns:

        if col not in df.columns:
            print(f"Warning: {col} not found.")
            continue

        try:

            print(
                f"{col} unique values:",
                df[col].unique()
            )

            if df[col].dtype == object:

                df_typed[col] = (
                    df_typed[col]
                    .astype(str)
                    .str.lower()
                    .map(mapping)
                )

            else:

                df_typed[col] = (
                    df_typed[col]
                    .astype(bool)
                )

            print(f"✓ {col} converted to bool")

        except Exception as e:

            print(f"✗ {col}: {e}")

    return df_typed

def compare_dtypes(df_original, df_typed):
    """
    Compare dtypes before and after conversion.
    """

    comparison = pd.DataFrame({
        "column": df_original.columns,
        "dtype_before": df_original.dtypes.values,
        "dtype_after": df_typed.dtypes.values,
        "changed": (
            df_original.dtypes != df_typed.dtypes
        ).values
    })

    print("\n" + "=" * 70)
    print("DTYPE CONVERSION SUMMARY")
    print("=" * 70)
    print(comparison.to_string(index=False))

    os.makedirs("output", exist_ok=True)

    comparison.to_csv(
        "output/dtype_conversion_report.csv",
        index=False
    )

    print(
        "\nReport saved to "
        "output/dtype_conversion_report.csv"
    )

    return comparison


def main():

    input_file = "data/raw/untyped_data.csv"

    if not os.path.exists(input_file):
        print("Dataset not found!")
        return

    df = pd.read_csv(input_file)

    print("=" * 70)
    print("BEFORE TYPE CONVERSION")
    print("=" * 70)

    print(df.dtypes)

    print("\nSample Data")
    print(df.head())

    df_typed = df.copy()

    print("\n1. Converting Dates")
    df_typed = convert_string_dates_to_datetime(
        df_typed,
        [
            "transaction_date",
            "signup_date"
        ],
        "%Y-%m-%d"
    )

    print("\n2. Converting Currency")
    df_typed = convert_currency_to_float(
        df_typed,
        [
            "amount",
            "revenue"
        ]
    )

    print("\n3. Converting Boolean")
    df_typed = convert_integers_to_boolean(
        df_typed,
        [
            "is_active",
            "is_premium"
        ]
    )

    print("\n4. Explicit Type Casting")

    type_mapping = {
        "amount": "float64",
        "revenue": "float64",
        "is_active": "bool",
        "is_premium": "bool"
    }

    df_typed, conversion_log = cast_columns_to_types(
        df_typed,
        type_mapping
    )

    print("\n5. Final Data Types")

    print(df_typed.dtypes)

    compare_dtypes(
        df,
        df_typed
    )

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df_typed.to_csv(
        "data/processed/typed_data.csv",
        index=False
    )

    print(
        "\n✓ Typed data saved to "
        "data/processed/typed_data.csv"
    )


if __name__ == "__main__":
    main()