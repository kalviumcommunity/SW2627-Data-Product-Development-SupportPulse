import os
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
DOCS_DIR = ROOT / 'docs'
OUTPUT_DIR = ROOT / 'output'

TODAY = pd.Timestamp('2026-07-27')

FIRST_NAMES = [
    'Olivia', 'Liam', 'Emma', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'Logan', 'Mia', 'Lucas', 'Amelia', 'Aiden', 'Harper',
    'Jackson', 'Evelyn', 'Elijah', 'Abigail', 'Oliver', 'Emily', 'Jacob',
    'Charlotte', 'Michael', 'Madison', 'Benjamin', 'Avery', 'Carter',
    'Ella', 'James', 'Scarlett', 'Alexander', 'Grace', 'Sebastian', 'Chloe',
    'Daniel', 'Victoria', 'Matthew', 'Aria', 'Henry', 'Luna', 'Joseph',
    'Hannah', 'Samuel', 'Zoe', 'David', 'Penelope', 'William', 'Riley',
    'Owen', 'Layla', 'Wyatt', 'Lillian'
]
LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
    'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
    'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark',
    'Ramirez', 'Lewis', 'Robinson'
]

PLAN_TYPES = ['Basic', 'Pro', 'Premium']
REGIONS = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'EMEA']
TICKET_CATEGORIES = ['Billing', 'Technical', 'Onboarding', 'Account', 'Usage', 'Cancellation']
PRIORITIES = ['Low', 'Medium', 'High', 'Urgent']
SUPPORT_CHANNELS = ['Email', 'Phone', 'Chat', 'Self-service']
PAYMENT_STATUSES = ['Success', 'Failed', 'Pending']


def ensure_directories():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def sample_phone():
    prefix = np.random.choice(['703', '804', '915', '202', '310', '415', '212', '617'])
    suffix = ''.join(np.random.choice(list('0123456789'), size=7))
    return f'{prefix}{suffix}'


def generate_customers(n_customers=120):
    np.random.seed(42)
    customer_id = np.arange(1, n_customers + 1)
    names = [f'{np.random.choice(FIRST_NAMES)} {np.random.choice(LAST_NAMES)}' for _ in range(n_customers)]
    email = [f'{name.lower().replace(" ", ".").replace("'","")}@example.com' for name in names]
    phone = [sample_phone() for _ in range(n_customers)]
    tenure_days = np.random.randint(30, 900, size=n_customers)
    signup_date = TODAY - pd.to_timedelta(tenure_days, unit='D')
    plan_type = np.random.choice(PLAN_TYPES, size=n_customers, p=[0.38, 0.42, 0.20])
    region = np.random.choice(REGIONS, size=n_customers, p=[0.35, 0.25, 0.20, 0.10, 0.10])
    monthly_spend = [
        float(np.round(np.random.normal(55, 12), 2)) if plan == 'Basic'
        else float(np.round(np.random.normal(115, 18), 2)) if plan == 'Pro'
        else float(np.round(np.random.normal(220, 30), 2))
        for plan in plan_type
    ]
    monthly_spend = np.maximum(monthly_spend, 12.0)
    churned = np.random.choice([0, 1], size=n_customers, p=[0.70, 0.30])
    churn_date = []
    for status, start, tenure in zip(churned, signup_date, tenure_days):
        if status == 1:
            delta = np.random.randint(30, max(31, min(int(tenure), 365)))
            churn_date.append(start + pd.to_timedelta(delta, unit='D'))
        else:
            churn_date.append(pd.NaT)
    churn_date = pd.to_datetime(churn_date)
    churn_status = churned

    churn_date_formatted = pd.Series(churn_date).where(churned.astype(bool)).dt.strftime('%Y-%m-%d')

    customers = pd.DataFrame({
        'customer_id': customer_id,
        'name': names,
        'email': email,
        'phone': phone,
        'signup_date': signup_date.strftime('%Y-%m-%d'),
        'plan_type': plan_type,
        'region': region,
        'tenure_days': tenure_days,
        'monthly_spend': np.round(monthly_spend, 2),
        'churn_status': churn_status,
        'churn_date': churn_date_formatted
    })

    return customers


def generate_tickets(customers):
    tickets = []
    ticket_id = 1
    for _, row in customers.iterrows():
        signup_date_dt = pd.to_datetime(row['signup_date'])
        customer_end = pd.to_datetime(row['churn_date']) if pd.notna(row['churn_date']) else TODAY
        ticket_count = max(1, int(np.random.poisson(4)))
        for _ in range(ticket_count):
            created = signup_date_dt + pd.to_timedelta(
                np.random.randint(0, max(1, (customer_end - signup_date_dt).days + 1)),
                unit='D'
            )
            priority = np.random.choice(PRIORITIES, p=[0.25, 0.45, 0.20, 0.10])
            category = np.random.choice(TICKET_CATEGORIES, p=[0.22, 0.28, 0.15, 0.12, 0.18, 0.05])
            resolved = np.random.choice([True, False], p=[0.82, 0.18])
            escalated = np.random.choice([True, False], p=[0.16 if resolved else 0.24, 0.84 if resolved else 0.76])
            resolution_time = round(np.random.normal(12, 10), 1) if resolved else np.nan
            resolution_time = max(resolution_time, 1.0) if resolved else ''
            csat_score = int(np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.08, 0.17, 0.40, 0.30])) if resolved else ''
            within_30d = False
            if pd.notna(row['churn_date']):
                churn_date = pd.to_datetime(row['churn_date'])
                within_30d = created >= churn_date - pd.Timedelta(days=30)
            tickets.append({
                'ticket_id': ticket_id,
                'customer_id': row['customer_id'],
                'created_date': created.strftime('%Y-%m-%d'),
                'ticket_category': category,
                'priority': priority,
                'support_channel': np.random.choice(SUPPORT_CHANNELS, p=[0.45, 0.25, 0.25, 0.05]),
                'escalated': escalated,
                'resolved': resolved,
                'resolution_time': resolution_time,
                'csat_score': csat_score,
                'within_30d_of_cancellation': within_30d
            })
            ticket_id += 1
    return pd.DataFrame(tickets)


def generate_transactions(customers):
    transactions = []
    txn_id = 1
    for _, row in customers.iterrows():
        end_date = pd.to_datetime(row['churn_date']) if pd.notna(row['churn_date']) else TODAY
        if end_date < pd.to_datetime(row['signup_date']):
            end_date = TODAY
        total_tx = max(1, int(np.random.poisson(8)))
        for _ in range(total_tx):
            trx_date = pd.to_datetime(row['signup_date']) + pd.to_timedelta(np.random.randint(0, max(1, (end_date - pd.to_datetime(row['signup_date'])).days + 1)), unit='D')
            amount = round(np.random.normal(row['monthly_spend'] * 0.4, row['monthly_spend'] * 0.25), 2)
            amount = float(np.round(max(amount, 5.0), 2))
            status = np.random.choice(PAYMENT_STATUSES, p=[0.92, 0.05, 0.03])
            transactions.append({
                'transaction_id': f'TXN{txn_id:06d}',
                'customer_id': row['customer_id'],
                'transaction_date': trx_date.strftime('%Y-%m-%d'),
                'amount': amount,
                'payment_status': status
            })
            txn_id += 1
    trans = pd.DataFrame(transactions)
    trans.sort_values(['customer_id', 'transaction_date'], inplace=True)
    trans.reset_index(drop=True, inplace=True)
    return trans


def build_customer_transactions(transactions):
    agg = (
        transactions[transactions['payment_status'] == 'Success']
        .groupby('customer_id')
        .agg(
            total_transactions=('transaction_id', 'count'),
            purchase_count=('transaction_id', 'count'),
            total_spent=('amount', 'sum'),
            last_purchase_date=('transaction_date', 'max')
        )
        .reset_index()
    )
    agg['average_order_value'] = np.round(agg['total_spent'] / agg['purchase_count'], 2)
    agg['days_since_last_purchase'] = (TODAY - pd.to_datetime(agg['last_purchase_date'])).dt.days
    agg['customer_lifetime_value'] = np.round(agg['total_spent'] * 1.5, 2)
    return agg[['customer_id', 'total_transactions', 'purchase_count', 'total_spent', 'days_since_last_purchase', 'average_order_value', 'customer_lifetime_value']]


def build_customer_revenue(customers):
    revenue = customers[['customer_id', 'monthly_spend']].copy()
    revenue['monthly_revenue'] = revenue['monthly_spend']
    revenue['annual_revenue'] = np.round(revenue['monthly_revenue'] * 12, 2)
    return revenue[['customer_id', 'monthly_revenue', 'annual_revenue']]


def create_missing_data(customers):
    missing = customers.sample(18, random_state=5).copy()
    for i, col in enumerate(['email', 'phone', 'signup_date', 'plan_type', 'region', 'monthly_spend']):
        idx = missing.sample(3, random_state=i).index
        if missing[col].dtype.kind in 'fiu':
            missing.loc[idx, col] = np.nan
        else:
            missing.loc[idx, col] = ''
    missing.loc[missing.sample(3, random_state=7).index, 'churn_date'] = ''
    return missing


def create_quality_test(customers):
    invalid = customers.sample(20, random_state=9).copy()
    invalid = invalid.astype({
        'email': 'object',
        'phone': 'object',
        'signup_date': 'object',
        'monthly_spend': 'float',
        'tenure_days': 'object'
    })
    invalid.loc[invalid.index[:4], 'email'] = ['bademail', 'jane@doe', 'no-at-sign.com', 'user@@example.com']
    invalid.loc[invalid.index[4:8], 'phone'] = ['12345', 'phone123', '999', 'abcdefghij']
    invalid.loc[invalid.index[8:12], 'signup_date'] = ['2026-14-01', '01/32/2025', '2025-02-30', '2025/13/05']
    invalid.loc[invalid.index[12:16], 'monthly_spend'] = [-20.0, -5.5, 0.0, -100.0]
    invalid.loc[invalid.index[16:20], 'tenure_days'] = [-5, -10, 9999, 0]
    return invalid


def create_data_with_dupes(customers):
    sample = customers.sample(15, random_state=12)
    duplicates = pd.concat([customers, sample], ignore_index=True)
    duplicates = duplicates.sample(frac=1, random_state=16).reset_index(drop=True)
    return duplicates


def create_messy_text_data(customers, tickets):
    messy_customers = customers.sample(30, random_state=13).copy()
    messy_customers['name'] = messy_customers['name'].apply(lambda x: x.replace(' ', '  ').upper() if np.random.rand() < 0.4 else x.lower())
    messy_customers['plan_type'] = messy_customers['plan_type'].replace({'Basic': 'basic', 'Pro': 'PRO', 'Premium': ' premium '})
    messy_customers['region'] = messy_customers['region'].apply(lambda x: x.strip().title() if np.random.rand() < 0.5 else x.upper())
    messy_customers['email'] = messy_customers['email'].apply(lambda x: x.replace('.', '._') if np.random.rand() < 0.2 else x)
    messy_customers['phone'] = messy_customers['phone'].apply(lambda x: f' {x} ' if np.random.rand() < 0.2 else x)
    messy_customers['signup_date'] = messy_customers['signup_date'].apply(lambda x: pd.to_datetime(x).strftime('%d-%m-%Y') if np.random.rand() < 0.3 else x)

    messy_tickets = tickets.sample(30, random_state=14).copy()
    messy_tickets['ticket_category'] = messy_tickets['ticket_category'].apply(lambda x: x.upper() if np.random.rand() < 0.35 else x.lower())
    messy_tickets['priority'] = messy_tickets['priority'].apply(lambda x: x.replace('High', 'HIGH ').replace('Low', ' low') if np.random.rand() < 0.3 else x)
    messy_tickets['support_channel'] = messy_tickets['support_channel'].apply(lambda x: x.replace('Phone', ' phone').replace('Chat', 'CHAT') if np.random.rand() < 0.3 else x)
    messy_tickets['created_date'] = messy_tickets['created_date'].apply(lambda x: pd.to_datetime(x).strftime('%m/%d/%Y') if np.random.rand() < 0.4 else x)
    messy = pd.concat([messy_customers, messy_tickets], sort=False)
    for col in messy.select_dtypes(include=['object']).columns:
        messy[col] = messy[col].fillna('')
    return messy


def create_untyped_data(customers):
    untyped = customers.head(25).copy()
    untyped['customer_id'] = untyped['customer_id'].astype(str)
    untyped['tenure_days'] = untyped['tenure_days'].astype(str)
    untyped['monthly_spend'] = untyped['monthly_spend'].astype(str)
    untyped['churn_status'] = untyped['churn_status'].astype(str)
    untyped['signup_date'] = pd.to_datetime(untyped['signup_date']).dt.strftime('%b %d, %Y')
    untyped['churn_date'] = untyped['churn_date'].replace('', pd.NaT).apply(lambda x: pd.to_datetime(x).strftime('%d/%m/%Y') if pd.notna(x) else '')
    return untyped


def build_processed_datasets(customers, tickets, revenue, txn_agg):
    cleaned_customers = customers.copy()
    cleaned_customers['name'] = cleaned_customers['name'].str.title().str.strip()
    cleaned_customers['email'] = cleaned_customers['email'].str.lower().str.strip()
    cleaned_customers['plan_type'] = cleaned_customers['plan_type'].str.title().str.strip()
    cleaned_customers['region'] = cleaned_customers['region'].str.title().str.strip()
    cleaned_customers['phone'] = cleaned_customers['phone'].str.replace(r'[^0-9]', '', regex=True)

    cleaned_tickets = tickets.copy()
    cleaned_tickets['ticket_category'] = cleaned_tickets['ticket_category'].str.title()
    cleaned_tickets['priority'] = cleaned_tickets['priority'].str.title()
    cleaned_tickets['support_channel'] = cleaned_tickets['support_channel'].str.title()
    cleaned_tickets['resolved'] = cleaned_tickets['resolved'].astype(bool)
    cleaned_tickets['escalated'] = cleaned_tickets['escalated'].astype(bool)
    cleaned_tickets['csat_score'] = pd.to_numeric(cleaned_tickets['csat_score'], errors='coerce')

    cleaned_customers['monthly_spend'] = cleaned_customers['monthly_spend'].astype(float)
    cleaned_customers['tenure_days'] = cleaned_customers['tenure_days'].astype(int)

    validated = cleaned_customers.copy()
    validated['valid_email'] = validated['email'].str.contains(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', regex=True)
    validated['valid_phone'] = validated['phone'].str.match(r'^\d{10}$')
    validated['valid_signup_date'] = pd.to_datetime(validated['signup_date'], errors='coerce').notna()
    validated['valid_monthly_spend'] = validated['monthly_spend'] >= 0
    validated['passes_all_checks'] = validated[['valid_email', 'valid_phone', 'valid_signup_date', 'valid_monthly_spend']].all(axis=1)

    typed = validated.copy()
    typed['customer_id'] = typed['customer_id'].astype(int)
    typed['tenure_days'] = typed['tenure_days'].astype(int)
    typed['monthly_spend'] = typed['monthly_spend'].astype(float)
    typed['churn_status'] = typed['churn_status'].astype(int)
    typed['signup_date'] = pd.to_datetime(typed['signup_date']).dt.strftime('%Y-%m-%d')
    typed['churn_date'] = pd.to_datetime(typed['churn_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    typed['churn_date'] = typed['churn_date'].fillna('')

    deduplicated = cleaned_customers.drop_duplicates(subset=['customer_id']).copy()

    feature_engineered = customers.copy()
    feature_engineered = feature_engineered.merge(txn_agg, on='customer_id', how='left')
    feature_engineered['ticket_frequency'] = (tickets.groupby('customer_id')['ticket_id'].count() / (feature_engineered['tenure_days'] / 30)).fillna(0).round(2)
    feature_engineered['avg_resolution_time'] = tickets.groupby('customer_id')['resolution_time'].apply(lambda x: pd.to_numeric(x, errors='coerce').mean()).fillna(0).round(2).values
    feature_engineered['customer_lifetime_value'] = np.round(feature_engineered['customer_lifetime_value'].fillna(feature_engineered['monthly_spend'] * 12 * 0.9), 2)
    feature_engineered['recency_score'] = pd.qcut(np.maximum(feature_engineered['days_since_last_purchase'].fillna(999), 0), 4, labels=[4, 3, 2, 1]).astype(int)
    feature_engineered['frequency_score'] = pd.qcut(np.maximum(feature_engineered['purchase_count'].fillna(0), 0) + 1, 4, labels=[1, 2, 3, 4]).astype(int)
    feature_engineered['monetary_score'] = pd.qcut(feature_engineered['total_spent'].fillna(0) + 1, 4, labels=[1, 2, 3, 4]).astype(int)
    feature_engineered['engagement_score'] = (feature_engineered['recency_score'] + feature_engineered['frequency_score'] + feature_engineered['monetary_score']).astype(int)
    churn_risk = feature_engineered['ticket_frequency'] * 0.15 + (1 - (feature_engineered['avg_resolution_time'] / 100)) * 0.25 + (1 - (feature_engineered['monthly_spend'] / feature_engineered['monthly_spend'].max())) * 0.10
    feature_engineered['churn_risk_score'] = np.round(np.clip(churn_risk * 100, 0, 100), 0).astype(int)
    feature_engineered['support_intensity'] = np.round((tickets.groupby('customer_id')['escalated'].mean().fillna(0) * 100), 1).astype(float)
    feature_engineered['spend_quartile'] = pd.qcut(feature_engineered['monthly_spend'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

    ticket_ts = tickets.copy()
    ticket_ts['created_date'] = pd.to_datetime(ticket_ts['created_date'], errors='coerce')
    ticket_ts['ticket_weekday'] = ticket_ts['created_date'].dt.day_name()
    ticket_ts['ticket_month'] = ticket_ts['created_date'].dt.to_period('M').astype(str)
    ticket_ts['days_since_ticket'] = (TODAY - ticket_ts['created_date']).dt.days

    revenue_analysis = revenue.merge(customers[['customer_id', 'plan_type', 'region']], on='customer_id', how='left')
    revenue_analysis = revenue_analysis.groupby(['plan_type', 'region'], as_index=False).agg(
        total_monthly_revenue=('monthly_revenue', 'sum'),
        total_annual_revenue=('annual_revenue', 'sum'),
        average_monthly_revenue=('monthly_revenue', 'mean')
    )

    customer_summary = customers.groupby('plan_type', as_index=False).agg(
        customer_count=('customer_id', 'count'),
        churn_rate=('churn_status', 'mean'),
        avg_monthly_spend=('monthly_spend', 'mean')
    )
    customer_summary['churn_rate'] = (customer_summary['churn_rate'] * 100).round(1).astype(str) + '%'

    ticket_summary = tickets.groupby('ticket_category', as_index=False).agg(
        ticket_count=('ticket_id', 'count'),
        escalated_rate=('escalated', lambda x: np.mean(x) * 100),
        resolution_rate=('resolved', lambda x: np.mean(x) * 100),
        avg_csat=('csat_score', lambda x: pd.to_numeric(x, errors='coerce').mean())
    )
    ticket_summary['escalated_rate'] = ticket_summary['escalated_rate'].round(1).astype(str) + '%'
    ticket_summary['resolution_rate'] = ticket_summary['resolution_rate'].round(1).astype(str) + '%'
    ticket_summary['avg_csat'] = ticket_summary['avg_csat'].round(2)

    dashboard_metrics = pd.DataFrame([{ 
        'total_customers': customers['customer_id'].nunique(),
        'active_customers': int((customers['churn_status'] == 0).sum()),
        'churn_rate': f"{((customers['churn_status'] == 1).mean() * 100):.1f}%",
        'average_resolution_time': f"{pd.to_numeric(tickets['resolution_time'], errors='coerce').mean():.1f}",
        'average_csat': f"{pd.to_numeric(tickets['csat_score'], errors='coerce').mean():.2f}",
        'escalation_rate': f"{(tickets['escalated'].mean() * 100):.1f}%",
        'monthly_revenue': revenue['monthly_revenue'].sum(),
        'revenue_per_customer': revenue['monthly_revenue'].mean().round(2),
        'ticket_resolution_rate': f"{(tickets['resolved'].mean() * 100):.1f}%",
        'unresolved_ticket_rate': f"{(1 - tickets['resolved'].mean()) * 100:.1f}%",
        'revenue_lost_to_churn': np.round(revenue.loc[customers['churn_status'] == 1, 'monthly_revenue'].sum(), 2)
    }])

    churn_report = customers.groupby(['plan_type', 'region'], as_index=False).agg(
        churned=('churn_status', 'sum'),
        total_customers=('customer_id', 'count')
    )
    churn_report['churn_rate'] = (churn_report['churned'] / churn_report['total_customers'] * 100).round(1).astype(str) + '%'

    return {
        'cleaned_customers': cleaned_customers,
        'cleaned_tickets': cleaned_tickets,
        'validated_data': validated,
        'typed_data': typed,
        'deduplicated_data': deduplicated,
        'feature_engineered_data': feature_engineered,
        'datetime_features': ticket_ts,
        'revenue_analysis': revenue_analysis,
        'customer_summary': customer_summary,
        'ticket_summary': ticket_summary,
        'dashboard_metrics': dashboard_metrics,
        'churn_report': churn_report
    }


def write_csv(name, df, directory):
    path = directory / f'{name}.csv'
    df.to_csv(path, index=False)
    print(f'Wrote {path}')
    return path


def write_docs():
    data_dictionary = DOCS_DIR / 'DATA_DICTIONARY.md'
    data_dictionary.write_text(
        '# Data Dictionary\n\n'
        'This project contains normalized customer support and churn analytics datasets. Each dataset is designed for a production-style analytics pipeline.\n\n'
        '## Raw datasets\n\n'
        '### customers.csv\n'
        '- `customer_id`: unique customer identifier\n'
        '- `name`: customer name\n'
        '- `email`: customer email address\n'
        '- `phone`: contact phone number\n'
        '- `signup_date`: customer onboarding date\n'
        '- `plan_type`: subscription tier or support plan\n'
        '- `region`: geographic region or market\n'
        '- `tenure_days`: days since signup\n'
        '- `monthly_spend`: recurring monthly spend amount\n'
        '- `churn_status`: binary churn indicator (1 = churned, 0 = active)\n'
        '- `churn_date`: date of churn event, if applicable\n\n'
        '### tickets.csv\n'
        '- `ticket_id`: unique ticket identifier\n'
        '- `customer_id`: foreign key to customers.csv\n'
        '- `created_date`: ticket creation date\n'
        '- `ticket_category`: support issue category\n'
        '- `priority`: ticket priority level\n'
        '- `support_channel`: support channel used\n'
        '- `escalated`: whether the ticket was escalated\n'
        '- `resolved`: whether the ticket was resolved\n'
        '- `resolution_time`: time to resolution in hours\n'
        '- `csat_score`: customer satisfaction rating 1-5\n'
        '- `within_30d_of_cancellation`: ticket occurred within 30 days before churn\n\n'
        '### customer_revenue.csv\n'
        '- `customer_id`: foreign key to customers.csv\n'
        '- `monthly_revenue`: monthly revenue per customer\n'
        '- `annual_revenue`: annualized revenue per customer\n\n'
        '### customer_transactions.csv\n'
        '- `customer_id`: foreign key to customers.csv\n'
        '- `total_transactions`: total successful transactions\n'
        '- `purchase_count`: number of purchases\n'
        '- `total_spent`: total successful payment amount\n'
        '- `days_since_last_purchase`: days since last successful transaction\n'
        '- `average_order_value`: average amount per purchase\n'
        '- `customer_lifetime_value`: derived lifetime value estimate\n\n'
        '### transactions.csv\n'
        '- `transaction_id`: unique transaction identifier\n'
        '- `customer_id`: foreign key to customers.csv\n'
        '- `transaction_date`: date of transaction\n'
        '- `amount`: transaction amount\n'
        '- `payment_status`: transaction payment status\n\n'
        '### missing_data.csv\n'
        '- a raw dataset containing realistic missing values for testing data imputation and validation\n\n'
        '### quality_test.csv\n'
        '- a raw dataset containing invalid values for data quality testing\n\n'
        '### data_with_dupes.csv\n'
        '- a raw dataset containing duplicate customer records for deduplication testing\n\n'
        '### messy_text_data.csv\n'
        '- a raw dataset containing inconsistent capitalization, spacing, and formatting for text cleaning exercises\n\n'
        '### untyped_data.csv\n'
        '- a raw dataset with numeric fields cast to text and inconsistent date formats for type validation testing\n\n'
        '## Processed datasets\n\n'
        '### cleaned_customers.csv\n'
        '- cleaned and normalized customer records\n\n'
        '### cleaned_tickets.csv\n'
        '- cleaned and normalized ticket records\n\n'
        '### validated_data.csv\n'
        '- customer records with validation flags for email, phone, signup date, and spend\n\n'
        '### typed_data.csv\n'
        '- typed customer records with normalized data types\n\n'
        '### deduplicated_data.csv\n'
        '- deduplicated customer records after removing duplicate keys\n\n'
        '### feature_engineered_data.csv\n'
        '- customer-level feature set including ticket frequency, churn risk, engagement, and spend quartile\n\n'
        '### datetime_features.csv\n'
        '- ticket-level date and time features such as weekday and days since ticket creation\n\n'
        '### revenue_analysis.csv\n'
        '- revenue metrics aggregated by plan and region\n\n'
        '### customer_summary.csv\n'
        '- summary statistics by plan type\n\n'
        '### ticket_summary.csv\n'
        '- summary statistics by ticket category\n\n'
        '### dashboard_metrics.csv\n'
        '- high-level dashboard KPIs for the dataset\n\n'
        '### churn_report.csv\n'
        '- churn counts and rates by plan and region\n'
    )

    kpi_reference = DOCS_DIR / 'kpi_reference.md'
    kpi_reference.write_text(
        '# KPI Reference\n\n'
        '## Total Customers\n'
        '- Definition: Distinct customers in the dataset.\n'
        '- Formula: COUNT(DISTINCT customer_id)\n\n'
        '## Active Customers\n'
        '- Definition: Customers with no churn event.\n'
        '- Formula: COUNT(customer_id) WHERE churn_status = 0\n\n'
        '## Churn Rate\n'
        '- Definition: Percent of customers who cancelled.\n'
        '- Formula: SUM(churn_status) / COUNT(customer_id)\n\n'
        '## Average Resolution Time\n'
        '- Definition: Average hours to resolve support tickets.\n'
        '- Formula: AVG(resolution_time) WHERE resolved = TRUE\n\n'
        '## Average CSAT\n'
        '- Definition: Average customer satisfaction score.\n'
        '- Formula: AVG(csat_score)\n\n'
        '## Escalation Rate\n'
        '- Definition: Percent of tickets escalated.\n'
        '- Formula: SUM(escalated) / COUNT(ticket_id)\n\n'
        '## Revenue Per Customer\n'
        '- Definition: Average monthly revenue per customer.\n'
        '- Formula: AVG(monthly_revenue)\n\n'
        '## Customer Lifetime Value\n'
        '- Definition: Estimated lifetime value per customer using aggregated spend.\n'
        '- Formula: SUM(total_spent * 1.5) / COUNT(customer_id)\n\n'
        '## Ticket Resolution Rate\n'
        '- Definition: Percent of tickets resolved.\n'
        '- Formula: SUM(resolved) / COUNT(ticket_id)\n\n'
        '## Unresolved Ticket Rate\n'
        '- Definition: Percent of tickets not resolved.\n'
        '- Formula: SUM(NOT resolved) / COUNT(ticket_id)\n\n'
        '## Monthly Revenue\n'
        '- Definition: Total monthly revenue across all customers.\n'
        '- Formula: SUM(monthly_revenue)\n\n'
        '## Revenue Lost to Churn\n'
        '- Definition: Monthly revenue from churned customers.\n'
        '- Formula: SUM(monthly_revenue) WHERE churn_status = 1\n'
    )


def main():
    ensure_directories()
    customers = generate_customers()
    tickets = generate_tickets(customers)
    transactions = generate_transactions(customers)
    revenue = build_customer_revenue(customers)
    txn_agg = build_customer_transactions(transactions)

    write_csv('customers', customers, RAW_DIR)
    write_csv('tickets', tickets, RAW_DIR)
    write_csv('customer_revenue', revenue, RAW_DIR)
    write_csv('customer_transactions', txn_agg, RAW_DIR)
    write_csv('transactions', transactions, RAW_DIR)
    write_csv('missing_data', create_missing_data(customers), RAW_DIR)
    write_csv('quality_test', create_quality_test(customers), RAW_DIR)
    write_csv('data_with_dupes', create_data_with_dupes(customers), RAW_DIR)
    write_csv('messy_text_data', create_messy_text_data(customers, tickets), RAW_DIR)
    write_csv('untyped_data', create_untyped_data(customers), RAW_DIR)

    processed = build_processed_datasets(customers, tickets, revenue, txn_agg)
    for name, df in processed.items():
        write_csv(name, df, PROCESSED_DIR)

    write_docs()
    print('\nDataset generation complete.')


if __name__ == '__main__':
    main()
