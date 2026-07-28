import os
import json
import pandas as pd


def ingest_csv(file_path):
    """
    Reads a CSV file and returns a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded CSV: {file_path}")
        return df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None


def ingest_json(file_path):
    """
    Reads a JSON file and returns a DataFrame.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        df = pd.DataFrame(data)
        print(f"Successfully loaded JSON: {file_path}")
        return df

    except Exception as e:
        print(f"Error reading JSON: {e}")
        return None


def ingest_csv_with_fallback(file_path):
    """
    Attempts to read a CSV using UTF-8.
    Falls back to latin-1 encoding if UTF-8 fails.
    """
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        print("CSV loaded using UTF-8 encoding.")
        return df

    except UnicodeDecodeError:
        print("UTF-8 failed. Trying latin-1...")

        try:
            df = pd.read_csv(file_path, encoding="latin-1")
            print("CSV loaded using latin-1 encoding.")
            return df

        except Exception as e:
            print(f"Fallback failed: {e}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def document_ingestion(df, source_name):
    """
    Prints ingestion summary.
    """
    if df is None:
        print(f"{source_name}: Ingestion Failed\n")
        return

    print("\n------------------------------")
    print(f"Source: {source_name}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("Column Names:")
    print(list(df.columns))
    print("------------------------------\n")


def save_processed(df, output_path):
    """
    Saves DataFrame as CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")


def main():

    csv_path = "data/raw/customers.csv"
    json_path = "data/raw/transactions.json"

    customers_df = ingest_csv_with_fallback(csv_path)
    transactions_df = ingest_json(json_path)

    document_ingestion(customers_df, "customers.csv")
    document_ingestion(transactions_df, "transactions.json")

    if customers_df is not None:
        save_processed(
            customers_df,
            "data/processed/customers_ingested.csv"
        )

    if transactions_df is not None:
        save_processed(
            transactions_df,
            "data/processed/transactions_ingested.csv"
        )

    print("\nData ingestion completed successfully.")


if __name__ == "__main__":
    main()