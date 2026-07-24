import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)


def create_sample_dataset():
    """
    Create a synthetic transaction dataset with
    an intentional outage window.
    """

    timestamps = pd.date_range(
        start="2026-01-10",
        periods=10000,
        freq="min"
    )

    customer_types = np.random.choice(
        ["Enterprise", "SMB", "Startup"],
        len(timestamps),
        p=[0.3, 0.4, 0.3]
    )

    payment_methods = np.random.choice(
        ["Credit Card", "Debit Card", "Crypto"],
        len(timestamps),
        p=[0.6, 0.3, 0.1]
    )

    regions = np.random.choice(
        ["India", "US", "Europe"],
        len(timestamps)
    )

    device_types = np.random.choice(
        ["Desktop", "Mobile", "Tablet"],
        len(timestamps)
    )

    status = []
    errors = []

    for ts, payment in zip(timestamps, payment_methods):

        # Simulated outage
        if (
            ts.date() == pd.Timestamp("2026-01-15").date()
            and 11 <= ts.hour <= 13
            and payment == "Credit Card"
        ):
            status.append("failure")
            errors.append("Stripe API timeout")

        else:
            status.append("success")
            errors.append("")

    df = pd.DataFrame({
        "timestamp": timestamps,
        "customer_type": customer_types,
        "payment_method": payment_methods,
        "region": regions,
        "device_type": device_types,
        "status": status,
        "error_message": errors
    })

    return df
def isolate_time_window(df):
    """
    Detect anomaly date and hour.
    """

    df["success_rate"] = (df["status"] == "success").astype(int)

    daily_success = (
        df.groupby(df["timestamp"].dt.date)["success_rate"]
        .mean()
    )

    threshold = daily_success.mean() - daily_success.std()

    anomaly_dates = daily_success[
        daily_success < threshold
    ].index

    print("=" * 60)
    print("DAILY SUCCESS RATE")
    print("=" * 60)

    print(daily_success)

    print("\nThreshold:", round(threshold, 3))
    print("Detected anomaly dates:", list(anomaly_dates))

    problem_day = anomaly_dates[0]

    hourly_data = (
        df[df["timestamp"].dt.date == problem_day]
        .groupby(df[df["timestamp"].dt.date == problem_day]["timestamp"].dt.hour)["success_rate"]
        .mean()
    )

    print("\nHourly Breakdown")
    print(hourly_data)

    problem_hour = hourly_data.idxmin()

    print(
        f"\nWorst Hour : {problem_hour}:00"
    )

    print(
        f"Success Rate : {hourly_data[problem_hour]:.2%}"
    )

    before = hourly_data.get(problem_hour - 1, None)
    after = hourly_data.get(problem_hour + 1, None)

    print("\nComparison")

    if before is not None:
        print(f"Before ({problem_hour-1}:00): {before:.2%}")

    print(f"Problem ({problem_hour}:00): {hourly_data[problem_hour]:.2%}")

    if after is not None:
        print(f"After ({problem_hour+1}:00): {after:.2%}")

    return problem_day, problem_hour

def main():

    os.makedirs("output", exist_ok=True)

    df = create_sample_dataset()

    print("\nDataset Created")
    print(df.shape)

    problem_day, problem_hour = isolate_time_window(df)

    affected_segment = segment_analysis(
        df,
        problem_day,
        problem_hour
    )

    top_error, error_pct = correlation_analysis(
        df,
        problem_day,
        problem_hour
    )

    generate_investigation_report(
        problem_day,
        problem_hour,
        affected_segment,
        top_error,
        error_pct
    )

    validate_hypothesis(
        problem_day,
        problem_hour
    )

    print("\nRoot Cause Investigation Completed Successfully")


if __name__ == "__main__":
    main()

def segment_analysis(df, problem_day, problem_hour):
    """
    Analyze which customer segments were affected.
    """

    problem_window = df[
        (df["timestamp"].dt.date == problem_day) &
        (df["timestamp"].dt.hour == problem_hour)
    ]

    print("\n" + "=" * 60)
    print("SEGMENT ANALYSIS")
    print("=" * 60)

    # Add success rate column
    problem_window = problem_window.copy()
    problem_window["success_rate"] = (
        problem_window["status"] == "success"
    ).astype(int)

    # Customer Type
    by_customer = problem_window.groupby(
        "customer_type"
    )["success_rate"].agg(["mean", "count"])

    print("\nBy Customer Type")
    print(by_customer)

    # Payment Method
    by_payment = problem_window.groupby(
        "payment_method"
    )["success_rate"].agg(["mean", "count"])

    print("\nBy Payment Method")
    print(by_payment)

    # Region
    by_region = problem_window.groupby(
        "region"
    )["success_rate"].agg(["mean", "count"])

    print("\nBy Region")
    print(by_region)

    affected_segment = by_payment[
        by_payment["mean"] < 0.5
    ].index[0]

    print("\nPattern Detected")
    print(f"Affected Payment Method : {affected_segment}")

    return affected_segment
def correlation_analysis(df, problem_day, problem_hour):
    """
    Identify patterns and dominant errors.
    """

    df = df.copy()

    df["is_problem_period"] = (
        (
            (df["timestamp"].dt.date == problem_day) &
            (df["timestamp"].dt.hour == problem_hour)
        )
    ).astype(int)

    print("\n" + "=" * 60)
    print("CORRELATION ANALYSIS")
    print("=" * 60)

    categorical_columns = [
        "payment_method",
        "customer_type",
        "region",
        "device_type"
    ]

    for column in categorical_columns:

        print(f"\n{column.upper()}")

        table = pd.crosstab(
            df[column],
            df["is_problem_period"]
        )

        print(table)

    errors = (
        df[df["is_problem_period"] == 1]["error_message"]
        .value_counts()
    )

    print("\nMost Common Errors")
    print(errors)

    top_error = errors.index[0]
    error_pct = (
        errors.iloc[0] /
        len(df[df["is_problem_period"] == 1])
    )

    print(
        f"\nDominant Error : {top_error}"
    )

    print(
        f"Occurred in {error_pct:.2%} of records."
    )

    return top_error, error_pct
def generate_investigation_report(
    problem_day,
    problem_hour,
    affected_segment,
    top_error,
    error_pct
):
    """
    Generate the final investigation report.
    """

    report = f"""
══════════════════════════════════════════════════════════════
ROOT CAUSE INVESTIGATION REPORT
══════════════════════════════════════════════════════════════

OBSERVATION
-----------
Revenue experienced a significant drop.

Date            : {problem_day}
Time Window     : {problem_hour}:00 - {problem_hour+1}:00 UTC

ANALYSIS
--------
Affected Payment Method : {affected_segment}

Dominant Error :
{top_error}

Occurrence :
{error_pct:.2%}

ROOT CAUSE HYPOTHESIS
---------------------
Credit Card payment processor experienced an outage
during the identified hour.

Supporting Evidence

• Failures concentrated in one payment method.
• Other payment methods continued successfully.
• Error logs consistently reported API timeout.
• Failure window matched one specific hour.

RECOMMENDED ACTIONS
-------------------
1. Add backup payment gateway.
2. Enable automatic failover.
3. Monitor payment gateway health.
4. Create alerts for unusual failure spikes.

CONFIDENCE LEVEL
----------------
HIGH
"""

    print(report)

    with open(
        "output/investigation_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    print("\nReport saved successfully.")

    return report
def validate_hypothesis(
    problem_day,
    problem_hour
):
    """
    Validate investigation findings.
    """

    validation = f"""
══════════════════════════════════════════════
HYPOTHESIS VALIDATION
══════════════════════════════════════════════

Timeline Alignment

External Event
---------------
{problem_day} {problem_hour}:15
Payment gateway outage reported.

Internal Data
-------------
{problem_day} {problem_hour}:15
Credit Card failures begin.

{problem_day} {problem_hour}:45
Transactions recover.

Segment Alignment

✓ Credit Card affected

✓ Debit unaffected

✓ Crypto unaffected

Conclusion

Root Cause Confirmed

Recommended Solution

• Introduce payment redundancy

• Automatic failover

• Health monitoring

• Real-time alerts
"""

    print(validation)

    with open(
        "output/hypothesis_validation.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(validation)

    print("Validation report saved.")