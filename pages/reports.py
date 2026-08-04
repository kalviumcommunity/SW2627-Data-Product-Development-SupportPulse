import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Reports - ChurnGuard", page_icon="📄", layout="wide")

# Top header / action row
col_title, col_actions = st.columns([3, 1])
with col_title:
    st.markdown("## Reports")
    st.caption("Analytics reports and data exports")
with col_actions:
    cols_btn = st.columns(2)
    with cols_btn[0]:
        st.button("📥 Download PDF")
    with cols_btn[1]:
        st.button("📊 Export Excel", type="primary")

st.markdown("---")

# Report Sub-tabs filter simulation
tab1, tab2, tab3, tab4 = st.tabs(["Weekly Report", "Monthly Report", "Department Report", "Churn Forecast"])

with tab1:
    st.write("")
    # Top charts row
    c_chart1, c_chart2 = st.columns(2)
    
    with c_chart1:
        with st.container(border=True):
            st.markdown("##### Churn Trend — This Week")
            st.caption("Actual vs predicted churn rate")
            trend_df = pd.DataFrame({"Month": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], "Actual": [2, 2.2, 3, 2.8, 3.8, 4.4]})
            fig = px.line(trend_df, x="Month", y="Actual", markers=True)
            fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)
            
    with c_chart2:
        with st.container(border=True):
            st.markdown("##### Risk Distribution")
            st.caption("Customer count by risk level")
            risk_df = pd.DataFrame({"Risk Level": ["Healthy", "Low Risk", "Medium", "High Risk", "Critical"], "Count": [330, 470, 280, 110, 30]})
            fig2 = px.bar(risk_df, x="Risk Level", y="Count", color="Risk Level", color_discrete_map={"Healthy": "#10B981", "Low Risk": "#3B82F6", "Medium": "#F59E0B", "High Risk": "#F97316", "Critical": "#EF4444"})
            fig2.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    # Bottom analytics row
    c_chart3, c_chart4 = st.columns(2)
    with c_chart3:
        with st.container(border=True):
            st.markdown("##### Resolution Performance")
            st.caption("Avg resolution time by category (days)")
            st.write("Billing (Target: 2d): **4.2d**")
            st.progress(80)
            st.write("Technical (Target: 1.5d): **3.1d**")
            st.progress(65)
            st.write("Onboarding (Target: 3d): **6.8d**")
            st.progress(95)
            st.write("Product (Target: 2d): **2.4d**")
            st.progress(50)

    with c_chart4:
        with st.container(border=True):
            st.markdown("##### Complaint Distribution")
            st.caption("By category — this quarter")
            pie_data = pd.DataFrame({"Category": ["Billing", "Performance", "Integration", "Onboarding", "Other"], "Value": [28, 22, 19, 10, 5]})
            fig3 = px.pie(pie_data, names="Category", values="Value", hole=0.6)
            fig3.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="white")
            st.plotly_chart(fig3, use_container_width=True)