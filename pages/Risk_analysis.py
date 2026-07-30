import streamlit as st
import pandas as pd

st.markdown("# Risk Analysis")
st.caption("Department-level risk distribution and root cause analysis")

f1, f2, f3, f4 = st.columns(4)
with f1: st.selectbox("Time", ["All", "Q1 2026", "Q4 2025"])
with f2: st.selectbox("Product", ["All", "Core Engine", "Analytics"])
with f3: st.selectbox("Region", ["All", "North America", "EMEA"])
with f4: st.selectbox("Priority", ["All", "High", "Medium", "Low"])

st.markdown("---")

col_heatmap, col_categories = st.columns([3, 2])

with col_heatmap:
    st.markdown("##### Department Risk Heatmap")
    st.caption("Customer distribution by risk level per department")
    
    dept_data = {
        "Department": ["Billing", "Technical", "Onboarding", "Account Mgmt", "Product"],
        "Low": [5, 8, 3, 12, 9],
        "Medium": [12, 9, 7, 6, 8],
        "High": [8, 6, 11, 4, 5],
        "Critical": [3, 2, 5, 1, 0]
    }
    df_dept = pd.DataFrame(dept_data).set_index("Department")
    st.bar_chart(df_dept, stack=True, color=["#22c55e", "#fbbf24", "#f97316", "#ef4444"])

with col_categories:
    st.markdown("##### Complaint Categories")
    st.caption("Distribution by issue type this quarter")
    
    cat_data = pd.DataFrame({
        "Issues": ["Billing", "Performance", "Integration", "Feature Request", "Onboarding", "Other"],
        "Count": [28, 23, 19, 17, 9, 4]
    }).set_index("Issues")
    st.bar_chart(cat_data, horizontal=True, color="#ef4444")

st.markdown("---")

col_trend, col_root = st.columns([3, 2])

with col_trend:
    st.markdown("##### Escalation Trend")
    st.caption("Monthly escalation rate — showing concerning upward trend")
    
    trend_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Escalation Rate (%)": [9.0, 9.5, 8.5, 11.2, 13.5, 15.0]
    }).set_index("Month")
    st.line_chart(trend_data, color="#ef4444")

with col_root:
    st.markdown("##### Root Cause Analysis")
    st.caption("Top contributing factors to customer churn this quarter")
    
    st.markdown("""
        * **Unresolved billing disputes** — 28 customers **34%**
        * **Slow technical support** — 22 customers **28%**
        * **Onboarding gaps** — 17 customers **21%**
        * **Missing product features** — 9 customers **12%**
    """)