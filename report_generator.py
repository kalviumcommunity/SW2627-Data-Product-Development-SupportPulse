from datetime import date


def generate_report(df, report_date=None):
    """
    Generate a structured insight report from the
    current SupportPulse analysis DataFrame.

    Required sections:
    1. KPI Summary
    2. Key Finding
    3. Recommended Action
    """

    if report_date is None:
        report_date = date.today()

    # ==========================================
    # BASIC VALIDATION
    # ==========================================

    if df is None or df.empty:

        return (
            "SUPPORTPULSE INSIGHT REPORT\n"
            f"Date: {report_date}\n\n"
            "No data is available for the selected analysis."
        )

    # Work on a copy so the original DataFrame
    # is never modified by report generation.
    report_df = df.copy()

    # ==========================================
    # KPI CALCULATIONS
    # ==========================================

    total_customers = len(report_df)

    # Churn
    if "churn_status" in report_df.columns:

        churned_customers = int(
            report_df["churn_status"]
            .fillna(0)
            .sum()
        )

        churn_rate = (
            churned_customers /
            total_customers
        ) * 100

    else:

        churned_customers = 0
        churn_rate = 0

    # Monthly spend
    if "monthly_spend" in report_df.columns:

        spend = (
            report_df["monthly_spend"]
            .astype(float)
            .fillna(0)
        )

        total_spend = spend.sum()
        average_spend = spend.mean()

    else:

        total_spend = 0
        average_spend = 0

    # Escalations
    if "escalations" in report_df.columns:

        total_escalations = int(
            report_df["escalations"]
            .fillna(0)
            .sum()
        )

    else:

        total_escalations = 0

    # ==========================================
    # KEY FINDING
    # ==========================================

    if "plan_type" in report_df.columns:

        plan_summary = (
            report_df
            .groupby("plan_type")
            .size()
            .sort_values(
                ascending=False
            )
        )

        if not plan_summary.empty:

            top_plan = plan_summary.index[0]

            finding = (
                f"The largest customer segment is "
                f"{top_plan}, with "
                f"{plan_summary.iloc[0]:,} customers."
            )

        else:

            finding = (
                "No segment-level finding is available."
            )

    else:

        if churn_rate > 20:

            finding = (
                f"Customer churn is elevated at "
                f"{churn_rate:.1f}%."
            )

        elif churn_rate > 0:

            finding = (
                f"The current customer churn rate is "
                f"{churn_rate:.1f}%."
            )

        else:

            finding = (
                "No churn information is available "
                "for the current analysis."
            )

    # ==========================================
    # RECOMMENDED ACTION
    # ==========================================

    if churn_rate >= 20:

        recommendation = (
            "Prioritize retention actions for "
            "high-risk customers and investigate "
            "the support factors contributing to churn."
        )

    elif total_escalations > 0:

        recommendation = (
            "Review escalated support cases and "
            "identify opportunities to improve "
            "resolution quality and customer experience."
        )

    else:

        recommendation = (
            "Continue monitoring customer support "
            "and retention metrics for emerging risks."
        )

    # ==========================================
    # BUILD REPORT
    # ==========================================

    lines = []

    lines.append(
        "SUPPORTPULSE INSIGHT REPORT"
    )

    lines.append(
        "Date: " + str(report_date)
    )

    lines.append("")

    # ------------------------------------------
    # SECTION 1 — KPI SUMMARY
    # ------------------------------------------

    lines.append(
        "== KPI SUMMARY =="
    )

    lines.append(
        f"Total Customers: {total_customers:,}"
    )

    lines.append(
        f"Churned Customers: {churned_customers:,}"
    )

    lines.append(
        f"Churn Rate: {churn_rate:.1f}%"
    )

    lines.append(
        f"Total Monthly Spend: ${total_spend:,.2f}"
    )

    lines.append(
        f"Average Monthly Spend: ${average_spend:,.2f}"
    )

    lines.append(
        f"Total Escalations: {total_escalations:,}"
    )

    lines.append("")

    # ------------------------------------------
    # SECTION 2 — KEY FINDING
    # ------------------------------------------

    lines.append(
        "== KEY FINDING =="
    )

    lines.append(
        finding
    )

    lines.append("")

    # ------------------------------------------
    # SECTION 3 — RECOMMENDED ACTION
    # ------------------------------------------

    lines.append(
        "== RECOMMENDED ACTION =="
    )

    lines.append(
        recommendation
    )

    return "\n".join(lines)