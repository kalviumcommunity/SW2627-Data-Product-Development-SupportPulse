import pandas as pd
import os


def load_data():
    """
    Load cleaned customer and ticket datasets.
    """

    customers = pd.read_csv(
        "data/processed/cleaned_customers.csv"
    )

    tickets = pd.read_csv(
        "data/processed/cleaned_tickets.csv"
    )

    return customers, tickets


def create_customer_features(customers):
    """
    Create customer-based engineered features.
    """

    print("=" * 60)
    print("CUSTOMER FEATURE ENGINEERING")
    print("=" * 60)

    # Customer Lifetime Value
    customers["customer_lifetime_value"] = (
        customers["monthly_spend"] *
        customers["tenure_days"] / 30
    )

    # Tenure in Months
    customers["tenure_months"] = (
        customers["tenure_days"] / 30
    ).round(1)

    # Spend Category
    customers["spend_category"] = pd.cut(
        customers["monthly_spend"],
        bins=[0, 75, 150, 250, float("inf")],
        labels=[
            "Low",
            "Medium",
            "High",
            "Premium"
        ]
    )

    # Customer Segment
    customers["customer_segment"] = pd.qcut(
        customers["customer_lifetime_value"],
        q=4,
        labels=[
            "Bronze",
            "Silver",
            "Gold",
            "Platinum"
        ]
    )

    # Tenure Group
    customers["tenure_group"] = pd.cut(
        customers["tenure_days"],
        bins=[0,180,365,730,float("inf")],
        labels=[
            "New",
            "Growing",
            "Loyal",
            "Long-Term"
        ]
    )

    # High Value Customer
    customers["high_value_customer"] = (
        customers["monthly_spend"] > 150
    )

    print(customers.head())

    return customers


def create_ticket_features(tickets):
    """
    Create ticket-based engineered features.
    """

    print("=" * 60)
    print("TICKET FEATURE ENGINEERING")
    print("=" * 60)

    # Resolution Speed
    tickets["resolution_speed"] = pd.cut(
        tickets["resolution_time"],
        bins=[0, 24, 48, 72, float("inf")],
        labels=[
            "Fast",
            "Normal",
            "Slow",
            "Very Slow"
        ]
    )

    # High Priority Ticket
    tickets["high_priority"] = (
        tickets["priority"] == "High"
    )

    # Escalation Flag
    tickets["is_escalated"] = tickets["escalated"].astype(bool)

    # Customer Satisfaction Category
    tickets["csat_category"] = pd.cut(
        tickets["csat_score"],
        bins=[0, 2, 3, 4, 5],
        labels=[
            "Poor",
            "Average",
            "Good",
            "Excellent"
        ],
        include_lowest=True
    )

    # Resolution Status
    tickets["resolution_status"] = tickets["resolved"].map({
        True: "Resolved",
        False: "Open"
    })

    print(tickets.head())

    return tickets


def validate_features(customers, tickets):

    print("=" * 60)
    print("FEATURE VALIDATION")
    print("=" * 60)

    print("\nCustomer Features")

    print(customers[[
        "customer_lifetime_value",
        "tenure_months",
        "customer_segment",
        "tenure_group"
    ]].isnull().sum())

    print("\nTicket Features")

    print(tickets[[
    "resolution_speed",
    "high_priority",
    "csat_category",
    "resolution_status"
]].isnull().sum())


def save_data(customers, tickets):

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    customers.to_csv(
        "data/processed/feature_engineered_customers.csv",
        index=False
    )

    tickets.to_csv(
        "data/processed/feature_engineered_tickets.csv",
        index=False
    )

    print("\nFeature engineered datasets saved.")


def main():

    print("=" * 70)
    print("SUPPORTPULSE FEATURE ENGINEERING")
    print("=" * 70)

    customers, tickets = load_data()

    customers = create_customer_features(customers)

    tickets = create_ticket_features(tickets)

    validate_features(
        customers,
        tickets
    )

    save_data(
        customers,
        tickets
    )

    print("\nPipeline Completed Successfully.")


if __name__ == "__main__":
    main()