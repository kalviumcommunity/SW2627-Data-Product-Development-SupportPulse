import pandas as pd

customers = pd.read_csv(
    "data/processed/cleaned_customers.csv"
)

tickets = pd.read_csv(
    "data/processed/cleaned_tickets.csv"
)

report = []

report.append([
    "Duplicate Customers",
    customers.duplicated().sum()
])

report.append([
    "Duplicate Tickets",
    tickets.duplicated().sum()
])

report.append([
    "Missing Customer IDs",
    customers["customer_id"].isnull().sum()
])

report.append([
    "Missing Ticket IDs",
    tickets["ticket_id"].isnull().sum()
])

validation = pd.DataFrame(
    report,
    columns=["Check","Count"]
)

validation.to_csv(
    "output/validation_report.csv",
    index=False
)

print(validation)