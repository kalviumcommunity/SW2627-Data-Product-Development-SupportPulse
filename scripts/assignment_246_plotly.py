import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------
# Create Output Folder
# ---------------------------------------

os.makedirs(
    "interactive_charts",
    exist_ok=True
)

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

print("=" * 60)
print("SUPPORTPULSE INTERACTIVE PLOTLY CHARTS")
print("=" * 60)

# ==========================================================
# CHART 1
# Revenue Trend
# ==========================================================

daily = (
    df.groupby("transaction_date")
      .agg(
          revenue=("amount", "sum"),
          order_count=("amount", "count")
      )
      .reset_index()
)

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=daily["transaction_date"],
        y=daily["revenue"],
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3),
        marker=dict(size=8),
        hovertemplate=
        "<b>%{x|%d-%b-%Y}</b><br>"
        "Revenue : $%{y:.2f}<br>"
        "Orders : %{customdata}<extra></extra>",
        customdata=daily["order_count"]
    )
)

fig1.update_layout(
    title="Daily Revenue Trend",
    xaxis_title="Date",
    yaxis_title="Revenue ($)",
    hovermode="x unified"
)

fig1.write_html(
    "interactive_charts/chart1_revenue_trend.html"
)

print("Chart 1 Created")

# ==========================================================
# CHART 2
# Revenue By Region
# ==========================================================

region = (
    df.groupby("region")
      .agg(
          revenue=("amount", "sum"),
          orders=("amount", "count")
      )
      .reset_index()
)

fig2 = px.bar(
    region,
    x="region",
    y="revenue",
    color="region"
)

fig2.update_traces(

    hovertemplate=
    "<b>%{x}</b><br>"
    "Revenue : $%{y:.2f}<br>"
    "Orders : %{customdata}<extra></extra>",

    customdata=region["orders"]
)

fig2.update_layout(
    title="Revenue By Region",
    xaxis_title="Region",
    yaxis_title="Revenue ($)"
)

fig2.write_html(
    "interactive_charts/chart2_region_revenue.html"
)

print("Chart 2 Created")

# ==========================================================
# CHART 3
# Dropdown
# ==========================================================

summary = (
    df.groupby("region")
      .agg(
          revenue=("amount","sum"),
          orders=("amount","count"),
          average=("amount","mean")
      )
      .reset_index()
)

fig3 = go.Figure()

fig3.add_trace(
    go.Bar(
        x=summary["region"],
        y=summary["revenue"],
        name="Revenue",
        visible=True
    )
)

fig3.add_trace(
    go.Bar(
        x=summary["region"],
        y=summary["orders"],
        name="Orders",
        visible=False
    )
)

fig3.add_trace(
    go.Bar(
        x=summary["region"],
        y=summary["average"],
        name="Average",
        visible=False
    )
)

fig3.update_layout(

    title="Region Performance",

    updatemenus=[

        dict(

            buttons=[

                dict(
                    label="Revenue",
                    method="update",
                    args=[
                        {"visible":[True,False,False]},
                        {"title":"Revenue"}
                    ]
                ),

                dict(
                    label="Orders",
                    method="update",
                    args=[
                        {"visible":[False,True,False]},
                        {"title":"Orders"}
                    ]
                ),

                dict(
                    label="Average",
                    method="update",
                    args=[
                        {"visible":[False,False,True]},
                        {"title":"Average Order Value"}
                    ]
                )

            ]

        )

    ]

)

fig3.write_html(
    "interactive_charts/chart3_metric_selector.html"
)

print("Chart 3 Created")

# ==========================================================
# CHART 4
# Zoom / Pan Demo
# ==========================================================

fig4 = go.Figure()

fig4.add_trace(

    go.Scatter(

        x=df["transaction_date"],

        y=df["amount"],

        mode="markers",

        marker=dict(

            size=10,

            color=df["amount"],

            colorscale="Viridis"

        ),

        hovertemplate=
        "<b>%{x}</b><br>"
        "Amount : $%{y:.2f}<extra></extra>"

    )

)

fig4.update_layout(

    title="Interactive Transaction Explorer",

    dragmode="zoom",

    hovermode="closest"

)

fig4.write_html(
    "interactive_charts/chart4_interactive.html"
)

print("Chart 4 Created")

print("=" * 60)
print("ALL PLOTLY CHARTS GENERATED")
print("=" * 60)