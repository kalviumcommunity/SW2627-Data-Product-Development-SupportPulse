import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

def create_sample_dataset():
    """
    Create 60 days of synthetic revenue data.
    Some days intentionally contain anomalies.
    """

    dates = pd.date_range(
        start="2026-01-01",
        periods=60,
        freq="D"
    )

    revenue = np.random.normal(
        loc=10000,
        scale=1200,
        size=60
    )

    transaction_count = np.random.randint(
        150,
        400,
        size=60
    )

    signup_rate = np.random.randint(
        20,
        120,
        size=60
    )

    # Introduce anomalies
    revenue[15] = 2500
    revenue[30] = 2200
    revenue[45] = 27000

    transaction_count[15] = 40
    signup_rate[30] = 5

    df = pd.DataFrame({
        "date": dates,
        "daily_revenue": revenue,
        "transaction_count": transaction_count,
        "signup_rate": signup_rate
    })

    return df
alert_rules = {
    "daily_revenue": {
        "min": 5000,
        "max": 50000
    },
    "transaction_count": {
        "min": 100,
        "max": 10000
    },
    "signup_rate": {
        "min": 10,
        "max": 500
    }
}
def check_thresholds(metrics, rules):
    """
    Compare metrics with business thresholds.
    """

    alerts = []

    for metric_name, rule in rules.items():

        value = metrics[metric_name]

        if value < rule["min"]:

            alerts.append({
                "metric": metric_name,
                "value": value,
                "threshold": rule["min"],
                "direction": "BELOW_MIN",
                "severity": "HIGH"
            })

        elif value > rule["max"]:

            alerts.append({
                "metric": metric_name,
                "value": value,
                "threshold": rule["max"],
                "direction": "ABOVE_MAX",
                "severity": "MEDIUM"
            })

    return alerts
def run_threshold_monitor(df):
    """
    Check the latest day's metrics.
    """

    latest = df.iloc[-1]

    today_metrics = {
        "daily_revenue": latest["daily_revenue"],
        "transaction_count": latest["transaction_count"],
        "signup_rate": latest["signup_rate"]
    }

    alerts = check_thresholds(
        today_metrics,
        alert_rules
    )

    print("=" * 60)
    print("THRESHOLD ALERTS")
    print("=" * 60)

    if len(alerts) == 0:
        print("No threshold violations detected.")

    else:

        for alert in alerts:

            print(
                f"⚠ {alert['metric']} "
                f"{alert['direction']} | "
                f"Value={alert['value']:.2f} | "
                f"Threshold={alert['threshold']} | "
                f"Severity={alert['severity']}"
            )

    return alerts
def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    df = create_sample_dataset()

    print("\nDataset Created")
    print(df.head())

    run_threshold_monitor(df)

    daily_revenue, anomalies, z_scores = (
        statistical_monitor(df)
    )

    severity_df = severity_report(
        anomalies,
        z_scores,
        daily_revenue
    )

    anomalies_df = log_anomalies(
        anomalies,
        z_scores,
        daily_revenue
    )

    plot_anomalies(
        daily_revenue,
        anomalies
    )

    print("\nAssignment Completed Successfully.")


if __name__ == "__main__":
    main()

def detect_anomalies_zscore(series, threshold=2):
    """
    Detect anomalies using Z-score.
    """

    mean = series.mean()
    std = series.std()

    z_scores = abs((series - mean) / std)

    anomalies = series[z_scores > threshold]

    return anomalies, z_scores
def statistical_monitor(df):
    """
    Detect statistical anomalies
    from last 30 days.
    """

    daily_revenue = (
        df.set_index("date")["daily_revenue"]
        .tail(30)
    )

    anomalies, z_scores = detect_anomalies_zscore(
        daily_revenue,
        threshold=2
    )

    print("\n" + "=" * 60)
    print("Z-SCORE ANOMALY DETECTION")
    print("=" * 60)

    print(
        f"Detected {len(anomalies)} anomalies "
        f"out of {len(daily_revenue)} days."
    )

    for date, value in anomalies.items():

        print(
            f"{date.date()} | "
            f"${value:.2f} | "
            f"Z-Score : {z_scores.loc[date]:.2f}"
        )

    return daily_revenue, anomalies, z_scores
def classify_severity(value, mean, std):
    """
    Classify anomaly severity.
    """

    z_score = abs((value - mean) / std)

    if z_score > 3:
        return "CRITICAL"

    elif z_score > 2:
        return "HIGH"

    elif z_score > 1.5:
        return "MEDIUM"

    else:
        return "LOW"
def severity_report(
    anomalies,
    z_scores,
    daily_revenue
):
    """
    Generate severity table.
    """

    severity_list = []

    mean = daily_revenue.mean()
    std = daily_revenue.std()

    for date, value in anomalies.items():

        severity = classify_severity(
            value,
            mean,
            std
        )

        severity_list.append({

            "date": date,

            "value": round(value, 2),

            "z_score": round(
                z_scores.loc[date],
                2
            ),

            "severity": severity

        })

    severity_df = pd.DataFrame(
        severity_list
    )

    print("\n" + "=" * 60)
    print("SEVERITY REPORT")
    print("=" * 60)

    print(severity_df)

    critical = severity_df[
        severity_df["severity"].isin(
            ["CRITICAL", "HIGH"]
        )
    ]

    print(
        f"\nHigh Priority Anomalies : {len(critical)}"
    )

    return severity_df
def log_anomalies(
    anomalies,
    z_scores,
    daily_revenue
):
    """
    Store anomalies for investigation.
    """

    anomaly_log = []

    mean = daily_revenue.mean()
    std = daily_revenue.std()

    expected_range = (
        f"{mean - 2*std:.2f}"
        f" - "
        f"{mean + 2*std:.2f}"
    )

    for date, value in anomalies.items():

        anomaly_log.append({

            "timestamp":
                pd.Timestamp.now(),

            "anomaly_date":
                date,

            "metric":
                "daily_revenue",

            "value":
                round(value, 2),

            "expected_range":
                expected_range,

            "z_score":
                round(z_scores.loc[date], 2),

            "severity":
                classify_severity(
                    value,
                    mean,
                    std
                ),

            "status":
                "OPEN"

        })

    anomalies_df = pd.DataFrame(
        anomaly_log
    )

    anomalies_df.to_csv(
        "output/anomalies_log.csv",
        index=False
    )

    print("\nLogged", len(anomalies_df), "anomalies.")

    return anomalies_df
def plot_anomalies(
    daily_revenue,
    anomalies
):
    """
    Plot revenue with anomalies.
    """

    plt.figure(figsize=(14, 6))

    plt.plot(
        daily_revenue.index,
        daily_revenue.values,
        marker="o",
        linewidth=2,
        label="Daily Revenue"
    )

    rolling_avg = (
        daily_revenue
        .rolling(7)
        .mean()
    )

    plt.plot(
        rolling_avg.index,
        rolling_avg.values,
        linewidth=2,
        label="7-Day Moving Average"
    )

    mean = daily_revenue.mean()
    std = daily_revenue.std()

    plt.fill_between(
        daily_revenue.index,
        mean - 2 * std,
        mean + 2 * std,
        alpha=0.2,
        label="Expected Range"
    )

    for date, value in anomalies.items():

        plt.scatter(
            date,
            value,
            marker="X",
            s=180
        )

        plt.annotate(
            "ANOMALY",
            (date, value),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center"
        )

    plt.title(
        "Daily Revenue with Anomalies"
    )

    plt.xlabel("Date")

    plt.ylabel("Revenue")

    plt.xticks(rotation=45)

    plt.grid(alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "output/anomaly_detection.png",
        dpi=150
    )

    plt.show()

    print("\nVisualization Saved.")