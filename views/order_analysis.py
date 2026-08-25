import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_engine
from utils.sql_loader import load_sql


def show():
    """
    Render the Order Analysis page.
    """

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.title("Order Analysis")
    st.subheader("Understanding demand changes during the crisis")

    st.write(
        """
        This section analyzes order volume before and during the crisis,
        including overall demand changes and city-level impact.
        """
    )

    st.divider()

    # --------------------------------------------------
    # Database Connection
    # --------------------------------------------------

    try:
        engine = get_engine()

        with engine.connect():
            pass

    except Exception as e:
        st.error("Unable to connect to PostgreSQL.")
        st.exception(e)
        return

    # ==================================================
    # Q1 — Overall Order Decline
    # ==================================================

    st.header("Q1 — Overall Order Decline")

    st.write(
        """
        How did overall order volume change during the crisis compared
        with the pre-crisis period?
        """
    )

    # --------------------------------------------------
    # Q1 Comparison Data
    # --------------------------------------------------

    try:
        comparison_query = load_sql(
            "sql/q1_order_decline.sql"
        )

        comparison_df = pd.read_sql(
            comparison_query,
            engine
        )

    except Exception as e:
        st.error("Unable to load Q1 order comparison data.")
        st.exception(e)
        return

    if comparison_df.empty:
        st.warning("No order data is available for Q1.")
        return

    comparison = comparison_df.iloc[0]

    pre_crisis_orders = int(
        comparison["pre_crisis_orders"]
    )

    crisis_orders = int(
        comparison["crisis_orders"]
    )

    order_decline = int(
        comparison["order_decline"]
    )

    order_decline_percentage = float(
        comparison["order_decline_percentage"]
    )

    avg_monthly_pre_crisis = float(
        comparison["avg_monthly_pre_crisis_orders"]
    )

    avg_monthly_crisis = float(
        comparison["avg_monthly_crisis_orders"]
    )

    monthly_order_decline_percentage = float(
        comparison["monthly_order_decline_percentage"]
    )

    # --------------------------------------------------
    # Q1 KPI Section
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Pre-Crisis Orders",
            value=f"{pre_crisis_orders:,}"
        )

    with col2:
        st.metric(
            label="Crisis Orders",
            value=f"{crisis_orders:,}",
            delta=f"-{order_decline_percentage:.2f}%",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            label="Absolute Order Decline",
            value=f"{order_decline:,}"
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            label="Avg. Monthly Orders — Pre-Crisis",
            value=f"{avg_monthly_pre_crisis:,.0f}"
        )

    with col5:
        st.metric(
            label="Avg. Monthly Orders — Crisis",
            value=f"{avg_monthly_crisis:,.0f}",
            delta=f"-{monthly_order_decline_percentage:.2f}%",
            delta_color="inverse"
        )

    # --------------------------------------------------
    # Q1 Comparison Chart
    # --------------------------------------------------

    comparison_chart_df = pd.DataFrame(
        {
            "Phase": [
                "Pre-Crisis",
                "Crisis"
            ],
            "Orders": [
                pre_crisis_orders,
                crisis_orders
            ]
        }
    )

    comparison_fig = px.bar(
        comparison_chart_df,
        x="Phase",
        y="Orders",
        text="Orders",
        labels={
            "Phase": "Period",
            "Orders": "Number of Orders"
        }
    )

    comparison_fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Orders: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    comparison_fig.update_layout(
        height=450,
        yaxis=dict(
            title="Number of Orders",
            tickformat=","
        ),
        xaxis=dict(
            title=""
        ),
        margin=dict(
            t=40,
            b=40,
            l=60,
            r=30
        )
    )

    st.plotly_chart(
        comparison_fig,
        width="stretch"
    )

    # --------------------------------------------------
    # Q1 Monthly Trend
    # --------------------------------------------------

    st.subheader("Monthly Order Trend")

    try:
        monthly_query = load_sql(
            "sql/q1_monthly_orders.sql"
        )

        monthly_orders = pd.read_sql(
            monthly_query,
            engine
        )

    except Exception as e:
        st.error("Unable to load monthly order trend.")
        st.exception(e)
        return

    if monthly_orders.empty:
        st.warning("No monthly order data is available.")
        return

    monthly_orders["order_month"] = pd.to_datetime(
        monthly_orders["order_month"]
    )

    monthly_fig = px.line(
        monthly_orders,
        x="order_month",
        y="total_orders",
        markers=True,
        labels={
            "order_month": "Month",
            "total_orders": "Orders"
        }
    )

    monthly_fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "Orders: %{y:,.0f}<br>"
            "Phase: %{customdata[0]}"
            "<extra></extra>"
        ),
        customdata=monthly_orders[["phase"]]
    )

    monthly_fig.add_vrect(
        x0="2025-06-01",
        x1="2025-10-01",
        fillcolor="gray",
        opacity=0.12,
        line_width=0,
        annotation_text="Crisis Period",
        annotation_position="top left"
    )

    monthly_fig.add_vline(
        x="2025-06-01",
        line_dash="dash",
        line_width=2,
        annotation_text="Crisis Begins",
        annotation_position="top"
    )

    monthly_fig.update_layout(
        hovermode="x unified",
        height=500,
        xaxis=dict(
            tickformat="%b %Y",
            title="Month"
        ),
        yaxis=dict(
            title="Number of Orders",
            tickformat=","
        ),
        margin=dict(
            t=60,
            b=40,
            l=60,
            r=30
        )
    )

    st.plotly_chart(
        monthly_fig,
        width="stretch"
    )

    # --------------------------------------------------
    # Q1 Key Finding
    # --------------------------------------------------

    st.subheader("Q1 — Key Finding")

    if monthly_order_decline_percentage > 0:

        st.write(
            f"""
            Order volume declined during the crisis period compared with
            the pre-crisis period. Total orders decreased by
            **{order_decline_percentage:.2f}%**, representing an absolute
            decline of **{order_decline:,} orders**.

            After accounting for the difference in period length, average
            monthly order volume declined by
            **{monthly_order_decline_percentage:.2f}%**, from approximately
            **{avg_monthly_pre_crisis:,.0f} orders per month** before the
            crisis to **{avg_monthly_crisis:,.0f} orders per month** during
            the crisis.
            """
        )

    elif monthly_order_decline_percentage < 0:

        st.write(
            f"""
            Contrary to the expected decline, average monthly order volume
            increased during the crisis period by
            **{abs(monthly_order_decline_percentage):.2f}%**.
            """
        )

    else:

        st.write(
            """
            Average monthly order volume remained broadly unchanged between
            the pre-crisis and crisis periods.
            """
        )

    st.divider()

    # ==================================================
    # Q2 — City-Level Order Decline
    # ==================================================

    st.header("Q2 — City-Level Order Decline")

    st.write(
        """
        Which top 5 city groups experienced the highest percentage decline
        in orders during the crisis compared with the pre-crisis period?
        """
    )

    # --------------------------------------------------
    # Q2 Data
    # --------------------------------------------------

    try:
        city_query = load_sql(
            "sql/q2_city_order_decline.sql"
        )

        city_decline = pd.read_sql(
            city_query,
            engine
        )

    except Exception as e:
        st.error("Unable to load Q2 city-level order data.")
        st.exception(e)
        return

    if city_decline.empty:
        st.warning("No city-level order data is available for Q2.")
        return

    # --------------------------------------------------
    # Q2 Summary Table
    # --------------------------------------------------

    display_city_decline = city_decline.copy()

    display_city_decline.columns = [
        "City",
        "Pre-Crisis Orders",
        "Crisis Orders",
        "Order Decline",
        "Decline (%)"
    ]

    display_city_decline["Pre-Crisis Orders"] = (
        display_city_decline["Pre-Crisis Orders"]
        .map(lambda x: f"{int(x):,}")
    )

    display_city_decline["Crisis Orders"] = (
        display_city_decline["Crisis Orders"]
        .map(lambda x: f"{int(x):,}")
    )

    display_city_decline["Order Decline"] = (
        display_city_decline["Order Decline"]
        .map(lambda x: f"{int(x):,}")
    )

    display_city_decline["Decline (%)"] = (
        display_city_decline["Decline (%)"]
        .map(lambda x: f"{x:.2f}%")
    )

    st.dataframe(
        display_city_decline,
        hide_index=True,
        width="stretch"
    )

    # --------------------------------------------------
    # Q2 Visualization
    # --------------------------------------------------

    city_fig = px.bar(
        city_decline,
        x="decline_percentage",
        y="city",
        orientation="h",
        text="decline_percentage",
        labels={
            "decline_percentage": "Order Decline (%)",
            "city": "City"
        },
        custom_data=[
            city_decline["pre_crisis_orders"],
            city_decline["crisis_orders"],
            city_decline["order_decline"]
        ]
    )

    city_fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Decline: %{x:.2f}%<br>"
            "Pre-Crisis Orders: %{customdata[0]:,.0f}<br>"
            "Crisis Orders: %{customdata[1]:,.0f}<br>"
            "Order Decline: %{customdata[2]:,.0f}"
            "<extra></extra>"
        )
    )

    city_fig.update_layout(
        height=450,
        xaxis=dict(
            title="Order Decline (%)",
            ticksuffix="%"
        ),
        yaxis=dict(
            title=""
        ),
        margin=dict(
            t=40,
            b=40,
            l=100,
            r=60
        )
    )

    st.plotly_chart(
        city_fig,
        width="stretch"
    )

    # --------------------------------------------------
    # Q2 Key Finding
    # --------------------------------------------------

    top_city = city_decline.iloc[0]

    st.subheader("Q2 — Key Finding")

    st.write(
        f"""
        **{top_city['city']}** experienced the highest percentage decline
        in orders, with a decrease of **{top_city['decline_percentage']:.2f}%**
        compared with its pre-crisis order volume.

        The chart and table above show the five cities with the largest
        proportional decline in demand during the crisis.
        """
    )