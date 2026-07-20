import os
import json
from datetime import datetime

import chardet
import pandas as pd

INPUT_FILE = "data/raw/sample.csv"
OUTPUT_FILE = "output/intake_report.json"

EXPECTED_COLUMNS = [
    "customer_id",
    "customer_name",
    "transaction_amount",
    "transaction_date",
]


def validate_file_exists(filepath):
    """
    Check if the file exists and is not empty.
    """
    if not os.path.exists(filepath):
        return False, f"File does not exist: {filepath}"

    if os.path.getsize(filepath) == 0:
        return False, f"File is empty: {filepath}"

    return True, "File exists and has content"


def validate_file_format(filepath, allowed_formats=["csv", "json", "xlsx"]):
    """
    Check whether the file format is supported.
    """
    extension = filepath.split(".")[-1].lower()

    if extension not in allowed_formats:
        return False, (
            f"Unsupported format: {extension}. "
            f"Allowed formats: {allowed_formats}"
        )

    return True, f"Format valid: {extension}"


def validate_schema(df, expected_columns):
    """
    Validate DataFrame columns against expected schema.
    """
    missing = set(expected_columns) - set(df.columns)
    extra = set(df.columns) - set(expected_columns)

    issues = []

    if missing:
        issues.append(f"Missing columns: {missing}")

    if extra:
        issues.append(f"Unexpected columns: {extra}")

    if not issues:
        return True, f"Schema valid: {len(df.columns)} columns present"

    return False, " | ".join(issues)


def detect_encoding(filepath):
    """
    Detect file encoding using chardet.
    """
    with open(filepath, "rb") as file:
        result = chardet.detect(file.read(10000))

    encoding = result.get("encoding", "utf-8")
    confidence = result.get("confidence", 0)

    return (
        encoding,
        f"Detected: {encoding} (confidence: {confidence:.1%})",
    )


def capture_dataset_stats(filepath, df):
    """
    Capture dataset statistics.
    """
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "file_size_mb": round(os.path.getsize(filepath) / (1024 * 1024), 4),
        "bytes": os.path.getsize(filepath),
    }


def generate_intake_report(filepath, expected_columns):
    """
    Generate the complete intake validation report.
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "filepath": filepath,
        "validations": {},
    }

    # Check file existence
    file_exists, message = validate_file_exists(filepath)
    report["validations"]["file_exists"] = message

    if not file_exists:
        return report

    # Check file format
    format_valid, message = validate_file_format(filepath)
    report["validations"]["format"] = message

    if not format_valid:
        return report

    # Load dataset
    df = pd.read_csv(filepath)

    # Validate schema
    schema_valid, message = validate_schema(df, expected_columns)
    report["validations"]["schema"] = message

    # Detect encoding
    encoding, message = detect_encoding(filepath)
    report["validations"]["encoding"] = message

    # Dataset statistics
    report["statistics"] = capture_dataset_stats(filepath, df)

    # Save report
    with open(OUTPUT_FILE, "w") as file:
        json.dump(report, file, indent=4)

    return report


if __name__ == "__main__":
    report = generate_intake_report(INPUT_FILE, EXPECTED_COLUMNS)

    print("Dataset Intake Validation Completed")
    print(json.dumps(report, indent=4))