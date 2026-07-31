import streamlit as st

st.markdown("# AI Churn Prediction")
st.caption("Powered by gradient boosting ensemble — last trained Dec 12, 2023")

col_title, col_btns = st.columns([3, 1])
with col_btns:
    b1, b2 = st.columns(2)
    with b1:
        st.button("🔄 Retrain Model", use_container_width=True)
    with b2:
        st.button("⚡ Run Batch Prediction", type="primary", use_container_width=True)

st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Model Accuracy", "94.2%")
with m2:
    st.metric("Customers Analyzed", "1,247")
with m3:
    st.metric("High Risk (>70%)", "38", delta="-2", delta_color="inverse")
with m4:
    st.metric("Revenue at Risk", "$284K")

st.markdown("<br>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown("##### Select Customer")
    customers = [
        {"name": "DataStream Analytics", "industry": "Analytics", "risk": 91, "bg": "#eff6ff"},
        {"name": "Acme Corporation", "industry": "Manufacturing", "risk": 87, "bg": "#ffffff"},
        {"name": "TechFlow Solutions", "industry": "Technology", "risk": 72, "bg": "#ffffff"},
        {"name": "EduLearn Platform", "industry": "Education", "risk": 65, "bg": "#ffffff"},
        {"name": "GlobalRetail Inc", "industry": "Retail", "risk": 58, "bg": "#ffffff"},
        {"name": "LegalEagle Firm", "industry": "Legal", "risk": 44, "bg": "#ffffff"},
        {"name": "HealthBridge Partners", "industry": "Healthcare", "risk": 18, "bg": "#ffffff"},
        {"name": "FinanceFirst Corp", "industry": "Finance", "risk": 12, "bg": "#ffffff"},
    ]
    
    for c in customers:
        color = "#ef4444" if c["risk"] > 70 else "#f97316" if c["risk"] > 50 else "#22c55e"
        st.markdown(f"""
            <div style="background-color: {c['bg']}; padding: 10px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{c['name']}</strong><br><span style="font-size: 12px; color: #64748b;">{c['industry']}</span>
                </div>
                <div style="font-weight: bold; color: {color};">{c['risk']}%</div>
            </div>
        """, unsafe_allow_html=True)

with right_col:
    st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; display: inline-block;">DataStream Analytics</h4> 
                    <span style="background-color: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; margin-left: 8px;">Critical</span>
                    <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Startup • Analytics • MRR: $2,000</p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 12px; color: #64748b;">Prediction confidence</span><br>
                    <span style="font-size: 20px; font-weight: bold; color: #0f172a;">94.2%</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### REASONS BEHIND PREDICTION")
    r1, r2 = st.columns(2)
    with r1:
        st.info("🕒 Late ticket resolution")
        st.info("🔄 Repeated complaints")
        st.info("⚡ Usage drop >30%")
    with r2:
        st.warning("💬 Negative sentiment trend")
        st.warning("📉 Multiple escalations")
        st.warning("📅 Short account age")