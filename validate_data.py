import pandas as pd
import sys


# ==========================================
# SUPPORTPULSE DATA VALIDATION
# ==========================================

def validate(file_path):
    """
    Validate SupportPulse dataset.

    Returns exit code 1 when validation fails.
    """

    print("=" * 60)
    print("SupportPulse Data Validation")
    print("=" * 60)

    print(f"\nValidating: {file_path}")

    # ==========================================
    # LOAD DATA
    # ==========================================

    try:
        df = pd.read_csv(file_path)

    except Exception as error:
        print("\nVALIDATION FAILED:")
        print(f"  ERROR: Could not read dataset: {error}")
        sys.exit(1)

    print(f"Rows found: {len(df)}")
    print(f"Columns found: {len(df.columns)}")

    errors = []

    # ==========================================
    # CHECK 1 — REQUIRED COLUMNS
    # ==========================================

    required_columns = [
        "customer_id",
        "monthly_spend",
        "churn_status",
        "plan_type",
        "region",
        "signup_date"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        errors.append(
            "Missing required columns: "
            + str(missing_columns)
        )

    else:

        print(
            "PASS: All required columns are present"
        )

    # ==========================================
    # CHECK 2 — DATA TYPES
    # ==========================================

    if "monthly_spend" in df.columns:

        if not pd.api.types.is_numeric_dtype(
            df["monthly_spend"]
        ):

            errors.append(
                "Column 'monthly_spend' is not numeric"
            )

        else:

            print(
                "PASS: monthly_spend column is numeric"
            )

    # customer_id should exist and contain values
    if "customer_id" in df.columns:

        if df["customer_id"].isnull().any():

            errors.append(
                "Column 'customer_id' contains null values"
            )

        else:

            print(
                "PASS: customer_id contains no null values"
            )

    # ==========================================
    # CHECK 3 — MINIMUM ROW COUNT
    # ==========================================

    minimum_rows = 100

    if len(df) < minimum_rows:

        errors.append(
            f"Row count {len(df)} "
            f"is below minimum {minimum_rows}"
        )

    else:

        print(
            f"PASS: Row count {len(df)} "
            f"meets minimum {minimum_rows}"
        )

    # ==========================================
    # CHECK 4 — FULLY NULL COLUMNS
    # ==========================================

    null_columns = [
        column
        for column in df.columns
        if df[column].isnull().all()
    ]

    if null_columns:

        errors.append(
            "Fully null columns: "
            + str(null_columns)
        )

    else:

        print(
            "PASS: No fully null columns"
        )

    # ==========================================
    # CHECK 5 — CHURN STATUS
    # ==========================================

    if "churn_status" in df.columns:

        valid_churn_values = {
            0,
            1,
            True,
            False
        }

        unique_values = set(
            df["churn_status"]
            .dropna()
            .unique()
        )

        invalid_values = (
            unique_values
            - valid_churn_values
        )

        if invalid_values:

            errors.append(
                "Invalid churn_status values: "
                + str(invalid_values)
            )

        else:

            print(
                "PASS: churn_status values are valid"
            )

    # ==========================================
    # FINAL RESULT
    # ==========================================

    print("\n" + "=" * 60)

    if errors:

        print("VALIDATION FAILED:")

        for error in errors:
            print(f"  ERROR: {error}")

        print("=" * 60)

        sys.exit(1)

    else:

        print("ALL CHECKS PASSED")

        print("=" * 60)

        sys.exit(0)


# ==========================================
# COMMAND LINE ENTRY POINT
# ==========================================

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: python validate_data.py "
            "<dataset_path>"
        )

        sys.exit(1)

    validate(sys.argv[1])