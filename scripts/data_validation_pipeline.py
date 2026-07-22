import pandas as pd
import numpy as np
import os


def create_sample_dataset():
    """
    Create sample customer dataset
    containing intentional validation errors.
    """

    data = {

        "customer_id": [
            101,102,None,104,105,
            106,107,108,109,110
        ],

        "age": [
            25,35,42,151,-5,
            28,40,60,32,45
        ],

        "price": [
            1500,2500,-300,4500,5000,
            3200,2800,1500,-200,4000
        ],

        "birth_date": [
            "1999-05-12",
            "1988-09-15",
            "2050-01-01",
            "1975-06-20",
            "2002-10-18",
            "1997-02-11",
            "1990-08-22",
            "1984-01-30",
            "2055-05-10",
            "1995-11-25"
        ],

        "email": [
            "john@gmail.com",
            "alice@gmail.com",
            "bobgmail.com",
            None,
            "david@yahoo.com",
            "eva@gmail.com",
            "samhotmail.com",
            "rose@gmail.com",
            "kevin@yahoo.com",
            "tom@gmail.com"
        ],

        "phone": [
            "9876543210",
            "9876543211",
            "12345",
            "9876543213",
            "9876543214",
            "9876543215",
            "abcd123456",
            "9876543217",
            "9876543218",
            "9876543219"
        ],

        "start_date": [
            "2025-01-01",
            "2025-02-01",
            "2025-03-01",
            "2025-04-01",
            "2025-05-01",
            "2025-06-01",
            "2025-07-01",
            "2025-08-01",
            "2025-09-01",
            "2025-10-01"
        ],

        "end_date": [
            "2025-01-31",
            "2025-01-20",
            "2025-03-15",
            "2025-04-20",
            "2025-05-25",
            "2025-05-20",
            "2025-07-30",
            "2025-08-28",
            "2025-08-25",
            "2025-10-30"
        ]

    }

    return pd.DataFrame(data)


def preprocess_dates(df):
    """
    Convert string columns to datetime.
    """

    df["birth_date"] = pd.to_datetime(df["birth_date"])

    df["start_date"] = pd.to_datetime(df["start_date"])

    df["end_date"] = pd.to_datetime(df["end_date"])

    return df


def validate_range(df):
    """
    Validate age, price and birth date.
    """

    print("\n" + "=" * 60)
    print("RANGE VALIDATION")
    print("=" * 60)

    df["valid_age"] = (
        (df["age"] >= 0) &
        (df["age"] <= 150)
    )

    df["valid_price"] = (
        df["price"] >= 0
    )

    df["valid_birth_date"] = (
        (df["birth_date"] >= pd.Timestamp("1920-01-01")) &
        (df["birth_date"] <= pd.Timestamp.now())
    )

    print(f"Invalid Ages : {(~df['valid_age']).sum()}")

    print(f"Invalid Prices : {(~df['valid_price']).sum()}")

    print(
        f"Invalid Birth Dates : "
        f"{(~df['valid_birth_date']).sum()}"
    )

    return df


def validate_nulls(df):
    """
    Validate mandatory fields.
    """

    print("\n" + "=" * 60)
    print("NULL VALIDATION")
    print("=" * 60)

    df["valid_customer_id"] = (
        df["customer_id"].notna()
    )

    df["valid_email"] = (
        df["email"].notna()
    )

    print(
        f"Missing Customer IDs : "
        f"{(~df['valid_customer_id']).sum()}"
    )

    print(
        f"Missing Emails : "
        f"{(~df['valid_email']).sum()}"
    )

    return df


def validate_format(df):
    """
    Validate email and phone formats.
    """

    print("\n" + "=" * 60)
    print("FORMAT VALIDATION")
    print("=" * 60)

    df["valid_email_format"] = (
        df["email"]
        .str.contains("@", na=False)
    )

    df["valid_phone"] = (
        df["phone"]
        .str.match(r"^\d{10}$", na=False)
    )

    print(
        f"Invalid Emails : "
        f"{(~df['valid_email_format']).sum()}"
    )

    print(
        f"Invalid Phone Numbers : "
        f"{(~df['valid_phone']).sum()}"
    )

    return df

def validate_business_rules(df):
    """
    Validate business rules.
    End date must be greater than
    or equal to start date.
    """

    print("\n" + "=" * 60)
    print("BUSINESS RULE VALIDATION")
    print("=" * 60)

    df["valid_date_order"] = (
        df["end_date"] >= df["start_date"]
    )

    print(
        f"Invalid Date Ranges : "
        f"{(~df['valid_date_order']).sum()}"
    )

    return df


def overall_validation(df):
    """
    Combine all validation rules.
    """

    print("\n" + "=" * 60)
    print("OVERALL VALIDATION")
    print("=" * 60)

    validation_columns = [

        "valid_age",
        "valid_price",
        "valid_birth_date",
        "valid_customer_id",
        "valid_email",
        "valid_email_format",
        "valid_phone",
        "valid_date_order"

    ]

    df["passes_all_checks"] = (
        df[validation_columns]
        .all(axis=1)
    )

    passed = df[
        df["passes_all_checks"]
    ]

    failed = df[
        ~df["passes_all_checks"]
    ]

    print(f"Total Records : {len(df)}")
    print(f"Passed : {len(passed)}")
    print(f"Failed : {len(failed)}")

    return df, passed, failed


def save_validation_results(
    passed,
    failed
):
    """
    Save passed and failed records.
    """

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    passed.to_csv(
        "data/processed/validated_data.csv",
        index=False
    )

    failed.to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print("\nValidation files saved.")


def validation_summary(df):
    """
    Display validation statistics.
    """

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    summary = pd.DataFrame({

        "Rule": [

            "Age",
            "Price",
            "Birth Date",
            "Customer ID",
            "Email Present",
            "Email Format",
            "Phone",
            "Date Order"

        ],

        "Passed": [

            df["valid_age"].sum(),
            df["valid_price"].sum(),
            df["valid_birth_date"].sum(),
            df["valid_customer_id"].sum(),
            df["valid_email"].sum(),
            df["valid_email_format"].sum(),
            df["valid_phone"].sum(),
            df["valid_date_order"].sum()

        ],

        "Failed": [

            (~df["valid_age"]).sum(),
            (~df["valid_price"]).sum(),
            (~df["valid_birth_date"]).sum(),
            (~df["valid_customer_id"]).sum(),
            (~df["valid_email"]).sum(),
            (~df["valid_email_format"]).sum(),
            (~df["valid_phone"]).sum(),
            (~df["valid_date_order"]).sum()

        ]

    })

    print(summary)

    summary.to_csv(
        "output/validation_summary.csv",
        index=False
    )

    return summary

def create_validation_report(df):
    """
    Create a structured validation report.
    """

    print("\n" + "=" * 60)
    print("VALIDATION REPORT")
    print("=" * 60)

    report = {

        "Total Records": len(df),
        "Passed Records": int(df["passes_all_checks"].sum()),
        "Failed Records": int((~df["passes_all_checks"]).sum()),

        "Invalid Age":
            int((~df["valid_age"]).sum()),

        "Invalid Price":
            int((~df["valid_price"]).sum()),

        "Invalid Birth Date":
            int((~df["valid_birth_date"]).sum()),

        "Missing Customer ID":
            int((~df["valid_customer_id"]).sum()),

        "Missing Email":
            int((~df["valid_email"]).sum()),

        "Invalid Email":
            int((~df["valid_email_format"]).sum()),

        "Invalid Phone":
            int((~df["valid_phone"]).sum()),

        "Invalid Date Order":
            int((~df["valid_date_order"]).sum())

    }

    report_df = pd.DataFrame(
        report.items(),
        columns=["Validation Rule", "Count"]
    )

    print(report_df)

    report_df.to_csv(
        "output/validation_report.csv",
        index=False
    )

    return report_df


def main():

    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("=" * 70)
    print("DATA VALIDATION PIPELINE")
    print("=" * 70)

    df = create_sample_dataset()

    df = preprocess_dates(df)

    df.to_csv(
        "data/raw/customer_data.csv",
        index=False
    )

    print("\nOriginal Dataset")
    print(df)

    # Task 1
    df = validate_range(df)

    # Task 2
    df = validate_nulls(df)

    # Task 3
    df = validate_format(df)

    # Task 4
    df = validate_business_rules(df)

    # Task 5
    df, passed, failed = overall_validation(df)

    save_validation_results(
        passed,
        failed
    )

    validation_summary(df)

    create_validation_report(df)

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(
        f"Total Records : {len(df)}"
    )

    print(
        f"Passed Records : {len(passed)}"
    )

    print(
        f"Failed Records : {len(failed)}"
    )

    print(
        f"Overall Validation Success : "
        f"{df['passes_all_checks'].sum()}"
    )

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()