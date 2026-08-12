import pandas as pd
import logging
import argparse
import os


# ==========================================
# LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================
# STAGE 1 — INGEST
# ==========================================

def ingest(file_path):
    """Load raw CSV data."""

    logger.info(
        "Ingesting data from: %s",
        file_path
    )

    df = pd.read_csv(file_path)

    logger.info(
        "Rows ingested: %s",
        len(df)
    )

    return df


# ==========================================
# STAGE 2 — CLEAN
# ==========================================

def clean(df):
    """Clean and validate the dataset."""

    logger.info("Cleaning data...")

    initial_rows = len(df)

    # Remove completely empty rows
    df = df.dropna(how="all")

    logger.info(
        "Rows after removing empty records: %s",
        len(df)
    )

    # Convert numeric columns where available
    if "monthly_spend" in df.columns:

        df["monthly_spend"] = pd.to_numeric(
            df["monthly_spend"],
            errors="coerce"
        )

        # Remove invalid negative spend
        df = df[
            df["monthly_spend"].isna()
            | (df["monthly_spend"] >= 0)
        ]

    # Remove rows without customer ID
    if "customer_id" in df.columns:

        df = df.dropna(
            subset=["customer_id"]
        )

    logger.info(
        "Cleaned: %s -> %s rows",
        initial_rows,
        len(df)
    )

    return df


# ==========================================
# STAGE 3 — AGGREGATE
# ==========================================

def aggregate(df):
    """Create aggregated customer metrics."""

    logger.info("Aggregating data...")

    # SupportPulse dataset
    if "plan_type" in df.columns:

        aggregation = (
            df.groupby("plan_type")
            .agg(
                customer_count=(
                    "customer_id",
                    "count"
                )
                if "customer_id" in df.columns
                else (
                    "plan_type",
                    "count"
                )
            )
            .reset_index()
        )

        # Add revenue/spend when available
        if "monthly_spend" in df.columns:

            spend_summary = (
                df.groupby("plan_type")[
                    "monthly_spend"
                ]
                .sum()
                .reset_index(
                    name="total_monthly_spend"
                )
            )

            aggregation = aggregation.merge(
                spend_summary,
                on="plan_type",
                how="left"
            )

        # Add churn when available
        if "churn_status" in df.columns:

            churn_summary = (
                df.groupby("plan_type")[
                    "churn_status"
                ]
                .mean()
                .reset_index(
                    name="churn_rate"
                )
            )

            churn_summary["churn_rate"] *= 100

            aggregation = aggregation.merge(
                churn_summary,
                on="plan_type",
                how="left"
            )

    else:

        # Generic fallback aggregation
        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_columns:

            aggregation = pd.DataFrame({
                "metric": numeric_columns,
                "mean": [
                    df[column].mean()
                    for column in numeric_columns
                ],
                "sum": [
                    df[column].sum()
                    for column in numeric_columns
                ]
            })

        else:

            aggregation = pd.DataFrame({
                "records": [len(df)]
            })

    logger.info(
        "Aggregation complete: %s rows",
        len(aggregation)
    )

    return aggregation


# ==========================================
# STAGE 4 — OUTPUT
# ==========================================

def output(cleaned_df, aggregated_df, output_dir):
    """Write processed datasets to output directory."""

    logger.info(
        "Writing output to: %s",
        output_dir
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    cleaned_path = os.path.join(
        output_dir,
        "cleaned_data.csv"
    )

    aggregated_path = os.path.join(
        output_dir,
        "aggregated_metrics.csv"
    )

    cleaned_df.to_csv(
        cleaned_path,
        index=False
    )

    aggregated_df.to_csv(
        aggregated_path,
        index=False
    )

    logger.info(
        "Cleaned output: %s",
        cleaned_path
    )

    logger.info(
        "Aggregated output: %s",
        aggregated_path
    )

    logger.info(
        "Pipeline complete."
    )


# ==========================================
# MAIN PIPELINE
# ==========================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "SupportPulse automated data pipeline"
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV file"
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Directory for processed output"
    )

    args = parser.parse_args()

    logger.info(
        "Starting SupportPulse pipeline"
    )

    raw_data = ingest(
        args.input
    )

    cleaned_data = clean(
        raw_data
    )

    aggregated_data = aggregate(
        cleaned_data
    )

    output(
        cleaned_data,
        aggregated_data,
        args.output
    )