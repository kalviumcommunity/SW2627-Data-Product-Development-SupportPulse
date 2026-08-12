import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_export_integration import render_export_section
import os
from alert_config import ALERT_THRESHOLDS
from utils.kpi_utils import (
    calculate_kpis,
    get_trend_indicator
)

metrics = pd.read_csv("output/dashboard_metrics.csv")

customers = pd.read_csv(
    "data/processed/feature_engineered_customers.csv"
)

tickets = pd.read_csv(
    "data/processed/feature_engineered_tickets.csv"
)

transactions = pd.read_csv(
    "data/raw/transactions.csv"
)

kpis = calculate_kpis(
    customers,
    tickets,
    transactions
)

st.set_page_config(
    page_title="ChurnGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
@st.cache_data
def load_uploaded_data(file_bytes, file_name):
    """
    Load an uploaded CSV or JSON file.

    Streamlit caches the DataFrame using the file content
    and file name, so filter changes do not reload the file.
    """

    if file_name.lower().endswith(".csv"):
        from io import BytesIO
        return pd.read_csv(BytesIO(file_bytes))

    elif file_name.lower().endswith(".json"):
        from io import BytesIO
        return pd.read_json(BytesIO(file_bytes))

    raise ValueError(
        "Unsupported file type. Please upload CSV or JSON."
    )

# ==========================================
# ALERT CHECKING
# ==========================================

def check_alerts(metrics_dict, thresholds):
    """
    Compare current KPI values against configured
    thresholds and return triggered alerts.
    """

    triggered = []

    for key, config in thresholds.items():

        if key not in metrics_dict:
            continue

        value = metrics_dict[key]
        threshold = config["threshold"]

        breached = False

        if (
            config["direction"] == "above"
            and value > threshold
        ):
            breached = True

        elif (
            config["direction"] == "below"
            and value < threshold
        ):
            breached = True

        if breached:

            triggered.append({
                "metric": config["metric"],
                "value": value,
                "threshold": threshold,
                "severity": config["severity"],
                "message": config["message"]
            })

    return triggered
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CSS Styles ----------------
st.markdown("""
<style>

    /* Fix text inside dark chart/element containers */
    .stPlotlyChart text {
        fill: #000000 !important;
        color: #000000 !important;
    }

    /* Streamlit dataframe/table text */
    [data-testid="stDataFrame"] * {
        color: #000000 !important;
    }

    /* General text inside app elements */
    [data-testid="stVerticalBlock"] p,
    [data-testid="stVerticalBlock"] span,
    [data-testid="stVerticalBlock"] label {
        color: #000000 !important;
    }

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}


.stApp{
    background:#f7f8fc;
}

[data-testid="stSidebar"]{
    background:white;
    border-right:1px solid #ececec;
}

.metric-card{
    background:white;
    border:1px solid #ededed;
    border-radius:14px;
    padding:18px;
    box-shadow:0px 1px 6px rgba(0,0,0,.05);
}

.metric-title{
    color:#7b8190;
    font-size:13px;
}

.metric-value{
    font-size:34px;
    font-weight:700;
}

.metric-change-red{
    color:#ef4444;
    font-size:12px;
    float:right;
}

.metric-change-green{
    color:#22c55e;
    font-size:12px;
    float:right;
}

.custom-table {
    background-color: #FFFFFF;
    border: 1px solid #EDEDED;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0px 1px 6px rgba(0,0,0,.05);
}
/* Make all text black */
html, body, .stApp,
p, span, div, label,
h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* Streamlit widgets */
.stTextInput input,
.stSelectbox,
.stSelectbox div,
.stMultiSelect,
.stButton button,
.stMarkdown,
.stCaption,
.stMetric,
.stDataFrame,
.stTable {
    color: #000000 !important;
}

/* Placeholder text */
input::placeholder {
    color: #000000 !important;
    opacity: 1;
}

/* Dropdown selected value */
[data-baseweb="select"] div {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar Routing ----------------
with st.sidebar:
    st.markdown("""
<h2 style="color:#000000; margin-bottom:0;">
🛡️ ChurnGuard
</h2>

<p style="color:#000000; font-size:14px; margin-top:2px;">
AI Retention Platform
</p>
""", unsafe_allow_html=True)

    selected = option_menu(
        "",
        [
            "Dashboard",
            "Customers",
            "Support Tickets",
            "AI Churn Prediction",
            "Risk Analysis",
            "Escalations",
            "Customer Timeline",
            "Recommendations",
            "Reports",
            "Settings",
            "Dataset Upload",
            "Session State",
        ],
        icons=[
    "grid",
    "people",
    "ticket",
    "robot",
    "exclamation-triangle",
    "graph-up",
    "clock-history",
    "lightbulb",
    "file-earmark-text",
    "gear",
    "cloud-upload",
    "arrow-repeat"
],
        default_index=0,
        styles={
            "container": {
                "padding": "0",
                "background": "white"
            },
            "icon": {
                "color": "#2563EB",
                "font-size": "16px"
            },
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px",
                "border-radius": "10px",
                "--hover-color": "#EEF4FF",
                "color": "#000000",
            },
            "nav-link-selected": {
                "background": "#EEF4FF",
                "color": "#000000",
                "font-weight": "600",
            }
        }
    )

    st.markdown("---")
    st.write("**Alex Morgan**")
    st.caption("Support Manager")

# ---------------- Top Global Header ----------------
col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    st.text_input("", placeholder="🔍 Search customers, tickets...", label_visibility="collapsed", key="global_search_input")

with col2:
    if st.button("🔄 Refresh", key="global_refresh_btn"):
        st.rerun()

with col3:
    if st.button("⬇ Export", key="global_export_btn"):
        st.toast("Exporting data...")

# ==========================================
# PAGE: DASHBOARD
# ==========================================
if selected == "Dashboard":

    st.markdown("""
    <h1 style="color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;">Dashboard</h1>
    <p style="color:#6B7280; font-size:16px; margin-top:0px;">
        Overview of churn risk and support health
    </p>
    """, unsafe_allow_html=True)

    ccards = st.columns(5)

    kpis = calculate_kpis(
        customers,
        tickets,
        transactions
    )

    values = []

    icons = {
        "Revenue": "💰",
        "Active Customers": "👥",
        "Average Order Value": "🛒",
        "Churn Rate": "⚠",
        "Customer Satisfaction": "⭐"
    }

    for metric in [
        "Revenue",
        "Active Customers",
        "Average Order Value",
        "Churn Rate",
        "Customer Satisfaction"
    ]:

        current, change = kpis[metric]

        inverse = metric == "Churn Rate"

        arrow, color = get_trend_indicator(
            change,
            inverse=inverse
        )

        if metric == "Revenue":
            value = f"${current:,.0f}"

        elif metric == "Average Order Value":
            value = f"${current:.2f}"

        elif metric == "Churn Rate":
            value = f"{current:.1f}%"

        elif metric == "Customer Satisfaction":
            value = f"{current:.2f}/5"

        else:
            value = f"{int(current)}"

        values.append(
            (
                icons[metric],
                value,
                metric,
                f"{arrow} {change:.1f}%",
                color
            )
        )

    for col, (icon, val, title, change, color) in zip(ccards, values):

        with col:

            cls = (
                "metric-change-red"
                if color == "red"
                else "metric-change-green"
            )

            st.markdown(
                f"""
                <div class="metric-card">
                    <span>{icon}</span>
                    <span class="{cls}">{change}</span>
                    <div class="metric-value">{val}</div>
                    <div class="metric-title">{title}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    customers["signup_date"] = pd.to_datetime(
        customers["signup_date"]
    )

    trend = (
        customers.groupby(
            customers["signup_date"].dt.to_period("M")
        )
        .size()
        .reset_index(name="Customers")
    )

    trend["signup_date"] = trend["signup_date"].astype(str)

    left, right = st.columns(2)

    # -----------------------------
    # Monthly Trend
    # -----------------------------
    with left:

        st.markdown("### Monthly Customer Trend")

        fig = px.line(
            trend,
            x="signup_date",
            y="Customers",
            markers=True,
            title="Monthly Customer Trend"
        )

        fig.update_traces(
            hovertemplate=
            "<b>Month:</b> %{x}<br>"
            "<b>Customers:</b> %{y}<extra></extra>",
            line=dict(
                width=4,
                color="#2563EB"
            )
        )

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=[
                    dict(
                        count=3,
                        label="3M",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(
                        count=6,
                        label="6M",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(step="all")
                    ]
                )
            )

        fig.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode="x unified",
            dragmode="zoom",
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Complaint Categories
    # -----------------------------
    with right:

        st.markdown("### Complaint Categories")

        pie = (
            tickets["ticket_category"]
            .value_counts()
            .reset_index()
        )

        pie.columns = [
            "Category",
            "Value"
        ]

        fig2 = px.pie(
            pie,
            names="Category",
            values="Value",
            hole=0.72,
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig2.update_traces(
            hovertemplate=
            "<b>%{label}</b><br>"
            "Tickets: %{value}<br>"
            "Percentage: %{percent}<extra></extra>"
        )

        fig2.update_layout(
            height=420,
            paper_bgcolor="white",
            margin=dict(
                l=0,
                r=0,
                t=10,
                b=0
            ),
            showlegend=True
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

            # ==========================================
    # REPORT EXPORT
    # ==========================================

    st.markdown("---")

    render_export_section(
        customers,
        tickets,
        transactions
    )
# ==========================================
# PAGE: CUSTOMERS
# ==========================================
elif selected == "Customers":
    st.markdown("""
    <h1 style="color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;">Customers</h1>
    <p style="color:#6B7280; font-size:16px; margin-top:0px;">Manage and monitor your customer accounts</p>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns([4, 1, 1, 1])
    with f1:
        st.text_input("Search filter", placeholder="🔍 Search by name or contact...", label_visibility="collapsed", key="customers_search")
    with f2:
        st.selectbox("Industry", ["All Industries"], label_visibility="collapsed")
    with f3:
        st.selectbox("Risk", ["All Risk Levels"], label_visibility="collapsed")
    with f4:
        st.markdown("<div style='padding-top: 8px; font-size: 14px; color: #6B7280;'>8 of 8 customers</div>", unsafe_allow_html=True)

    st.write("")

    customers_data = customers.copy()

    st.markdown("""
        <div class="custom-table">
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
                <tr style="border-bottom: 1px solid #EDEDED; color: #6B7280; background-color: #FAFAFA;">
                    <th style="padding: 12px 16px;">Customer</th>
                    <th style="padding: 12px 16px;">Industry / Region</th>
                    <th style="padding: 12px 16px;">Open Tickets</th>
                    <th style="padding: 12px 16px;">Avg Resolution</th>
                    <th style="padding: 12px 16px;">Escalations</th>
                    <th style="padding: 12px 16px;">AI Risk Score</th>
                    <th style="padding: 12px 16px;">Health Score</th>
                    <th style="padding: 12px 16px;">Status</th>
                    <th style="padding: 12px 16px;"></th>
                </tr>
    """, unsafe_allow_html=True)

    for _, c in customers_data.iterrows():
        status_color = "#EF4444" if c["churn_status"] == 1 else "#22C55E"
        risk_color = "#EF4444" if c["churn_status"] == 1 else "#22C55E"
        
        st.markdown(f"""
                <tr style="border-bottom: 1px solid #F3F4F6;">
                    <td style="padding: 12px 16px;">
                        <b>{c['name']}</b><br><span style="font-size: 11px; color: #6B7280;">{c["email"]}</span>
                    </td>
                    <td style="padding: 12px 16px; color: #4B5563;">
                        {c["plan_type"]}<br><span style="font-size: 11px; color: #9CA3AF;">{c['region']}</span>
                    </td>
                    <td style="padding: 12px 16px; color: #EF4444; font-weight: bold;">{tickets[
tickets.customer_id == c.customer_id
].shape[0]}</td>
                    <td style="padding: 12px 16px; color: #4B5563;">{round(
tickets[
tickets.customer_id==c.customer_id
]["resolution_time"].mean(),
1
)}</td>
                    <td style="padding: 12px 16px; color: #EF4444; font-weight: bold;">{tickets[
(tickets.customer_id==c.customer_id)
&
(tickets.escalated==True)
].shape[0]}</td>
                    <td style="padding: 12px 16px;"><span style="background: #FEF2F2; color: {risk_color}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{"High" if c["churn_status"]==1 else "Low"}</span></td>
                    <td style="padding: 12px 16px; color: #374151;">{max(0,100-int(c["tenure_days"]//10))}</td>
                    <td style="padding: 12px 16px;"><span style="background: #FEE2E2; color: {status_color}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{"Churned"
if c["churn_status"]==1
else "Active"}</span></td>
                    <td style="padding: 12px 16px; color: #9CA3AF;">›</td>
                </tr>
        """, unsafe_allow_html=True)

    st.markdown("</table></div>", unsafe_allow_html=True)

# ==========================================
# PAGE: SUPPORT TICKETS
# ==========================================
elif selected == "Support Tickets":
    st.markdown("""
    <h1 style="color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;">Support Tickets</h1>
    <p style="color:#6B7280; font-size:16px; margin-top:0px;">8 active tickets — 4 escalated</p>
    """, unsafe_allow_html=True)

    s1, s2 = st.columns([5, 1])
    with s1:
        st.text_input("Ticket search", placeholder="🔍 Search by ticket ID, customer, or issue...", label_visibility="collapsed", key="tickets_search")
    with s2:
        st.selectbox("Status", ["All Status"], label_visibility="collapsed")

    st.write("")

    tickets_data = tickets.copy()

    st.markdown("""
        <div class="custom-table">
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
                <tr style="border-bottom: 1px solid #EDEDED; color: #6B7280; background-color: #FAFAFA;">
                    <th style="padding: 12px 16px;">Ticket ID</th>
                    <th style="padding: 12px 16px;">Customer</th>
                    <th style="padding: 12px 16px;">Issue Category</th>
                    <th style="padding: 12px 16px;">Priority</th>
                    <th style="padding: 12px 16px;">Status</th>
                    <th style="padding: 12px 16px;">Agent</th>
                    <th style="padding: 12px 16px;">Resolution Time</th>
                    <th style="padding: 12px 16px;">Escalated</th>
                    <th style="padding: 12px 16px;">Sentiment</th>
                </tr>
    """, unsafe_allow_html=True)

    for _, t in tickets_data.iterrows():
        priority_color = "#EF4444" if t["priority"] in ["Critical", "High"] else "#F59E0B"
        status_color = "#22C55E" if t["resolved"] else "#EF4444"
        escalated_color = "#EF4444" if t["escalated"] == "Yes" else "#6B7280"

        st.markdown(f"""
                <tr style="border-bottom: 1px solid #F3F4F6;">
                    <td style="padding: 12px 16px; color: #2563EB; font-weight: bold;">{t["ticket_id"]}</td>
                    <td style="padding: 12px 16px; font-weight: 500;">{customers.loc[
customers.customer_id==t.customer_id,
"name"
].values[0]}</td>
                    <td style="padding: 12px 16px; color: #4B5563;">{t["ticket_category"]}</td>
                    <td style="padding: 12px 16px; color: {priority_color}; font-weight: bold;">{t['priority']}</td>
                    <td style="padding: 12px 16px;"><span style="background: #EFF6FF; color: {status_color}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{"Resolved"
if t["resolved"]
else "Open"}</span></td>
                    <td style="padding: 12px 16px; color: #4B5563;">Support Team</td>
                    <td style="padding: 12px 16px; color: #EF4444;">{f'{t["resolution_time"]} hrs'}</td>
                    <td style="padding: 12px 16px; color: {escalated_color}; font-weight: bold;">{"Yes"
if t["escalated"]
else "No"}</td>
                    <td style="padding: 12px 16px; color: #EF4444;">Neutral</td>
                </tr>
        """, unsafe_allow_html=True)

    st.markdown("</table></div>", unsafe_allow_html=True)

# ==========================================
# PAGE: AI CHURN PREDICTION
# ==========================================
elif selected == "AI Churn Prediction":
    col_title, col_btns = st.columns([3, 1])
    with col_title:
        st.markdown("<h1 style='color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;'>AI Churn Prediction</h1>", unsafe_allow_html=True)
        st.caption("Powered by gradient boosting ensemble — last trained Dec 12, 2023")
    with col_btns:
        b1, b2 = st.columns(2)
        with b1:
            st.button("🔄 Retrain Model", key="retrain_model_btn", use_container_width=True)
        with b2:
            st.button("⚡ Run Batch", key="run_batch_btn", type="primary", use_container_width=True)

    st.markdown("---")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('''<div class="metric-card"><div class="metric-title">Model Accuracy</div><div class="metric-value">94.2%</div></div>''', unsafe_allow_html=True)
    with m2:
        st.markdown('''<div class="metric-card"><div class="metric-title">Customers Analyzed</div><div class="metric-value">1,247</div></div>''', unsafe_allow_html=True)
    with m3:
        st.markdown('''<div class="metric-card"><div class="metric-title">High Risk (>70%)</div><div class="metric-value" style="color:#ef4444;">38</div></div>''', unsafe_allow_html=True)
    with m4:
        st.markdown('''<div class="metric-card"><div class="metric-title">Revenue at Risk</div><div class="metric-value" style="color:#f97316;">$284K</div></div>''', unsafe_allow_html=True)

    st.write("")
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown("### Select Customer")
        customers_list = [
            {"name": "DataStream Analytics", "ind": "Analytics", "risk": 91},
            {"name": "Acme Corporation", "ind": "Manufacturing", "risk": 87},
            {"name": "TechFlow Solutions", "ind": "Technology", "risk": 72},
            {"name": "EduLearn Platform", "ind": "Education", "risk": 65},
            {"name": "GlobalRetail Inc", "ind": "Retail", "risk": 58},
            {"name": "LegalEagle Firm", "ind": "Legal", "risk": 44},
            {"name": "HealthBridge Partners", "ind": "Healthcare", "risk": 18},
            {"name": "FinanceFirst Corp", "ind": "Finance", "risk": 12},
        ]
        for c in customers_list:
            bg_col = "#eff6ff" if c["name"] == "DataStream Analytics" else "#ffffff"
            risk_col = "#ef4444" if c["risk"] > 70 else ("#f97316" if c["risk"] > 50 else "#22c55e")
            st.markdown(f'''
                <div style="background-color: {bg_col}; padding: 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #ededed; display: flex; justify-content: space-between; align-items: center;">
                    <div><b>{c['name']}</b><br><span style="font-size: 11px; color: #6b7280;">{c['ind']}</span></div>
                    <div style="font-weight: bold; color: {risk_col};">{c['risk']}%</div>
                </div>
            ''', unsafe_allow_html=True)

    with right_col:
        st.markdown('''
            <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #ededed;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; display: inline-block;">DataStream Analytics</h3>
                        <span style="background-color: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; margin-left: 8px;">Critical</span>
                        <p style="color: #6b7280; font-size: 13px; margin: 4px 0 0 0;">Startup • Analytics • MRR: $2,000</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 11px; color: #6b7280;">Prediction confidence</span><br>
                        <span style="font-size: 20px; font-weight: bold; color: #0f172a;">94.2%</span>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        st.write("")
        st.markdown("### Reasons Behind Prediction")
        r1, r2 = st.columns(2)
        with r1:
            st.info("🕒 Late ticket resolution")
            st.info("🔄 Repeated complaints")
            st.info("⚡ Usage drop >30%")
        with r2:
            st.warning("💬 Negative sentiment trend")
            st.warning("📉 Multiple escalations")
            st.warning("📅 Short account age")

# ==========================================
# PAGE: RISK ANALYSIS
# ==========================================
elif selected == "Risk Analysis":
    st.markdown("<h1 style='color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;'>Risk Analysis</h1>", unsafe_allow_html=True)
    st.caption("Department-level risk distribution and root cause analysis")

    f1, f2, f3, f4 = st.columns(4)
    with f1: st.selectbox("Time", ["All", "Q1 2026", "Q4 2025"], label_visibility="collapsed")
    with f2: st.selectbox("Product", ["All", "Core Engine", "Analytics"], label_visibility="collapsed")
    with f3: st.selectbox("Region", ["All", "North America", "EMEA"], label_visibility="collapsed")
    with f4: st.selectbox("Priority", ["All", "High", "Medium", "Low"], label_visibility="collapsed")

    st.write("")
    col_heatmap, col_categories = st.columns([3, 2])

    with col_heatmap:
        st.markdown("### Department Risk Heatmap")
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
        st.markdown("### Complaint Categories")
        cat_data = pd.DataFrame({
            "Issues": ["Billing", "Performance", "Integration", "Feature Request", "Onboarding", "Other"],
            "Count": [28, 23, 19, 17, 9, 4]
        }).set_index("Issues")
        st.bar_chart(cat_data, horizontal=True, color="#ef4444")

    st.write("")
    col_trend, col_root = st.columns([3, 2])

    with col_trend:
        st.markdown("### Escalation Trend")
        trend_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Escalation Rate (%)": [9.0, 9.5, 8.5, 11.2, 13.5, 15.0]
        }).set_index("Month")
        st.line_chart(trend_data, color="#ef4444")

    with col_root:
        st.markdown("### Root Cause Analysis")
        st.markdown("""
            * **Unresolved billing disputes** — 28 customers (**34%**)
            * **Slow technical support** — 22 customers (**28%**)
            * **Onboarding gaps** — 17 customers (**21%**)
            * **Missing product features** — 9 customers (**12%**)
        """)

# ==========================================
# PAGE: ESCALATIONS
# ==========================================
elif selected == "Escalations":
    col_title, col_search, col_actions = st.columns([2, 2, 1])
    with col_title:
        st.markdown("## Escalations")
        st.caption("4 active escalations requiring attention")
    with col_search:
        st.text_input("Search esc", placeholder="🔍 Search customers, tickets...", label_visibility="collapsed", key="escalations_search")
    with col_actions:
        cols_btn = st.columns(2)
        with cols_btn[0]:
            st.markdown("🔔")
        with cols_btn[1]:
            st.button("📥 Export", key="escalations_export_btn", use_container_width=True)

    st.markdown("---")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Critical Escalations", value="2", delta="Action Required", delta_color="inverse")
    with m2:
        st.metric(label="Overdue Tickets", value="3")
    with m3:
        st.metric(label="Unassigned", value="0")

    st.markdown("<br>", unsafe_allow_html=True)

    data = {
        "Ticket ID": ["TKT-2847", "TKT-2843", "TKT-2821", "TKT-2815"],
        "Customer": ["Acme Corporation", "DataStream Analytics", "LegalEagle Firm", "DataStream Analytics"],
        "Issue": ["Billing Dispute", "API Integration Failure", "Compliance Feature", "Onboarding Blockers"],
        "Priority": ["High", "Critical", "Medium", "Critical"],
        "Status": ["Open", "Escalated", "Pending", "Open"],
        "Agent": ["Sarah M.", "Tom R.", "Sarah M.", "Tom R."],
        "Time Overdue": ["Overdue (8d)", "Overdue (12d)", "4d", "Overdue (21d)"],
        "Sentiment": ["Negative", "Very Negative", "Neutral", "Very Negative"]
    }

    df_esc = pd.DataFrame(data)

    for index, row in df_esc.iterrows():
        c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([1.2, 2, 2.2, 1, 1, 1.2, 1.5, 1.2, 1])
        c1.write(f"**{row['Ticket ID']}**")
        c2.write(row['Customer'])
        c3.write(row['Issue'])
        
        if row['Priority'] == 'Critical':
            c4.markdown(":red[**Critical**]")
        elif row['Priority'] == 'High':
            c4.markdown(":orange[**High**]")
        else:
            c4.markdown(":blue[Medium]")
            
        c5.write(row['Status'])
        c6.write(row['Agent'])
        
        if "Overdue" in row['Time Overdue']:
            c7.markdown(f":red[{row['Time Overdue']}]")
        else:
            c7.write(row['Time Overdue'])
            
        c8.write(row['Sentiment'])
        
        with c9:
            if st.button("Assign", key=f"btn_{row['Ticket ID']}"):
                st.toast(f"Assigned {row['Ticket ID']}")
        st.markdown("<hr style='margin: 4px 0px; opacity: 0.2;'>", unsafe_allow_html=True)

# ==========================================
# PAGE: CUSTOMER TIMELINE
# ==========================================
elif selected == "Customer Timeline":
    col_title, col_search = st.columns([3, 1])
    with col_title:
        st.markdown("## Customer Timeline")
        st.caption("Complete interaction history and event log")
    with col_search:
        st.selectbox("Select Customer", ["Acme Corporation", "DataStream Analytics", "LegalEagle Firm"], label_visibility="collapsed")

    st.markdown("---")

    left_col, right_col = st.columns([1, 2.2])

    with left_col:
        with st.container(border=True):
            st.markdown("### 🔴 Acme Corporation")
            st.caption("Critical Status Account")
            st.markdown("---")
            
            col_a, col_b = st.columns(2)
            col_a.markdown("**Joined**")
            col_b.markdown("Jun 12, 2023")
            
            col_a, col_b = st.columns(2)
            col_a.markdown("**Subscription**")
            col_b.markdown("Enterprise")
            
            col_a, col_b = st.columns(2)
            col_a.markdown("**Account Age**")
            col_b.markdown("18 months")
            
            col_a, col_b = st.columns(2)
            col_a.markdown("**Total Tickets**")
            col_b.markdown("14")
            
            col_a, col_b = st.columns(2)
            col_a.markdown("**Escalations**")
            col_b.markdown("3")

        with st.container(border=True):
            st.markdown("##### EVENT TYPES")
            st.markdown("🔵 Onboarding &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1**")
            st.markdown("🔘 Support Ticket &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **6**")
            st.markdown("🟠 Complaint &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **3**")
            st.markdown("🔴 Escalation &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2**")
            st.markdown("🟢 Retention Action &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **2**")
            st.markdown("🟣 AI Alert &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **1**")

    with right_col:
        st.markdown("### Interaction Timeline")
        
        timeline_events = [
            ("Jun 12, 2023", "Customer Onboarded", "Enterprise plan activated. Onboarding call completed successfully.", "blue"),
            ("Jul 28, 2023", "First Support Ticket", "Minor API configuration issue. Resolved in 2 days by technical team.", "gray"),
            ("Sep 15, 2023", "Repeated Complaint", "Billing discrepancy reported for the second time this quarter.", "orange"),
            ("Oct 22, 2023", "Escalation Event", "Billing dispute escalated to senior account manager after 14 days.", "red"),
            ("Nov 3, 2023", "Retention Call Held", "30-minute call. Customer expressed frustration about resolution speed.", "purple"),
            ("Nov 18, 2023", "AI Warning Issued", "Churn probability exceeded 70% threshold. Automated alert sent to team.", "orange")
        ]

        for date, title, desc, color in timeline_events:
            with st.container(border=True):
                col_date, col_content = st.columns([1, 4])
                col_date.markdown(f"**{date}**")
                col_content.markdown(f"**{title}**")
                col_content.caption(desc)

# ==========================================
# PAGE: RECOMMENDATIONS
# ==========================================
elif selected == "Recommendations":
    col_title, col_search, col_actions = st.columns([2, 2, 1])
    with col_title:
        st.markdown("## AI Recommendations")
        st.caption("Prioritized retention actions generated by AI — updated Dec 14, 2023")
    with col_search:
        st.text_input("", placeholder="🔍 Search customers, tickets...", label_visibility="collapsed", key="recommendations_search")
    with col_actions:
        cols_btn = st.columns(2)
        with cols_btn[0]:
            st.button("🔄 Refresh", key="rec_refresh_btn")
        with cols_btn[1]:
            st.button("📥 Export Plan", key="rec_export_btn", use_container_width=True)

    st.markdown("---")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Customers Requiring Action", value="3", delta="High + Critical risk", delta_color="inverse")
    with m2:
        st.metric(label="Est. Churn Reduction", value="-34%", delta="With full plan execution", delta_color="normal")
    with m3:
        st.metric(label="Revenue Protected", value="$284K", delta="At-risk MRR this quarter", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        c_head1, c_head2 = st.columns([4, 1])
        with c_head1:
            st.markdown("### 🔴 DataStream Analytics")
            st.caption("Critical • Analytics • MRR $2,000")
        with c_head2:
            st.markdown("<div style='text-align: right; color: #EF4444; font-weight: bold;'>Churn Risk<br><span style='font-size: 24px;'>91%</span></div>", unsafe_allow_html=True)
        
        st.info("⚠️ 4 escalations in 30 days. Onboarding issues unresolved for 3 weeks. Extremely high churn probability.")
        
        b1, b2, b3, b4 = st.columns(4)
        with b1: st.button("👤 Assign Agent", key="btn_rec_1")
        with b2: st.button("🏷️ Send Offer", key="btn_rec_2")
        with b3: st.button("📅 Schedule Meeting", key="btn_rec_3")
        with b4: st.button("✉️ Generate Email", key="btn_rec_4")
        
        st.markdown("---")
        f_col1, f_col2 = st.columns([2, 2])
        f_col1.caption("Est. revenue at risk: **$24,000/yr**")
        f_col2.markdown("<div style='text-align: right; color: #10B981; font-size: 13px;'>Estimated churn reduction if acted: <b>-28%</b></div>", unsafe_allow_html=True)

    with st.container(border=True):
        c_head1, c_head2 = st.columns([4, 1])
        with c_head1:
            st.markdown("### 🔴 Acme Corporation")
            st.caption("Critical • Manufacturing • MRR $4,000")
        with c_head2:
            st.markdown("<div style='text-align: right; color: #EF4444; font-weight: bold;'>Churn Risk<br><span style='font-size: 24px;'>87%</span></div>", unsafe_allow_html=True)
        
        st.info("⚠️ High escalation rate with repeated billing complaints. 3 unresolved tickets in the past 30 days indicate serious dissatisfaction.")
        
        b1, b2, b3, b4 = st.columns(4)
        with b1: st.button("👤 Assign Agent", key="btn_rec_5")
        with b2: st.button("🏷️ Send Offer", key="btn_rec_6")
        with b3: st.button("📅 Schedule Meeting", key="btn_rec_7")
        with b4: st.button("✉️ Generate Email", key="btn_rec_8")
        
        st.markdown("---")
        f_col1, f_col2 = st.columns([2, 2])
        f_col1.caption("Est. revenue at risk: **$48,000/yr**")
        f_col2.markdown("<div style='text-align: right; color: #10B981; font-size: 13px;'>Estimated churn reduction if acted: <b>-28%</b></div>", unsafe_allow_html=True)

# ==========================================
# PAGE: REPORTS
# ==========================================
elif selected == "Reports":
    col_title, col_actions = st.columns([3, 1])
    with col_title:
        st.markdown("## Reports")
        st.caption("Analytics reports and data exports")
    with col_actions:
        cols_btn = st.columns(2)
        with cols_btn[0]:
            st.button("📥 Download PDF", key="reports_pdf_btn")
        with cols_btn[1]:
            st.button("📊 Export Excel", key="reports_excel_btn", type="primary")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Weekly Report", "Monthly Report", "Department Report", "Churn Forecast"])

    with tab1:
        st.write("")
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

# ==========================================
# PAGE: SETTINGS
# ==========================================
elif selected == "Settings":
    st.markdown("## Settings")
    st.markdown("---")

    nav_col, form_col = st.columns([1, 3])

    with nav_col:
        st.markdown("👤 **Profile**")
        st.markdown("👥 Users & Roles")
        st.markdown("⚙️ AI Thresholds")
        st.markdown("🔔 Notifications")
        st.markdown("🔒 Security")
        st.markdown("🔑 API Keys")

    with form_col:
        with st.container(border=True):
            st.markdown("### Profile Information")
            
            col_avatar, col_info = st.columns([1, 6])
            with col_avatar:
                st.markdown("### 🔵 **AM**")
            with col_info:
                st.markdown("**Alex Morgan**")
                st.caption("Support Manager • alex@company.com")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            f1, f2 = st.columns(2)
            with f1:
                st.text_input("First Name", value="Alex", key="settings_first_name")
            with f2:
                st.text_input("Last Name", value="Morgan", key="settings_last_name")
                
            f3, f4 = st.columns(2)
            with f3:
                st.text_input("Email", value="alex@company.com", key="settings_email")
            with f4:
                st.text_input("Role", value="Support Manager", key="settings_role")
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Save Changes", key="settings_save_btn", type="primary"):
                st.success("Profile information updated successfully!")

# ==========================================
# PAGE: DATASET UPLOAD
# ==========================================

# ==========================================
# PAGE: DATASET UPLOAD
# REAL-TIME KPI DASHBOARD
# ==========================================

elif selected == "Dataset Upload":

    st.markdown("""
        <h1 style="
            color:#000000;
            font-size:40px;
            margin-bottom:0px;
            font-weight:700;
        ">
            Dataset Upload
        </h1>

        <p style="
            color:#6B7280;
            font-size:16px;
            margin-top:0px;
        ">
            Upload, filter and analyse your dataset in real time
        </p>
    """, unsafe_allow_html=True)

    st.divider()

    # ==========================================
    # FILE UPLOAD
    # ==========================================

    st.header("Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV or JSON file",
        type=["csv", "json"],
        help="Supported formats: CSV and JSON"
    )

    # ==========================================
    # NO FILE
    # ==========================================

    if uploaded_file is None:

        st.info(
            "Upload a CSV or JSON file to begin."
        )

        st.stop()

    # ==========================================
    # LOAD DATA USING CACHE
    # ==========================================

    try:

        file_bytes = uploaded_file.getvalue()

        df = load_uploaded_data(
            file_bytes,
            uploaded_file.name
        )

    except ValueError as e:

        st.error(str(e))
        st.stop()

    except pd.errors.EmptyDataError:

        st.warning(
            "Uploaded file is empty. "
            "Please upload a file containing data."
        )

        st.stop()

    except Exception as e:

        st.error(
            "Could not read this file. "
            "Please check that it is a valid CSV or JSON dataset."
        )

        st.stop()

    # ==========================================
    # EMPTY DATASET
    # ==========================================

    if df.empty:

        st.warning(
            "Uploaded file contains no records."
        )

        st.stop()

    # ==========================================
    # SUCCESS
    # ==========================================

    st.success(
        f"Loaded: {uploaded_file.name} "
        f"({len(df):,} rows, {len(df.columns):,} columns)"
    )

    # ==========================================
    # DATASET OVERVIEW
    # ==========================================

    st.divider()

    st.header("Dataset Overview")

    overview_1, overview_2, overview_3 = st.columns(3)

    with overview_1:

        st.metric(
            "Rows",
            f"{len(df):,}"
        )

    with overview_2:

        st.metric(
            "Columns",
            f"{len(df.columns):,}"
        )

    with overview_3:

        total_nulls = df.isnull().sum().sum()

        total_cells = (
            df.shape[0] *
            df.shape[1]
        )

        null_percentage = (
            (total_nulls / total_cells) * 100
            if total_cells > 0
            else 0
        )

        st.metric(
            "Null %",
            f"{null_percentage:.1f}%"
        )

    # ==========================================
    # COLUMN VALIDATION
    # ==========================================

    st.divider()

    st.header("Column Validation")

    available_columns = set(df.columns)

    # SupportPulse dataset columns that we can use
    # for the reactive KPI dashboard.
    preferred_columns = [
        "customer_id",
        "monthly_spend",
        "churn_status",
        "plan_type",
        "region",
        "signup_date"
    ]

    available_preferred = [
        column
        for column in preferred_columns
        if column in available_columns
    ]

    missing_preferred = [
        column
        for column in preferred_columns
        if column not in available_columns
    ]

    if available_preferred:

        st.success(
            "Available dashboard columns: "
            + ", ".join(available_preferred)
        )

    if missing_preferred:

        st.caption(
            "Optional columns not found: "
            + ", ".join(missing_preferred)
        )

    # ==========================================
    # FILTER SECTION
    # ==========================================

    st.divider()

    st.header("Filters")

    filtered_df = df.copy()

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    # ------------------------------------------
    # PLAN FILTER
    # ------------------------------------------

    with filter_col1:

        if "plan_type" in filtered_df.columns:

            plan_options = sorted(
                filtered_df["plan_type"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_plan = st.selectbox(
                "Plan Type",
                ["All"] + plan_options,
                key="kpi_plan_filter"
            )

            if selected_plan != "All":

                filtered_df = filtered_df[
                    filtered_df["plan_type"].astype(str)
                    == selected_plan
                ]

        else:

            st.info(
                "Plan Type filter unavailable."
            )

    # ------------------------------------------
    # REGION FILTER
    # ------------------------------------------

    with filter_col2:

        if "region" in filtered_df.columns:

            region_options = sorted(
                filtered_df["region"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_region = st.selectbox(
                "Region",
                ["All"] + region_options,
                key="kpi_region_filter"
            )

            if selected_region != "All":

                filtered_df = filtered_df[
                    filtered_df["region"].astype(str)
                    == selected_region
                ]

        else:

            st.info(
                "Region filter unavailable."
            )

    # ------------------------------------------
    # CHURN FILTER
    # ------------------------------------------

    with filter_col3:

        if "churn_status" in filtered_df.columns:

            churn_options = {
                "All": None,
                "Active": 0,
                "Churned": 1
            }

            selected_churn = st.selectbox(
                "Customer Status",
                list(churn_options.keys()),
                key="kpi_churn_filter"
            )

            churn_value = churn_options[selected_churn]

            if churn_value is not None:

                filtered_df = filtered_df[
                    filtered_df["churn_status"]
                    == churn_value
                ]

        else:

            st.info(
                "Churn filter unavailable."
            )

    # ==========================================
    # EMPTY FILTER RESULT
    # ==========================================

    if filtered_df.empty:

        st.warning(
            "No records match the selected filters."
        )

        st.info(
            "Try changing the Plan Type, Region, "
            "or Customer Status filters."
        )

        st.stop()

    # ==========================================
    # REACTIVE KPI DASHBOARD
    # ==========================================

    st.divider()

    st.header("Real-Time KPI Dashboard")

    # ------------------------------------------
    # KPI 1 — TOTAL RECORDS
    # ------------------------------------------

    total_records = len(filtered_df)

    # ------------------------------------------
    # KPI 2 — TOTAL REVENUE / SPEND
    # ------------------------------------------

    if "monthly_spend" in filtered_df.columns:

        total_revenue = pd.to_numeric(
            filtered_df["monthly_spend"],
            errors="coerce"
        ).fillna(0).sum()

    else:

        total_revenue = 0

    # ------------------------------------------
    # KPI 3 — AVERAGE SPEND
    # ------------------------------------------

    if "monthly_spend" in filtered_df.columns:

        average_spend = pd.to_numeric(
            filtered_df["monthly_spend"],
            errors="coerce"
        ).fillna(0).mean()

    else:

        average_spend = 0

    # ------------------------------------------
    # KPI 4 — CHURN RATE
    # ------------------------------------------

    if "churn_status" in filtered_df.columns:

        churn_rate = (
            pd.to_numeric(
                filtered_df["churn_status"],
                errors="coerce"
            )
            .fillna(0)
            .mean()
            * 100
        )

    else:

        churn_rate = 0

    # ------------------------------------------
    # KPI 5 — DATA QUALITY
    # ------------------------------------------

    total_missing = (
        filtered_df.isnull()
        .sum()
        .sum()
    )

    total_cells_filtered = (
        filtered_df.shape[0] *
        filtered_df.shape[1]
    )

    if total_cells_filtered > 0:

        data_quality = (
            1 -
            (
                total_missing /
                total_cells_filtered
            )
        ) * 100

    else:

        data_quality = 100

        # ==========================================
    # ALERT MONITORING
    # ==========================================

    current_metrics = {
        "churn_rate": churn_rate,
        "average_spend": average_spend,
        "null_percentage": 100 - data_quality
    }

    alerts = check_alerts(
        current_metrics,
        ALERT_THRESHOLDS
    )

    # ==========================================
    # DISPLAY ALERTS
    # ==========================================

    if alerts:

        st.divider()

        st.header("🚨 Active Alerts")

        for alert in alerts:

            alert_text = (
                f"{alert['metric']} is "
                f"{alert['value']:.1f} "
                f"(threshold: {alert['threshold']}). "
                f"{alert['message']}"
            )

            if alert["severity"] == "critical":

                st.error(
                    "ALERT: " + alert_text
                )

            else:

                st.warning(
                    "WARNING: " + alert_text
                )

    else:

        st.success(
            "✅ All monitored metrics are within safe thresholds."
        )

    # ==========================================
    # DISPLAY 5 KPIs
    # ==========================================

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric(
            "Total Records",
            f"{total_records:,}"
        )

    with k2:
        st.metric(
            "Total Spend",
            f"${total_revenue:,.0f}"
        )

    with k3:
        st.metric(
            "Average Spend",
            f"${average_spend:,.2f}"
        )

    with k4:
        st.metric(
            "Churn Rate",
            f"{churn_rate:.1f}%"
        )

    with k5:
        st.metric(
            "Data Quality",
            f"{data_quality:.1f}%"
        )
    # ==========================================
    # DISPLAY 5 KPIs
    # ==========================================

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        st.metric(
            "Total Records",
            f"{total_records:,}"
        )

    with k2:

        st.metric(
            "Total Spend",
            f"${total_revenue:,.0f}"
        )

    with k3:

        st.metric(
            "Average Spend",
            f"${average_spend:,.2f}"
        )

    with k4:

        st.metric(
            "Churn Rate",
            f"{churn_rate:.1f}%"
        )

    with k5:

        st.metric(
            "Data Quality",
            f"{data_quality:.1f}%"
        )

    # ==========================================
    # CHART SECTION
    # ==========================================

    st.divider()

    st.header("Interactive Charts")

    chart_left, chart_right = st.columns(2)

    # ==========================================
    # CHART 1 — LINE CHART
    # ==========================================

    with chart_left:

        st.subheader("Customer Trend")

        if "signup_date" in filtered_df.columns:

            trend_df = filtered_df.copy()

            trend_df["signup_date"] = pd.to_datetime(
                trend_df["signup_date"],
                errors="coerce"
            )

            trend_df = trend_df.dropna(
                subset=["signup_date"]
            )

            if not trend_df.empty:

                trend_df["Month"] = (
                    trend_df["signup_date"]
                    .dt.to_period("M")
                    .astype(str)
                )

                monthly_trend = (
                    trend_df
                    .groupby("Month")
                    .size()
                    .reset_index(
                        name="Customers"
                    )
                )

                fig_line = px.line(
                    monthly_trend,
                    x="Month",
                    y="Customers",
                    markers=True,
                    title="Customers Over Time"
                )

                fig_line.update_layout(
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    height=400
                )

                st.plotly_chart(
                    fig_line,
                    use_container_width=True
                )

            else:

                st.info(
                    "No valid date values available."
                )

        else:

            st.info(
                "Signup date column is unavailable."
            )

    # ==========================================
    # CHART 2 — BAR CHART
    # ==========================================

    with chart_right:

        st.subheader("Spend by Plan")

        if (
            "plan_type" in filtered_df.columns
            and "monthly_spend" in filtered_df.columns
        ):

            plan_chart_df = filtered_df.copy()

            plan_chart_df["monthly_spend"] = (
                pd.to_numeric(
                    plan_chart_df["monthly_spend"],
                    errors="coerce"
                )
                .fillna(0)
            )

            plan_summary = (
                plan_chart_df
                .groupby("plan_type")[
                    "monthly_spend"
                ]
                .sum()
                .reset_index()
            )

            if not plan_summary.empty:

                fig_bar = px.bar(
                    plan_summary,
                    x="plan_type",
                    y="monthly_spend",
                    title="Monthly Spend by Plan",
                    labels={
                        "plan_type": "Plan",
                        "monthly_spend": "Spend"
                    }
                )

                fig_bar.update_layout(
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    height=400
                )

                st.plotly_chart(
                    fig_bar,
                    use_container_width=True
                )

            else:

                st.info(
                    "No plan data available."
                )

        else:

            st.info(
                "Plan Type or Monthly Spend column "
                "is unavailable."
            )

    # ==========================================
    # CHART 3 — HISTOGRAM
    # ==========================================

    st.subheader("Spend Distribution")

    if "monthly_spend" in filtered_df.columns:

        histogram_df = filtered_df.copy()

        histogram_df["monthly_spend"] = (
            pd.to_numeric(
                histogram_df["monthly_spend"],
                errors="coerce"
            )
        )

        histogram_df = histogram_df.dropna(
            subset=["monthly_spend"]
        )

        if not histogram_df.empty:

            fig_hist = px.histogram(
                histogram_df,
                x="monthly_spend",
                nbins=20,
                title="Monthly Spend Distribution",
                labels={
                    "monthly_spend": "Monthly Spend"
                }
            )

            fig_hist.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                height=400
            )

            st.plotly_chart(
                fig_hist,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric spend values available."
            )

    else:

        st.info(
            "Monthly Spend column is unavailable."
        )

    # ==========================================
    # FILTERED DATA PREVIEW
    # ==========================================

    st.divider()

    st.header("Filtered Dataset")

    st.caption(
        f"Showing {len(filtered_df):,} records "
        f"after applying the selected filters."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # ==========================================
    # DATASET DETAILS
    # ==========================================

    with st.expander("ℹ️ Dataset Details"):

        st.write(
            f"**File:** {uploaded_file.name}"
        )

        st.write(
            f"**Original Rows:** {len(df):,}"
        )

        st.write(
            f"**Filtered Rows:** {len(filtered_df):,}"
        )

        st.write(
            f"**Columns:** {len(df.columns):,}"
        )

        st.write(
            f"**Numeric Columns:** "
            f"{len(df.select_dtypes(include='number').columns)}"
        )
# ==========================================
# PAGE: SESSION STATE & WORKFLOW
# ==========================================

elif selected == "Session State":

    # ------------------------------------------------
    # SESSION STATE INITIALIZATION
    # ------------------------------------------------

    # "selected_segment" stores the user's selected
    # customer segment so it survives Streamlit reruns.
    if "selected_segment" not in st.session_state:
        st.session_state["selected_segment"] = "All"

    # "workflow_step" tracks the current workflow step.
    # Step 1 = segment selection, Step 2 = analysis.
    if "workflow_step" not in st.session_state:
        st.session_state["workflow_step"] = 1

    # "analysis_result" stores the calculated result
    # from Step 2 so it remains available after reruns.
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None

    # ------------------------------------------------
    # RESET WORKFLOW
    # ------------------------------------------------

    with st.sidebar:
        st.markdown("---")

        if st.button(
            "🔄 Reset Workflow",
            key="session_reset_workflow",
            use_container_width=True
        ):

            # Remove only the workflow-related session state.
            # Other application state remains untouched.
            for key in [
                "selected_segment",
                "workflow_step",
                "analysis_result"
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

    # ------------------------------------------------
    # PAGE HEADER
    # ------------------------------------------------

    st.markdown("""
        <h1 style="
            color:#000000;
            font-size:40px;
            margin-bottom:0px;
            font-weight:700;
        ">
            Session State Workflow
        </h1>

        <p style="
            color:#6B7280;
            font-size:16px;
            margin-top:0px;
        ">
            Persistent multi-step customer churn analysis
        </p>
    """, unsafe_allow_html=True)

    st.divider()

    # ------------------------------------------------
    # CURRENT WORKFLOW STATUS
    # ------------------------------------------------

    current_step = st.session_state["workflow_step"]

    st.markdown("### Workflow Status")

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        st.metric(
            "Current Step",
            f"Step {current_step}"
        )

    with status_col2:
        st.metric(
            "Selected Segment",
            st.session_state["selected_segment"]
        )

    with status_col3:
        result = st.session_state["analysis_result"]

        if result is None:
            result_display = "Not calculated"
        else:
            result_display = f"{result:,.0f}"

        st.metric(
            "Analysis Result",
            result_display
        )

    st.divider()

    # ==================================================
    # STEP 1
    # ==================================================

    st.header("Step 1: Select Customer Segment")

    segments = [
        "All",
        "Enterprise",
        "Mid-Market",
        "SMB"
    ]

    # Read the saved value from session state.
    # This keeps the widget synchronized after reruns.
    current_segment = st.session_state["selected_segment"]

    if current_segment not in segments:
        current_segment = "All"

    segment = st.selectbox(
        "Choose a segment",
        segments,
        index=segments.index(current_segment),
        key="workflow_segment_selector"
    )

    st.caption(
        "Your selection will remain available even when "
        "the application reruns."
    )

    if st.button(
        "Confirm Segment →",
        type="primary",
        key="confirm_segment_btn"
    ):

        # Save Step 1 selection into session state.
        st.session_state["selected_segment"] = segment

        # Move the workflow to Step 2.
        st.session_state["workflow_step"] = 2

        # Clear any previous result because the segment changed.
        st.session_state["analysis_result"] = None

        st.rerun()

    # ==================================================
    # STEP 2
    # ==================================================

    if st.session_state["workflow_step"] >= 2:

        st.divider()

        st.header("Step 2: Segment Analysis")

        # Retrieve the segment saved in Step 1.
        chosen_segment = st.session_state["selected_segment"]

        st.success(
            f"Analyzing customer segment: **{chosen_segment}**"
        )

        # ------------------------------------------------
        # FIND SEGMENT COLUMN
        # ------------------------------------------------

        # Your SupportPulse customer dataset uses plan_type,
        # so map the workflow segments to the available plans.

        segment_mapping = {
            "All": None,
            "Enterprise": "Enterprise",
            "Mid-Market": "Mid-Market",
            "SMB": "SMB"
        }

        target_plan = segment_mapping[chosen_segment]

        analysis_df = customers.copy()

        if target_plan is not None:

            if "plan_type" in analysis_df.columns:

                analysis_df = analysis_df[
                    analysis_df["plan_type"] == target_plan
                ]

        # ------------------------------------------------
        # ANALYSIS
        # ------------------------------------------------

        total_customers_segment = len(analysis_df)

        if total_customers_segment > 0:

            if "churn_status" in analysis_df.columns:

                churned_customers = int(
                    analysis_df["churn_status"].sum()
                )

                churn_rate = (
                    churned_customers /
                    total_customers_segment
                ) * 100

            else:

                churned_customers = 0
                churn_rate = 0

            if "monthly_spend" in analysis_df.columns:

                total_revenue = float(
                    analysis_df["monthly_spend"].sum()
                )

            else:

                total_revenue = 0

            # Store the main analysis result in session state.
            st.session_state["analysis_result"] = total_revenue

            # ------------------------------------------------
            # RESULT METRICS
            # ------------------------------------------------

            st.markdown("### Segment Results")

            r1, r2, r3, r4 = st.columns(4)

            with r1:
                st.metric(
                    "Customers",
                    total_customers_segment
                )

            with r2:
                st.metric(
                    "Churned",
                    churned_customers
                )

            with r3:
                st.metric(
                    "Churn Rate",
                    f"{churn_rate:.1f}%"
                )

            with r4:
                st.metric(
                    "Monthly Spend",
                    f"${total_revenue:,.0f}"
                )

            # ------------------------------------------------
            # SEGMENT DATA
            # ------------------------------------------------

            st.markdown("### Customers in Selected Segment")

            display_columns = [
                column
                for column in [
                    "customer_id",
                    "name",
                    "plan_type",
                    "region",
                    "monthly_spend",
                    "churn_status"
                ]
                if column in analysis_df.columns
            ]

            if display_columns:

                display_df = analysis_df[
                    display_columns
                ].copy()

                if "churn_status" in display_df.columns:

                    display_df["churn_status"] = (
                        display_df["churn_status"]
                        .map({
                            0: "Active",
                            1: "Churned"
                        })
                    )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.warning(
                f"No customers found for the "
                f"{chosen_segment} segment."
            )

    # ==================================================
    # SESSION STATE DEBUG / DEMONSTRATION
    # ==================================================

    st.divider()

    with st.expander("🔍 View Session State"):

        st.write(
            "These values persist across Streamlit reruns:"
        )

        st.json({
            "selected_segment":
                st.session_state["selected_segment"],

            "workflow_step":
                st.session_state["workflow_step"],

            "analysis_result":
                st.session_state["analysis_result"]
        })
# ==========================================
# OTHER PAGES PLACEHOLDER
# ==========================================

else:

    st.markdown(f"""
        <h1 style="color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;">
            {selected}
        </h1>

        <p style="color:#6B7280; font-size:16px; margin-top:0px;">
            Manage module settings and controls for {selected.lower()}
        </p>
    """, unsafe_allow_html=True)

    st.write("")

    st.info(
        f"The **{selected}** module view is active. "
        f"Connect your specific backend data models or filters "
        f"for this section here."
    )