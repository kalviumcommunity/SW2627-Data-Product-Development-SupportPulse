import pandas as pd
import os

import pandas as pd
import os


def load_data():

    customers = pd.read_csv(
        "data/processed/feature_engineered_customers.csv"
    )

    tickets = pd.read_csv(
        "data/processed/feature_engineered_tickets.csv"
    )

    return customers, tickets


def calculate_kpis(customers, tickets):

    total_customers = len(customers)

    churned_customers = customers["churn_status"].sum()

    churn_rate = (
        churned_customers / total_customers
    ) * 100

    avg_monthly_spend = customers["monthly_spend"].mean()

    avg_customer_value = customers[
        "customer_lifetime_value"
    ].mean()

    total_tickets = len(tickets)

    resolved_tickets = tickets["resolved"].sum()

    resolution_rate = (
        resolved_tickets / total_tickets
    ) * 100

    avg_resolution_time = tickets[
        "resolution_time"
    ].mean()

    avg_csat = tickets[
        "csat_score"
    ].mean()

    escalation_rate = (
        tickets["escalated"].sum()
        / total_tickets
    ) * 100

    kpis = {

        "Total Customers": total_customers,

        "Churn Rate (%)": round(churn_rate,2),

        "Average Monthly Spend": round(avg_monthly_spend,2),

        "Average Customer Lifetime Value": round(avg_customer_value,2),

        "Total Tickets": total_tickets,

        "Resolution Rate (%)": round(resolution_rate,2),

        "Average Resolution Time": round(avg_resolution_time,2),

        "Average CSAT": round(avg_csat,2),

        "Escalation Rate (%)": round(escalation_rate,2)

    }

    return kpis


def save_kpis(kpis):

    os.makedirs(
        "output",
        exist_ok=True
    )

    df = pd.DataFrame(
        list(kpis.items()),
        columns=[
            "Metric",
            "Value"
        ]
    )

    df.to_csv(
        "output/dashboard_metrics.csv",
        index=False
    )

    print(df)


def main():

    customers, tickets = load_data()

    kpis = calculate_kpis(
        customers,
        tickets
    )

    save_kpis(kpis)

    print("\nKPI calculation completed.")


if __name__ == "__main__":
    main()