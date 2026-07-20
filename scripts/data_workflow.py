import pandas as pd

INPUT_FILE = "data/raw/sample.csv"
OUTPUT_FILE = "output/processed.csv"


def ingest_data(filepath):
    """
    Read customer support dataset.

    Args:
        filepath (str): CSV file path.

    Returns:
        pd.DataFrame
    """
    df = pd.read_csv(filepath)
    return df


def process_data(df):
    """
    Clean the dataset.

    Removes duplicate rows and fills missing
    resolution time with median value.

    Args:
        df (pd.DataFrame)

    Returns:
        pd.DataFrame
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing resolution time
    df["resolution_time"] = df["resolution_time"].fillna(
        df["resolution_time"].median()
    )

    return df


def output_results(df, output_path):
    """
    Save processed dataset.

    Args:
        df (pd.DataFrame)
        output_path (str)
    """

    df.to_csv(output_path, index=False)
    print("Data successfully processed")
    print(f"Rows processed: {len(df)}")
    print(f"Output saved to {output_path}")


if __name__ == "__main__":

    data = ingest_data(INPUT_FILE)

    processed = process_data(data)

    output_results(processed, OUTPUT_FILE)