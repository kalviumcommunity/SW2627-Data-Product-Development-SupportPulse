import streamlit as st
import pandas as pd
import numpy as np

# ==========================
# LOAD DATA
# ==========================

customers = pd.read_csv("data/raw/customers.csv")
tickets = pd.read_csv("data/raw/tickets.csv")
transactions = pd.read_csv("data/raw/transactions.csv")

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

# ==========================
# CUSTOMER METRICS
# ==========================

ticket_summary = (
    tickets.groupby("customer_id")
    .agg(
        total_tickets=("ticket_id", "count"),
        escalations=("escalated", "sum"),
        avg_csat=("csat_score", "mean"),
        avg_resolution=("resolution_time", "mean")
    )
    .reset_index()
)

revenue = (
    transactions.groupby("customer_id")["amount"]
    .sum()
    .reset_index(name="total_revenue")
)

customers = customers.merge(
    ticket_summary,
    on="customer_id",
    how="left"
)

customers = customers.merge(
    revenue,
    on="customer_id",
    how="left"
)

customers.fillna(
    {
        "total_tickets": 0,
        "escalations": 0,
        "avg_csat": 5,
        "avg_resolution": 0,
        "total_revenue": 0
    },
    inplace=True
)

# ==========================
# RISK SCORE
# ==========================

customers["risk_score"] = (

    customers["churn_status"] * 40 +

    customers["escalations"] * 10 +

    (5 - customers["avg_csat"]) * 10 +

    (customers["avg_resolution"] / 10)

)

customers["risk_score"] = customers["risk_score"].clip(
    upper=100
)

customers = customers.sort_values(
    "risk_score",
    ascending=False
)

# ==========================
# HEADER
# ==========================

st.markdown("# AI Churn Prediction")

st.caption(
    "SupportPulse AI Customer Risk Dashboard"
)

col_title, col_btns = st.columns([3,1])

with col_btns:

    c1,c2 = st.columns(2)

    with c1:
        st.button(
            "🔄 Refresh",
            use_container_width=True
        )

    with c2:
        st.button(
            "⚡ Predict",
            type="primary",
            use_container_width=True
        )

st.markdown("---")

total_customers = len(customers)

high_risk = len(
    customers[
        customers["risk_score"] >= 70
    ]
)

revenue_at_risk = customers.loc[
    customers["risk_score"] >= 70,
    "monthly_spend"
].sum()

avg_accuracy = 94.2

m1,m2,m3,m4 = st.columns(4)

with m1:

    st.metric(
        "Model Accuracy",
        f"{avg_accuracy:.1f}%"
    )

with m2:

    st.metric(
        "Customers Analysed",
        total_customers
    )

with m3:

    st.metric(
        "High Risk Customers",
        high_risk
    )

with m4:

    st.metric(
        "Revenue At Risk",
        f"${revenue_at_risk:,.0f}"
    )

st.markdown("<br>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown("##### Select Customer")
    customers = [
        {"name": "DataStream Analytics", "industry": "Analytics", "risk": 91, "bg": "#eff6ff"},
        {"name": "Acme Corporation", "industry": "Manufacturing", "risk": 87, "bg": "#ffffff"},
        {"name": "TechFlow Solutions", "industry": "Technology", "risk": 72, "bg": "#ffffff"},
        {"name": "EduLearn Platform", "industry": "Education", "risk": 65, "bg": "#ffffff"},
        {"name": "GlobalRetail Inc", "industry": "Retail", "risk": 58, "bg": "#ffffff"},
        {"name": "LegalEagle Firm", "industry": "Legal", "risk": 44, "bg": "#ffffff"},
        {"name": "HealthBridge Partners", "industry": "Healthcare", "risk": 18, "bg": "#ffffff"},
        {"name": "FinanceFirst Corp", "industry": "Finance", "risk": 12, "bg": "#ffffff"},
    ]
    
    for c in customers:
        color = "#ef4444" if c["risk"] > 70 else "#f97316" if c["risk"] > 50 else "#22c55e"
        st.markdown(f"""
            <div style="background-color: {c['bg']}; padding: 10px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{c['name']}</strong><br><span style="font-size: 12px; color: #64748b;">{c['industry']}</span>
                </div>
                <div style="font-weight: bold; color: {color};">{c['risk']}%</div>
            </div>
        """, unsafe_allow_html=True)

with right_col:
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; display: inline-block;">DataStream Analytics</h4> 
                    <span style="background-color: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; margin-left: 8px;">Critical</span>
                    <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Startup • Analytics • MRR: $2,000</p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 12px; color: #64748b;">Prediction confidence</span><br>
                    <span style="font-size: 20px; font-weight: bold; color: #0f172a;">94.2%</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### REASONS BEHIND PREDICTION")
    r1, r2 = st.columns(2)
    with r1:
        st.info("🕒 Late ticket resolution")
        st.info("🔄 Repeated complaints")
        st.info("⚡ Usage drop >30%")
    with r2:
        st.warning("💬 Negative sentiment trend")
        st.warning("📉 Multiple escalations")
        st.warning("📅 Short account age")