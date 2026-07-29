import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="ChurnGuard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS Styles ----------------
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
            "Settings"
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
            "gear"
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
    st.text_input("", placeholder="🔍 Search customers, tickets...", label_visibility="collapsed")

with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

with col3:
    if st.button("⬇ Export"):
        st.toast("Exporting data...")

# ==========================================
# PAGE: DASHBOARD
# ==========================================
if selected == "Dashboard":
    st.markdown("""
    <h1 style="color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;">Dashboard</h1>
    <p style="color:#6B7280; font-size:16px; margin-top:0px;">Overview of churn risk and support health — Dec 2023</p>
    """, unsafe_allow_html=True)

    cards = st.columns(5)
    values = [
        ("👥", "1,247", "Total Customers", "+12 this month", "red"),
        ("📂", "84", "Open Tickets", "+8 vs last week", "red"),
        ("⚠", "5.5%", "Predicted Churn", "+0.3%", "red"),
        ("✅", "23", "Resolved Today", "-5 vs yesterday", "green"),
        ("🕒", "2.4d", "Avg Resolution", "+0.3d", "red")
    ]

    for col, (icon, val, title, change, color) in zip(cards, values):
        with col:
            cls = "metric-change-red" if color == "red" else "metric-change-green"
            st.markdown(f"""
            <div class="metric-card">
            <span>{icon}</span>
            <span class="{cls}">{change}</span>
            <div class="metric-value">{val}</div>
            <div class="metric-title">{title}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([2.2, 1])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    actual = [2, 2.1, 2.0, 2.8, 3, 2.4, 3.2, 3.7, 3.6, 4.2, 4.8, 5.4]
    df = pd.DataFrame({"Month": months, "Actual": actual})

    with left:
        st.markdown("### Monthly Churn Trend")
        fig = px.line(df, x="Month", y="Actual", markers=False)
        fig.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title=""
        )
        fig.update_traces(line=dict(width=4, color="#2563EB"))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### Complaint Categories")
        pie = pd.DataFrame({
            "Category": ["Billing", "Performance", "Integration", "Feature Request", "Onboarding", "Other"],
            "Value": [28, 22, 19, 16, 10, 5]
        })
        fig2 = px.pie(pie, names="Category", values="Value", hole=.72)
        fig2.update_layout(
            height=420, paper_bgcolor="white",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=True
        )
        st.plotly_chart(fig2, use_container_width=True)

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
        st.text_input("Search filter", placeholder="🔍 Search by name or contact...", label_visibility="collapsed")
    with f2:
        st.selectbox("Industry", ["All Industries"], label_visibility="collapsed")
    with f3:
        st.selectbox("Risk", ["All Risk Levels"], label_visibility="collapsed")
    with f4:
        st.markdown("<div style='padding-top: 8px; font-size: 14px; color: #6B7280;'>8 of 8 customers</div>", unsafe_allow_html=True)

    st.write("")

    customers_data = [
        {"name": "Acme Corporation", "contact": "James Mitchell", "industry": "Manufacturing", "region": "North America", "tickets": 8, "resolution": "4.2d", "escalations": 3, "risk": "87% • Critical", "health": 23, "status": "Critical"},
        {"name": "TechFlow Solutions", "contact": "Sarah Chen", "industry": "Technology", "region": "Asia Pacific", "tickets": 5, "resolution": "2.8d", "escalations": 2, "risk": "72% • Critical", "health": 38, "status": "High Risk"},
        {"name": "GlobalRetail Inc", "contact": "Michael Torres", "industry": "Retail", "region": "Europe", "tickets": 3, "resolution": "1.9d", "escalations": 1, "risk": "58% • Medium", "health": 55, "status": "Medium Risk"},
        {"name": "HealthBridge Partners", "contact": "Emily Watson", "industry": "Healthcare", "region": "North America", "tickets": 1, "resolution": "0.8d", "escalations": 0, "risk": "18% • Low", "health": 89, "status": "Healthy"},
        {"name": "DataStream Analytics", "contact": "Robert Kim", "industry": "Analytics", "region": "North America", "tickets": 6, "resolution": "3.5d", "escalations": 4, "risk": "91% • Critical", "health": 12, "status": "Critical"},
        {"name": "LegalEagle Firm", "contact": "Amanda Foster", "industry": "Legal", "region": "Europe", "tickets": 2, "resolution": "2.1d", "escalations": 1, "risk": "44% • Medium", "health": 67, "status": "Low Risk"},
        {"name": "EduLearn Platform", "contact": "David Park", "industry": "Education", "region": "Asia Pacific", "tickets": 4, "resolution": "2.9d", "escalations": 2, "risk": "65% • Medium", "health": 44, "status": "Medium Risk"},
        {"name": "FinanceFirst Corp", "contact": "Linda Garcia", "industry": "Finance", "region": "North America", "tickets": 0, "resolution": "1.2d", "escalations": 0, "risk": "12% • Low", "health": 94, "status": "Healthy"}
    ]

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

    for c in customers_data:
        status_color = "#EF4444" if c["status"] == "Critical" else ("#F97316" if "Risk" in c["status"] else "#22C55E")
        risk_color = "#EF4444" if "Critical" in c["risk"] else ("#F59E0B" if "Medium" in c["risk"] else "#22C55E")
        
        st.markdown(f"""
                <tr style="border-bottom: 1px solid #F3F4F6;">
                    <td style="padding: 12px 16px;">
                        <b>{c['name']}</b><br><span style="font-size: 11px; color: #6B7280;">{c['contact']}</span>
                    </td>
                    <td style="padding: 12px 16px; color: #4B5563;">
                        {c['industry']}<br><span style="font-size: 11px; color: #9CA3AF;">{c['region']}</span>
                    </td>
                    <td style="padding: 12px 16px; color: #EF4444; font-weight: bold;">{c['tickets']}</td>
                    <td style="padding: 12px 16px; color: #4B5563;">{c['resolution']}</td>
                    <td style="padding: 12px 16px; color: #EF4444; font-weight: bold;">{c['escalations']}</td>
                    <td style="padding: 12px 16px;"><span style="background: #FEF2F2; color: {risk_color}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{c['risk']}</span></td>
                    <td style="padding: 12px 16px; color: #374151;">{c['health']}</td>
                    <td style="padding: 12px 16px;"><span style="background: #FEE2E2; color: {status_color}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{c['status']}</span></td>
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
        st.text_input("Ticket search", placeholder="🔍 Search by ticket ID, customer, or issue...", label_visibility="collapsed")
    with s2:
        st.selectbox("Status", ["All Status"], label_visibility="collapsed")

    st.write("")

    tickets_data = [
        {"id": "TKT-2847", "customer": "Acme Corporation", "category": "Billing Dispute", "priority": "High", "status": "Open", "agent": "Sarah M.", "resolution": "Overdue (8d)", "escalated": "Yes", "sentiment": "Negative"},
        {"id": "TKT-2843", "customer": "DataStream Analytics", "category": "API Integration Failure", "priority": "Critical", "status": "Escalated", "agent": "Tom R.", "resolution": "Overdue (12d)", "escalated": "Yes", "sentiment": "Very Negative"},
        {"id": "TKT-2839", "customer": "TechFlow Solutions", "category": "Performance Degradation", "priority": "High", "status": "In Progress", "agent": "Emma L.", "resolution": "3d", "escalated": "No", "sentiment": "Neutral"},
        {"id": "TKT-2834", "customer": "GlobalRetail Inc", "category": "Pricing Inquiry", "priority": "Medium", "status": "Open", "agent": "Unassigned", "resolution": "12d", "escalated": "No", "sentiment": "Neutral"},
        {"id": "TKT-2829", "customer": "EduLearn Platform", "category": "LMS Integration", "priority": "High", "status": "In Progress", "agent": "Chris K.", "resolution": "5d", "escalated": "No", "sentiment": "Neutral"},
        {"id": "TKT-2821", "customer": "LegalEagle Firm", "category": "Compliance Feature", "priority": "Medium", "status": "Pending", "agent": "Sarah M.", "resolution": "4d", "escalated": "Yes", "sentiment": "Neutral"},
        {"id": "TKT-2815", "customer": "DataStream Analytics", "category": "Onboarding Blockers", "priority": "Critical", "status": "Open", "agent": "Tom R.", "resolution": "Overdue (21d)", "escalated": "Yes", "sentiment": "Very Negative"},
        {"id": "TKT-2801", "customer": "Acme Corporation", "category": "Data Export Error", "priority": "High", "status": "In Progress", "agent": "Emma L.", "resolution": "2d", "escalated": "No", "sentiment": "Negative"}
    ]

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

    for t in tickets_data:
        priority_color = "#EF4444" if t["priority"] in ["Critical", "High"] else "#F59E0B"
        status_color = "#EF4444" if t["status"] == "Escalated" else "#3B82F6"
        escalated_color = "#EF4444" if t["escalated"] == "Yes" else "#6B7280"
        



        st.markdown(f"""
                <tr style="border-bottom: 1px solid #F3F4F6;">
                    <td style="padding: 12px 16px; color: #2563EB; font-weight: bold;">{t['id']}</td>
                    <td style="padding: 12px 16px; font-weight: 500;">{t['customer']}</td>
                    <td style="padding: 12px 16px; color: #4B5563;">{t['category']}</td>
                    <td style="padding: 12px 16px; color: {priority_color}; font-weight: bold;">{t['priority']}</td>
                    <td style="padding: 12px 16px;"><span style="background: #EFF6FF; color: {status_color}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{t['status']}</span></td>
                    <td style="padding: 12px 16px; color: #4B5563;">{t['agent']}</td>
                    <td style="padding: 12px 16px; color: #EF4444;">{t['resolution']}</td>
                    <td style="padding: 12px 16px; color: {escalated_color}; font-weight: bold;">{t['escalated']}</td>
                    <td style="padding: 12px 16px; color: #EF4444;">{t['sentiment']}</td>
                </tr>
        """, unsafe_allow_html=True)

    st.markdown("</table></div>", unsafe_allow_html=True)



# ==========================================
# OTHER PAGES PLACEHOLDER
# ==========================================
else:
    st.markdown(f"""
    <h1 style="color:#000000; font-size:40px; margin-bottom:0px; font-weight:700;">{selected}</h1>
    <p style="color:#6B7280; font-size:16px; margin-top:0px;">Manage module settings and controls for {selected.lower()}</p>
    """, unsafe_allow_html=True)
    st.write("")
    st.info(f"The **{selected}** module view is active. Connect your specific backend data models or filters for this section here.")