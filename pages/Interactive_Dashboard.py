import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Interactive Dashboard",
    layout="wide"
)

st.title("📊 SupportPulse Interactive Dashboard")

# ---------------------------------------
# Load Data
# ---------------------------------------

customers = pd.read_csv(
    "data/raw/customers.csv"
)

transactions = pd.read_csv(
    "data/raw/transactions.csv"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

df = transactions.merge(
    customers,
    on="customer_id",
    how="left"
)

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------

st.sidebar.header("Filters")

regions = ["All"] + sorted(df["region"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

min_amount = st.sidebar.slider(
    "Minimum Transaction Amount",
    int(df["amount"].min()),
    int(df["amount"].max()),
    int(df["amount"].min())
)

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["region"] == selected_region
    ]

filtered_df = filtered_df[
    filtered_df["amount"] >= min_amount
]

st.write(f"Showing **{len(filtered_df)}** transactions")

# ---------------------------------------
# Daily Revenue
# ---------------------------------------

daily = (
    filtered_df
    .groupby("transaction_date")
    .agg(
        revenue=("amount", "sum"),
        orders=("amount", "count")
    )
    .reset_index()
)

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=daily["transaction_date"],

        y=daily["revenue"],

        mode="lines+markers",

        line=dict(color="#1f77b4", width=3),

        marker=dict(size=8),

        customdata=daily["orders"],

        hovertemplate=
        "<b>%{x|%d-%b-%Y}</b><br>"
        "Revenue: $%{y:.2f}<br>"
        "Orders: %{customdata}<extra></extra>"

    )

)

fig.update_layout(

    title="Daily Revenue Trend",

    xaxis_title="Date",

    yaxis_title="Revenue ($)",

    hovermode="x unified",

    dragmode="zoom",

    height=550

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Filtered Transactions")

st.dataframe(

    filtered_df[
        [
            "transaction_date",
            "customer_id",
            "region",
            "amount"
        ]
    ],

    use_container_width=True

)