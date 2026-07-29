import streamlit as st

st.set_page_config(page_title="ChurnGuard - Customers", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E5E7EB; }
    .custom-table { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛡️ **ChurnGuard**")
    st.caption("AI Retention Platform")
    st.markdown("---")
    st.markdown("<br>" * 14, unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns([1, 4])
    with c1: st.markdown("🟢")
    with c2: st.markdown("**Alex Morgan**<br><span style='font-size: 12px; color: gray;'>Support Manager</span>", unsafe_allow_html=True)

st.markdown("### Customers")
st.caption("Manage and monitor your customer accounts")

col_btn1, col_btn2 = st.columns([7, 1])
with col_btn2:
    if st.button("📤 Export CSV", use_container_width=True): st.toast("Exporting customer table...")

st.markdown("---")

f1, f2, f3, f4 = st.columns([4, 1, 1, 1])
with f1: st.text_input("Search", placeholder="🔍 Search by name or contact...", label_visibility="collapsed")
with f2: st.selectbox("Filter", ["All Industries"], label_visibility="collapsed")
with f3: st.selectbox("Risk", ["All Risk Levels"], label_visibility="collapsed")
with f4: st.markdown("<div style='padding-top: 6px; font-size: 14px; color: #6B7280;'>8 of 8 customers</div>", unsafe_allow_html=True)

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
            <tr style="border-bottom: 1px solid #E5E7EB; color: #6B7280; background-color: #FAFAFA;">
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
    status_color = "#EF4444" if c["status"] == "Critical" else ("#F97316" if "Risk" in c["status"] else "#10B981")
    risk_color = "#EF4444" if "Critical" in c["risk"] else ("#F59E0B" if "Medium" in c["risk"] else "#10B981")
    
    st.markdown(f"""
            <tr style="border-bottom: 1px solid #F3F4F6;">
                <td style="padding: 12px 16px;"><b>{c['name']}</b><br><span style="font-size: 11px; color: #6B7280;">{c['contact']}</span></td>
                <td style="padding: 12px 16px; color: #4B5563;">{c['industry']}<br><span style="font-size: 11px; color: #9CA3AF;">{c['region']}</span></td>
                <td style="padding: 12px 16px; color: #EF4444; font-weight: bold;">{c['tickets']}</td>
                <td style="padding: 12px 16px; color: #4B5563;">{c['resolution']}</td>
                <td style="padding: 12px 16px; color: #EF4444; font-weight: bold;">{c['escalations']}</td>
                <td style="padding: 12px 16px;"><span style="background: #FEF2F2; color: {risk_color}; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{c['risk']}</span></td>
                <td style="padding: 12px 16px; color: #374151;">{c['health']}</td>
                <td style="padding: 12px 16px;"><span style="background: #FEE2E2; color: {status_color}; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{c['status']}</span></td>
                <td style="padding: 12px 16px; color: #9CA3AF;">›</td>
            </tr>
    """, unsafe_allow_html=True)

st.markdown("</table></div>", unsafe_allow_html=True)