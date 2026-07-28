import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def create_sample_dataset():
    """
    Create a sample daily revenue dataset
    for time-series analysis.
    """

    np.random.seed(42)

    dates = pd.date_range(
        start="2025-01-01",
        periods=90,
        freq="D"
    )

    revenue = np.random.randint(
        8000,
        15000,
        size=90
    )

    orders = np.random.randint(
        50,
        150,
        size=90
    )

    df = pd.DataFrame({

        "date": dates,

        "revenue": revenue,

        "orders": orders

    })

    return df


def resample_data(df):
    """
    Resample data into weekly
    and monthly periods.
    """

    print("\n" + "=" * 60)
    print("TIME-SERIES RESAMPLING")
    print("=" * 60)

    df["date"] = pd.to_datetime(df["date"])

    df_ts = df.set_index("date")

    # Weekly Aggregation

    weekly_revenue = df_ts["revenue"].resample("W").sum()

    weekly_orders = df_ts["orders"].resample("W").count()

    weekly_average = df_ts["revenue"].resample("W").mean()

    print("\nWeekly Revenue\n")

    print(weekly_revenue)

    print("\nWeekly Order Count\n")

    print(weekly_orders)

    print("\nWeekly Average Revenue\n")

    print(weekly_average)

    # Monthly Aggregation

    monthly_revenue = df_ts["revenue"].resample("ME").sum()

    monthly_orders = df_ts["orders"].resample("ME").count()

    monthly_average = df_ts["revenue"].resample("ME").mean()

    print("\nMonthly Revenue\n")

    print(monthly_revenue)

    print("\nMonthly Order Count\n")

    print(monthly_orders)

    print("\nMonthly Average Revenue\n")

    print(monthly_average)

    print("\nHighest Revenue Week")

    print(weekly_revenue.idxmax())

    print(weekly_revenue.max())

    print("\nHighest Revenue Month")

    print(monthly_revenue.idxmax())

    print(monthly_revenue.max())

    return (

        df,

        df_ts,

        weekly_revenue,

        monthly_revenue

    )
def compute_rolling_average(df):
    """
    Compute rolling averages and
    visualize revenue trends.
    """

    print("\n" + "=" * 60)
    print("ROLLING WINDOW ANALYSIS")
    print("=" * 60)

    df["revenue_ma7"] = (
        df["revenue"]
        .rolling(window=7)
        .mean()
    )

    df["revenue_ma30"] = (
        df["revenue"]
        .rolling(window=30)
        .mean()
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        df["date"],
        df["revenue"],
        label="Raw Revenue",
        alpha=0.4
    )

    plt.plot(
        df["date"],
        df["revenue_ma7"],
        label="7-Day Moving Average",
        linewidth=2
    )

    plt.plot(
        df["date"],
        df["revenue_ma30"],
        label="30-Day Moving Average",
        linewidth=2
    )

    plt.title("Revenue Trend with Rolling Averages")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.legend()
    plt.grid(True)

    plt.savefig(
        "output/rolling_avg.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nRolling average plot saved.")

    return df


def month_over_month_change(df_ts):
    """
    Compute Month-over-Month
    percentage growth.
    """

    print("\n" + "=" * 60)
    print("MONTH-OVER-MONTH ANALYSIS")
    print("=" * 60)

    monthly_revenue = (
        df_ts["revenue"]
        .resample("ME")
        .sum()
    )

    mom_change = (
        monthly_revenue
        .pct_change()
        * 100
    )

    print("\nMonthly Revenue\n")

    print(monthly_revenue)

    print("\nMonth-over-Month Change (%)\n")

    print(mom_change)

    growth_months = (
        mom_change[
            mom_change > 0
        ]
    )

    decline_months = (
        mom_change[
            mom_change < 0
        ]
    )

    print("\nGrowth Months\n")

    print(growth_months)

    print("\nDecline Months\n")

    print(decline_months)

    return mom_change
def cumulative_analysis(df):
    """
    Compute cumulative revenue
    and visualize growth.
    """

    print("\n" + "=" * 60)
    print("CUMULATIVE REVENUE")
    print("=" * 60)

    df["cumulative_revenue"] = (
        df["revenue"]
        .cumsum()
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        df["date"],
        df["cumulative_revenue"],
        linewidth=2
    )

    plt.title("Cumulative Revenue Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Revenue")
    plt.grid(True)

    plt.savefig(
        "output/cumulative.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nTotal Revenue: "
        f"${df['cumulative_revenue'].iloc[-1]:,.0f}"
    )

    return df


def trend_analysis(df, mom_change):
    """
    Analyze revenue trend and
    generate business insights.
    """

    print("\n" + "=" * 60)
    print("TREND ANALYSIS")
    print("=" * 60)

    recent_ma30 = (
        df["revenue_ma30"]
        .dropna()
        .tail(30)
    )

    if recent_ma30.empty:

        trend_direction = "flat"
        trend_magnitude = 0

    else:

        trend_direction = (
            "up"
            if recent_ma30.iloc[-1] >
               recent_ma30.iloc[0]
            else "down"
        )

        trend_magnitude = (
            (
                recent_ma30.iloc[-1]
                -
                recent_ma30.iloc[0]
            )
            /
            recent_ma30.iloc[0]
        ) * 100

    latest_mom = (
        mom_change.iloc[-1]
        if not mom_change.dropna().empty
        else 0
    )

    analysis = f"""
=============================
TREND ANALYSIS REPORT
=============================

Rolling Average Trend : {trend_direction.upper()}

Change over last 30 days : {trend_magnitude:.2f}%

Latest Month-over-Month Growth : {latest_mom:.2f}%

Revenue Volatility (Std Dev) : ${df['revenue'].std():.2f}

Business Implications
---------------------

"""

    if trend_direction == "up":

        analysis += (
            "- Revenue trend is improving.\n"
            "- Continue current strategy.\n"
            "- Increase marketing investment.\n"
            "- Scale successful campaigns.\n"
        )

    else:

        analysis += (
            "- Revenue trend is declining.\n"
            "- Investigate customer churn.\n"
            "- Improve customer retention.\n"
            "- Review pricing and promotions.\n"
        )

    print(analysis)

    with open(
        "output/trend_analysis.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(analysis)

    return analysis


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("=" * 70)
    print("TIME-SERIES TREND & ROLLING METRICS")
    print("=" * 70)

    df = create_sample_dataset()

    print("\nSample Dataset\n")

    print(df.head())

    (
        df,
        df_ts,
        weekly_revenue,
        monthly_revenue
    ) = resample_data(df)

    df = compute_rolling_average(df)

    mom_change = month_over_month_change(df_ts)

    df = cumulative_analysis(df)

    trend_analysis(
        df,
        mom_change
    )

    print("\n" + "=" * 60)
    print("TESTING")
    print("=" * 60)

    print(
        f"Total Records : {len(df)}"
    )

    print(
        f"Date Range : "
        f"{df['date'].min().date()} "
        f"to "
        f"{df['date'].max().date()}"
    )

    print(
        f"Total Revenue : "
        f"${df['revenue'].sum():,}"
    )

    print(
        "\nPipeline Completed Successfully."
    )


if __name__ == "__main__":
    main()