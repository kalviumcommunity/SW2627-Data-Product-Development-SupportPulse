import pandas as pd
import os

# Create processed folder
os.makedirs("data/processed", exist_ok=True)

# Read datasets
customers = pd.read_csv("data/raw/customers.csv")
tickets = pd.read_csv("data/raw/tickets.csv")

print(customers.head())
print(tickets.head())

print("Customers Shape:", customers.shape)
print("Tickets Shape:", tickets.shape)

print(customers.info())
print(tickets.info())

print(customers.describe())

print(customers.isnull().sum())

print(tickets.isnull().sum())
customers.drop_duplicates(inplace=True)
tickets.drop_duplicates(inplace=True)

customers.drop_duplicates(subset="customer_id", inplace=True)

tickets.drop_duplicates(subset="ticket_id", inplace=True)

customers.drop_duplicates(subset="customer_id", inplace=True)

tickets.drop_duplicates(subset="ticket_id", inplace=True)

categorical_cols = customers.select_dtypes(include="object").columns

customers[categorical_cols] = customers[categorical_cols].fillna("Unknown")

text_cols = customers.select_dtypes(include="object").columns

for col in text_cols:
    customers[col] = customers[col].str.strip().str.title()

text_cols = tickets.select_dtypes(include="object").columns

for col in text_cols:
    tickets[col] = tickets[col].str.strip().str.title()

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
)

customers["churn_date"] = pd.to_datetime(
    customers["churn_date"],
    errors="coerce"
)

tickets["created_date"] = pd.to_datetime(
    tickets["created_date"],
    errors="coerce"
)

customers["monthly_spend_usd"] = pd.to_numeric(
    customers["monthly_spend_usd"],
    errors="coerce"
)

customers["tenure_days"] = pd.to_numeric(
    customers["tenure_days"],
    errors="coerce"
)
customers.to_csv(
    "data/processed/cleaned_customers.csv",
    index=False
)

tickets.to_csv(
    "data/processed/cleaned_tickets.csv",
    index=False
)

print("Data cleaned successfully.")