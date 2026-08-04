import streamlit as st

st.set_page_config(page_title="Settings - ChurnGuard", page_icon="⚙️", layout="wide")

# Top header row
st.markdown("## Settings")
st.markdown("---")

# Layout columns for sub-navigation menu & form container
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
        
        # Profile header representation
        col_avatar, col_info = st.columns([1, 6])
        with col_avatar:
            st.markdown("### 🔵 **AM**")
        with col_info:
            st.markdown("**Alex Morgan**")
            st.caption("Support Manager • alex@company.com")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Input Form Grid
        f1, f2 = st.columns(2)
        with f1:
            st.text_input("First Name", value="Alex")
        with f2:
            st.text_input("Last Name", value="Morgan")
            
        f3, f4 = st.columns(2)
        with f3:
            st.text_input("Email", value="alex@company.com")
        with f4:
            st.text_input("Role", value="Support Manager")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Changes", type="primary"):
            st.success("Profile information updated successfully!")