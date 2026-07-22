import pandas as pd
import numpy as np
import os


def create_sample_data():
    """
    Create sample dataset with messy text.
    """

    data = {
        "name": [
            " John ",
            "JOHN",
            "john",
            " Alice ",
            "ALICE",
            None
        ],

        "category": [
            " Electronics ",
            "electronics",
            "ELECTRONICS",
            " Furniture ",
            "FURNITURE",
            " electronics "
        ],

        "segment": [
            "B2B",
            "b2b",
            "B 2 B",
            "business-to-business",
            "SME",
            "enterprise"
        ],

        "city": [
            "São Paulo",
            "Montréal",
            " Chennai ",
            "New-York",
            "München",
            " Delhi "
        ]
    }

    return pd.DataFrame(data)


def strip_all_strings(df):
    """
    Strip whitespace from every string column.
    """

    print("\n" + "=" * 60)
    print("STRIPPING WHITESPACE")
    print("=" * 60)

    string_cols = df.select_dtypes(include=["object"]).columns

    total_fixed = 0

    for col in string_cols:

        before_unique = df[col].nunique(dropna=False)

        whitespace_count = (
            df[col]
            .fillna("")
            .str.match(r"^\s|\s$")
            .sum()
        )

        total_fixed += whitespace_count

        df[col] = df[col].str.strip()

        after_unique = df[col].nunique(dropna=False)

        print(f"\nColumn : {col}")
        print(f"Whitespace values : {whitespace_count}")
        print(f"Unique Before : {before_unique}")
        print(f"Unique After  : {after_unique}")

    print("\nTotal whitespace issues fixed:", total_fixed)

    return df


def normalize_casing(df, columns_to_lower):
    """
    Convert text columns to lowercase.
    """

    print("\n" + "=" * 60)
    print("CASING NORMALIZATION")
    print("=" * 60)

    for col in columns_to_lower:

        if col not in df.columns:
            continue

        print(f"\nBefore ({col})")
        print(df[col].head())

        df[col] = df[col].str.lower()

        print(f"\nAfter ({col})")
        print(df[col].head())

        print(f"✓ {col} converted to lowercase")

    return df
def remove_special_characters(df, columns):
    """
    Remove special characters using regex.
    """

    print("\n" + "=" * 60)
    print("SPECIAL CHARACTER REMOVAL")
    print("=" * 60)

    pattern = r"[^a-zA-Z0-9 ]"

    print(f"Regex Used : {pattern}")
    print("Removes everything except letters, numbers and spaces.\n")

    for col in columns:

        if col not in df.columns:
            continue

        print(f"\nBefore ({col})")
        print(df[col].head())

        df[col] = (
            df[col]
            .str.replace(pattern, "", regex=True)
        )

        print(f"\nAfter ({col})")
        print(df[col].head())

        print(f"✓ Cleaned {col}")

    return df


def standardize_categories(df):
    """
    Standardize category labels using mapping dictionaries.
    """

    print("\n" + "=" * 60)
    print("CATEGORY STANDARDIZATION")
    print("=" * 60)

    segment_map = {

        "b2b": "B2B",
        "b 2 b": "B2B",
        "b2 b": "B2B",
        "business-to-business": "B2B",

        "sme": "SMB",
        "small medium enterprise": "SMB",

        "enterprise": "Enterprise"
    }

    print("\nValue Counts Before Mapping")
    print(df["segment"].value_counts(dropna=False))

    df["segment"] = (
        df["segment"]
        .str.lower()
        .replace(segment_map)
    )

    print("\nValue Counts After Mapping")
    print(df["segment"].value_counts(dropna=False))

    print("\nCanonical Forms Chosen")
    print("--------------------------------")
    print("B2B        -> CRM Standard")
    print("SMB        -> Business Standard")
    print("Enterprise -> Enterprise")

    return df
def clean_text_column(
    series,
    lowercase=True,
    strip=True,
    remove_special=False,
    mapping=None
):
    """
    Reusable text cleaning function.
    """

    result = series.copy()

    if result.isna().any():
        print(
            f"Warning: {result.isna().sum()} null values found."
        )

    if strip:
        result = result.str.strip()

    if lowercase:
        result = result.str.lower()

    if remove_special:
        result = result.str.replace(
            r"[^a-zA-Z0-9 ]",
            "",
            regex=True
        )

    if mapping is not None:
        result = result.replace(mapping)

    return result

if __name__ == "__main__":

    os.makedirs("data/raw", exist_ok=True)

    df = create_sample_data()

    df.to_csv(
        "data/raw/messy_text_data.csv",
        index=False
    )

    print("\nOriginal Dataset\n")
    print(df)

    # Task 1
    df = strip_all_strings(df)

    # Task 2
    df = normalize_casing(
        df,
        [
            "name",
            "category",
            "segment"
        ]
    )

    # Task 3
    df = remove_special_characters(
        df,
        [
            "city",
            "name"
        ]
    )

    # Task 4
    df = standardize_categories(df)

    print("\nApplying reusable function...\n")

    segment_map = {
        "b2b": "B2B",
        "b 2 b": "B2B",
        "business-to-business": "B2B",
        "sme": "SMB",
        "enterprise": "Enterprise"
    }

    df["name"] = clean_text_column(
        df["name"],
        lowercase=True,
        strip=True
    )

    df["city"] = clean_text_column(
        df["city"],
        lowercase=False,
        strip=True,
        remove_special=True
    )

    df["segment"] = clean_text_column(
        df["segment"],
        lowercase=True,
        strip=True,
        mapping=segment_map
    )

    print("\nFinal Clean Dataset\n")
    print(df)

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(
        "data/processed/cleaned_text_data.csv",
        index=False
    )

    print(
        "\n✓ Cleaned dataset saved to "
        "data/processed/cleaned_text_data.csv"
    )
test_cases = [
    "  Product A  ",
    "PRODUCT B",
    "Product_C",
    None,
    ""
]

test_series = pd.Series(test_cases)

result = clean_text_column(
    test_series,
    lowercase=True,
    strip=True,
    remove_special=True
)

print("\nEdge Case Test")
print(result)