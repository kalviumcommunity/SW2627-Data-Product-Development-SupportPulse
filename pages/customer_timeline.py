import streamlit as st

st.set_page_config(page_title="Customer Timeline - ChurnGuard", page_icon="⏱️", layout="wide")

# Custom CSS to reset global text visibility on dark elements and enforce clean black text on containers
st.markdown("""
<style>
    .stApp {
        background-color: #f7f8fc;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# Top header / search row
col_title, col_search = st.columns([3, 1])
with col_title:
    st.markdown("## Customer Timeline")
    st.caption("Complete interaction history and event log")
with col_search:
    selected_customer = st.selectbox("Select Customer", ["Acme Corporation", "DataStream Analytics", "LegalEagle Firm"], label_visibility="collapsed")

st.markdown("---")

# Layout columns for profile card & event types vs interactive timeline
left_col, right_col = st.columns([1, 2.2])

with left_col:
    # Customer Profile summary card container
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

    # Event Types breakdown box
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