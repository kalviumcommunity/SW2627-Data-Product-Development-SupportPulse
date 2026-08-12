# 🛡️ ChurnGuard — AI Retention Platform

ChurnGuard is a customer retention and analytics platform built on the
SupportPulse data product.

It combines customer, support-ticket, and transaction data to monitor
customer behaviour, calculate churn-risk indicators, identify high-risk
customers, track business KPIs, generate alerts, and produce insight
reports.

The platform is designed for support managers, customer-success teams,
operations teams, and analysts who need to identify retention risks before
customers churn.

---

## 📌 Project Overview

### Business Problem

Customer support teams often have access to ticket activity, escalation
records, customer satisfaction scores, resolution times, and transaction
data, but these signals are not always connected to customer churn.

This makes retention efforts reactive rather than proactive.

### Solution

ChurnGuard combines these signals into a single analytics platform that
allows users to:

- Upload and inspect datasets
- Filter customer records
- Monitor customer and revenue KPIs
- Calculate customer risk scores
- Identify high-risk customers
- View interactive charts
- Detect threshold breaches
- Generate insight reports
- Run automated data pipelines
- Validate datasets before processing

---

# 📊 Dataset

The application works with SupportPulse customer, ticket, and transaction
data.

## Main Data Sources

| Dataset | Purpose |
|---|---|
| `customers.csv` | Customer profile and churn information |
| `tickets.csv` | Customer support activity |
| `transactions.csv` | Customer transaction and spending information |

## Important Customer Columns

| Column | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `monthly_spend` | Customer monthly spending |
| `churn_status` | Customer churn indicator |
| `plan_type` | Customer subscription/plan type |
| `region` | Customer region |
| `signup_date` | Customer account signup date |

Support-ticket data is used to derive support experience metrics such as
ticket count, escalation count, CSAT, and resolution time.

Transaction data is used to calculate customer revenue/spending metrics.

---

# ⚙️ Features

## Dataset Upload

Users can upload CSV or JSON datasets through the dashboard.

The upload module provides:

- File validation
- Row and column counts
- Null percentage
- Column validation
- Dataset preview
- Column summary
- Descriptive statistics

---

## 🔎 Filtering

Users can filter customer data based on available fields such as:

- Plan type
- Region
- Customer status

Filters update the displayed dataset and dashboard metrics.

---

## 📈 KPI Dashboard

The dashboard provides important business metrics including:

- Total records
- Total spend
- Average spend
- Churn rate
- Data quality

These metrics help support and business teams understand the current
customer base.

---

## 🚨 Alerts

ChurnGuard monitors KPI values against configured thresholds.

Examples include:

- High churn rate
- Poor data quality
- Other configured business metric breaches

Alerts help users identify issues that require investigation.

---

## 🤖 Customer Risk Analysis

The customer risk analysis combines churn and support-related signals
into a risk score.

The current rule-based calculation uses:

- Churn status
- Escalations
- Average CSAT
- Average resolution time

The resulting score is capped at 100.

Customers can then be ranked by risk score to identify customers requiring
attention.

---

## 📊 Interactive Charts

The dashboard provides visual analysis including:

- Customer trends
- Spend by plan
- Spend distribution

Charts are displayed when the required dataset columns are available.

---

## 📧 Insight Reports

Users can generate reports from the currently filtered dataset.

The reporting functionality provides:

- Report generation
- Report preview
- Email delivery

Email delivery requires SMTP configuration.

---

# 🔄 Pipeline Architecture

The data product follows this general flow:

```text
                 CSV / JSON Dataset
                         |
                         v
                +------------------+
                |    Ingestion     |
                | Load input data  |
                +--------+---------+
                         |
                         v
                +------------------+
                |    Validation    |
                | Check schema and |
                | data quality     |
                +--------+---------+
                         |
                         v
                +------------------+
                |     Cleaning     |
                | Remove invalid   |
                | records and      |
                | normalize types  |
                +--------+---------+
                         |
                         v
                +------------------+
                |   Aggregation    |
                | Customer metrics |
                | and summaries    |
                +--------+---------+
                         |
                         v
                +------------------+
                |     Output       |
                | cleaned_data.csv |
                | aggregated_      |
                | metrics.csv      |
                +--------+---------+
                         |
                         v
                +------------------+
                |    Dashboard     |
                | KPIs / Filters   |
                | Charts / Alerts  |
                +--------+---------+
                         |
                         v
                +------------------+
                | Insight Reports  |
                | Email Delivery   |
                +------------------+
```
### Pipeline Stages
**1. Ingestion**

The pipeline loads the input CSV dataset.

Example:
```
python pipeline.py \
  --input data/raw/customers.csv \
  --output output/pipeline
```
**2. Cleaning**

The pipeline:

- Removes completely empty rows
- Converts numeric fields where required
- Removes invalid negative spending values
- Removes records without a customer ID

**3. Aggregation**

Customer information can be grouped by plan type and summarized using
available metrics such as:

- Customer count
- Total monthly spend
- Churn rate

**4. Output**

The pipeline writes:
```
output/pipeline/
├── cleaned_data.csv
└── aggregated_metrics.csv
```
**5. Dashboard**

The Streamlit application loads the processed information and provides:

- KPIs
- Filters
- Charts
- Alerts
- Customer risk analysis

**6. Reporting**

Filtered dashboard data can be used to generate insight reports and,
when SMTP is configured, deliver them by email.

**🧮 Derived Features**

The following metrics are derived from the available customer,
ticket, and transaction data.

Feature	Type  	Description	Example
total_tickets  Integer	Total support tickets for a customer	12
escalations	Integer	Number of escalated support tickets	3
avg_csat	Float	Average customer satisfaction score	3.8
avg_resolution	Float	Average ticket resolution time	18.4
total_revenue	Float	Total transaction amount for a customer	1470.50
risk_score	Float	Rule-based customer churn-risk score	82.5

Higher scores indicate greater retention risk.

### 🚀 Getting Started

Requirements
Python 3.11+
Git
pip
Streamlit

**Installation**
```
1. Clone the repository
git clone <YOUR_REPOSITORY_URL>
cd SW2627-Data-Product-Development-SupportPulse
2. Create a virtual environment
```

3. Install dependencies
```
pip install -r requirements.txt
```
4. Run the application
streamlit run app.py

The Streamlit application will display the ChurnGuard dashboard.

**🖥️ Usage Guide**

- Dataset Upload
- Open the Dataset Upload page.
- Choose a CSV or JSON file.
- Upload the dataset.
- Review the dataset overview.
- Check column validation.
- Review the data preview and statistics.
- Filtering

Use the available filters to narrow the customer dataset.

The dashboard recalculates the displayed metrics based on the selected
filters.

**KPI Monitoring**

Review:

Total Records
Total Spend
Average Spend
Churn Rate
Data Quality
Alerts

Review active alerts when metrics exceed configured thresholds.

**Customer Risk**

Use the churn-risk analysis to identify customers requiring retention
attention.

**Reports**

Generate a report from the filtered dataset and use the configured email
settings when email delivery is required.

### 🔐 Automated Data Validation

The project includes a separate validation script:

validate_data.py

The validation process checks:

- Required columns
- Numeric data types
- Minimum row count
- Fully-null columns
- Customer ID validity
- Churn status values

Run validation manually:
```
python validate_data.py data/raw/customers.csv
```
A successful validation returns exit code 0.

A failed validation returns exit code 1.

The validation workflow is designed to run through GitHub Actions.

**⚙️ Automated Data Pipeline**

The automated pipeline is implemented in:

pipeline.py

Run it manually:
```
python pipeline.py \
  --input data/raw/customers.csv \
  --output output/pipeline
```
The pipeline performs:

Ingest
  ↓
Clean
  ↓
Aggregate
  ↓
Output

The pipeline logs each stage with timestamps and status messages.

#### 📁 Project Structure
```
SupportPulse/
│
├── app.py
├── pipeline.py
├── validate_data.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│   └── raw/
│
├── pages/
│
├── scripts/
│
├── queries/
│
├── kpis/
│
├── interactive_charts/
│
├── supporting_evidence/
│
├── docs/
│
├── output/
│   └── pipeline/
│
└── .github/
    └── workflows/
```
**⚠️ Known Limitations**

The current customer risk score is rule-based rather than a trained
machine-learning model.
Risk scoring depends on the availability and quality of support and
customer data.
Dashboard functionality depends on expected column names being present
in uploaded datasets.
Missing columns can make individual filters, KPIs, or charts unavailable.
Data quality depends on the completeness of uploaded datasets.
Email report delivery requires valid SMTP configuration.
Without SMTP credentials, email delivery cannot be completed.
Alert thresholds are static and do not currently adapt automatically to
seasonal patterns.
Scheduled pipeline execution depends on successful GitHub Actions runs.
The automated pipeline currently processes CSV input.
The current validation process checks predefined schema and quality
rules rather than automatically discovering every possible data issue.

**🔮 Future Improvements**

Potential future improvements include:

Machine-learning-based churn prediction
Dynamic risk thresholds
Historical churn trend analysis
More advanced customer segmentation
Real-time data ingestion
Database-backed analytics
Automated alert notifications
Improved email delivery monitoring
Model performance monitoring
Advanced role-based access control

**📝 Documentation**

This README documents:

Project purpose
Dataset structure
Setup instructions
Application features
Pipeline architecture
Derived metrics
Validation
Automated processing
Known limitations
