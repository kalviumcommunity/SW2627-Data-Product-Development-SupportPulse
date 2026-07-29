import streamlit as st

st.set_page_config(page_title="ChurnGuard - Support Tickets", page_icon="🛡️", layout="wide")

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

st.markdown("### Support Tickets")
st.caption("8 active tickets — 4 escalated")

col_b1, col_b2 = st.columns([7, 1])
with col_b2:
    if st.button("📤 Export", use_container_width=True): st.toast("Exporting tickets...")

st.markdown("---")

st.text_input("Search tickets", placeholder="🔍 Search by ticket ID, customer, or issue...", label_visibility="collapsed")
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
            <tr style="border-bottom: 1px solid #E5E7EB; color: #6B7280; background-color: #FAFAFA;">
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
                <td style="padding: 12px 16px;"><span style="background: #EFF6FF; color: {status_color}; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{t['status']}</span></td>
                <td style="padding: 12px 16px; color: #4B5563;">{t['agent']}</td>
                <td style="padding: 12px 16px; color: #EF4444;">{t['resolution']}</td>
                <td style="padding: 12px 16px; color: {escalated_color}; font-weight: bold;">{t['escalated']}</td>
                <td style="padding: 12px 16px; color: #EF4444;">{t['sentiment']}</td>
            </tr>
    """, unsafe_allow_html=True)

st.markdown("</table></div>", unsafe_allow_html=True)