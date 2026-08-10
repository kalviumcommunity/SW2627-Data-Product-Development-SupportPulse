import streamlit as st
import pandas as pd


def render_ai_churn_prediction(customers, tickets, transactions):

st.set_page_config(page_title="AI Churn Prediction", page_icon="🤖", layout="wide")

customers = pd.read_csv("data/raw/customers.csv")
tickets = pd.read_csv("data/raw/tickets.csv")
transactions = pd.read_csv("data/raw/transactions.csv")

tickets["csat_score"] = pd.to_numeric(tickets["csat_score"], errors="coerce")
tickets["resolution_time"] = pd.to_numeric(tickets["resolution_time"], errors="coerce")
tickets["escalated"] = pd.to_numeric(tickets["escalated"], errors="coerce")
transactions["amount"] = pd.to_numeric(transactions["amount"], errors="coerce")



ticket_summary = tickets.groupby("customer_id").agg(
    total_tickets=("ticket_id", "count"),
    escalations=("escalated", "sum"),
    avg_csat=("csat_score", "mean"),
    avg_resolution=("resolution_time", "mean")
).reset_index()

revenue_summary = transactions.groupby("customer_id").agg(
    total_revenue=("amount", "sum"),
    transaction_count=("amount", "count")
).reset_index()

ai_customers = customers.merge(ticket_summary, on="customer_id", how="left")
ai_customers = ai_customers.merge(revenue_summary, on="customer_id", how="left")

for column, value in {
    "total_tickets": 0,
    "escalations": 0,
    "avg_csat": 0,
    "avg_resolution": 0,
    "total_revenue": 0,
    "transaction_count": 0
}.items():
    ai_customers[column] = ai_customers[column].fillna(value)

ai_customers["risk_score"] = (
    ai_customers["churn_status"] * 40
    + ai_customers["escalations"].clip(upper=3) * 10
    + (5 - ai_customers["avg_csat"]).clip(lower=0) * 10
    + (ai_customers["avg_resolution"] / 10).clip(upper=20)
    + ai_customers["total_tickets"].clip(upper=5) * 2
).clip(0, 100)

st.title("AI Churn Prediction")
st.caption("SupportPulse AI Customer Risk Dashboard")

b1, b2 = st.columns([1, 1])
with b1:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
with b2:
    if st.button("⚡ Predict", type="primary", use_container_width=True):
        st.success("Risk scores calculated from current SupportPulse data.")

st.markdown("---")

total_customers = len(ai_customers)
churned_customers = int(ai_customers["churn_status"].sum())
churn_rate = churned_customers / total_customers * 100 if total_customers else 0
high_risk = int((ai_customers["risk_score"] >= 70).sum())
revenue_at_risk = ai_customers.loc[ai_customers["risk_score"] >= 70, "monthly_spend"].sum()

m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Churn Rate", f"{churn_rate:.1f}%")
with m2: st.metric("Customers Analysed", f"{total_customers:,}")
with m3: st.metric("High Risk Customers", f"{high_risk:,}")
with m4: st.metric("Revenue At Risk", f"${revenue_at_risk:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)
left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown("### Select Customer")
    search_customer = st.text_input("Search customer", placeholder="🔍 Search customer...", label_visibility="collapsed")
    customer_list = ai_customers.sort_values("risk_score", ascending=False).copy()
    if search_customer:
        customer_list = customer_list[customer_list["name"].astype(str).str.contains(search_customer, case=False, na=False)]

    if len(customer_list) > 0:
        options = [f"{int(r['customer_id'])} - {r['name']}" for _, r in customer_list.iterrows()]
        selected_label = st.selectbox("Customer", options, label_visibility="collapsed")
        selected_id = int(selected_label.split(" - ")[0])
        selected_customer = customer_list[customer_list["customer_id"] == selected_id].iloc[0]
    else:
        selected_customer = None
        st.warning("No customers found.")

with right_col:
    st.markdown("### Customer Risk Details")
    if selected_customer is not None:
        risk = int(round(selected_customer["risk_score"]))
        if risk >= 70:
            label, bg, color = "Critical", "#fee2e2", "#991b1b"
        elif risk >= 40:
            label, bg, color = "Medium", "#ffedd5", "#9a3412"
        else:
            label, bg, color = "Low", "#dcfce7", "#166534"

        st.markdown(f"""
        <div style="background:white;padding:24px;border-radius:12px;border:1px solid #e2e8f0;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div><h3 style="margin:0;color:#000;">{selected_customer['name']}</h3>
                <p style="color:#64748b;font-size:13px;line-height:1.7;">
                Customer ID: {int(selected_customer['customer_id'])}<br>
                Plan: {selected_customer['plan_type']}<br>
                Region: {selected_customer['region']}<br>
                Monthly Spend: ${selected_customer['monthly_spend']:,.2f}</p></div>
                <div style="text-align:right;"><span style="background:{bg};color:{color};padding:5px 12px;border-radius:15px;font-size:12px;font-weight:bold;">{label}</span>
                <div style="font-size:28px;font-weight:bold;margin-top:8px;color:#000;">{risk}%</div>
                <span style="color:#64748b;font-size:11px;">Risk Score</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("### Support Signals")
        s1, s2, s3, s4 = st.columns(4)
        with s1: st.metric("Tickets", int(selected_customer["total_tickets"]))
        with s2: st.metric("Escalations", int(selected_customer["escalations"]))
        with s3: st.metric("Avg CSAT", f"{selected_customer['avg_csat']:.2f}/5")
        with s4: st.metric("Avg Resolution", f"{selected_customer['avg_resolution']:.1f} hrs")

        st.markdown("### Customer Revenue")
        r1, r2 = st.columns(2)
        with r1: st.metric("Total Revenue", f"${selected_customer['total_revenue']:,.2f}")
        with r2: st.metric("Transactions", int(selected_customer["transaction_count"]))

        st.markdown("### Reasons Behind Prediction")
        reasons = []
        if selected_customer["churn_status"] == 1: reasons.append("⚠️ Customer is marked as churned")
        if selected_customer["escalations"] >= 2: reasons.append("📈 Multiple support escalations")
        if 0 < selected_customer["avg_csat"] < 3: reasons.append("😟 Low customer satisfaction")
        if selected_customer["avg_resolution"] > 24: reasons.append("🕒 High average resolution time")
        if selected_customer["total_tickets"] >= 5: reasons.append("🎫 High support ticket volume")
        if selected_customer["monthly_spend"] > 0: reasons.append(f"💰 Monthly spend: ${selected_customer['monthly_spend']:,.2f}")
        if not reasons: reasons.append("✅ No major risk signals detected")

        c1, c2 = st.columns(2)
        for i, reason in enumerate(reasons):
            with (c1 if i % 2 == 0 else c2):
                if any(x in reason for x in ["churned", "escalations", "Low", "High"]): st.warning(reason)
                else: st.info(reason)
    else:
        st.info("Select a customer to view their risk details.")

st.markdown("---")
with st.expander("📋 View All Customer Risk Data"):
    cols = ["customer_id", "name", "email", "plan_type", "region", "monthly_spend", "total_tickets", "escalations", "avg_csat", "avg_resolution", "total_revenue", "transaction_count", "risk_score", "churn_status"]
    cols = [c for c in cols if c in ai_customers.columns]
    display_df = ai_customers[cols].copy()
    display_df["risk_score"] = display_df["risk_score"].round(1)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
