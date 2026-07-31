import streamlit as st
import pandas as pd

st.set_page_config(page_title="Escalations - ChurnGuard", page_icon="🚨", layout="wide")

# Top header / search row
col_title, col_search, col_actions = st.columns([2, 2, 1])
with col_title:
    st.markdown("## Escalations")
    st.caption("4 active escalations requiring attention")
with col_search:
    st.text_input("", placeholder="🔍 Search customers, tickets...", label_visibility="collapsed")
with col_actions:
    cols_btn = st.columns(2)
    with cols_btn[0]:
        st.markdown("🔔")
    with cols_btn[1]:
        st.button("📥 Export", use_container_width=True)

st.markdown("---")

# Metrics Cards row
m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="Critical Escalations", value="2", delta="Action Required", delta_color="inverse")
with m2:
    st.metric(label="Overdue Tickets", value="3")
with m3:
    st.metric(label="Unassigned", value="0")

st.markdown("<br>", unsafe_allow_html=True)

# Data Table representation matching the UI
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

df = pd.DataFrame(data)

# Render a styled representation of the table
for index, row in df.iterrows():
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([1.2, 2, 2.2, 1, 1, 1.2, 1.5, 1.2, 1])
    c1.write(f"**{row['Ticket ID']}**")
    c2.write(row['Customer'])
    c3.write(row['Issue'])
    
    # Color indicators for Priority
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