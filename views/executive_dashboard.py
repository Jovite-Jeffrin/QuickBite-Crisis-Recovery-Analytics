import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_engine
from utils.sql_loader import load_sql


def show():
    """
    Render the Executive Dashboard.
    """

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.title("Executive Dashboard")
    st.subheader("Business Performance Overview")

    st.write(
        """
        This dashboard provides a high-level summary of QuickBite's
        operational, customer, and financial performance.
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

    # --------------------------------------------------
    # Executive KPIs
    # --------------------------------------------------

    try:
        kpi_query = load_sql("sql/executive_kpis.sql")

        kpi_df = pd.read_sql(
            kpi_query,
            engine
        )

    except Exception as e:
        st.error("Unable to load executive KPI data.")
        st.exception(e)
        return

    kpis = kpi_df.iloc[0]

    total_orders = int(kpis["total_orders"])
    total_revenue = float(kpis["total_revenue"])
    total_customers = int(kpis["total_customers"])
    average_rating = float(kpis["average_rating"])
    cancellation_rate = float(kpis["cancellation_rate"])
    average_delivery_time = float(
        kpis["average_delivery_time"]
    )

    # --------------------------------------------------
    # KPI Section
    # --------------------------------------------------

    st.header("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Orders",
            value=f"{total_orders:,}"
        )

    with col2:
        st.metric(
            label="Total Revenue",
            value=f"₹{total_revenue:,.0f}"
        )

    with col3:
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}"
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            label="Average Rating",
            value=f"{average_rating:.2f}"
        )

    with col5:
        st.metric(
            label="Cancellation Rate",
            value=f"{cancellation_rate:.2f}%"
        )

    with col6:
        st.metric(
            label="Average Delivery Time",
            value=f"{average_delivery_time:.1f} min"
        )

    st.divider()

    # --------------------------------------------------
    # Monthly Order Trend
    # --------------------------------------------------

    st.header("Monthly Order Trend")

    try:
        orders_query = load_sql(
            "sql/monthly_orders.sql"
        )

        monthly_orders = pd.read_sql(
            orders_query,
            engine
        )

    except Exception as e:
        st.error("Unable to load monthly order data.")
        st.exception(e)
        return

    monthly_orders["order_month"] = pd.to_datetime(
        monthly_orders["order_month"]
    )

    order_fig = px.line(
        monthly_orders,
        x="order_month",
        y="total_orders",
        markers=True,
        labels={
            "order_month": "Month",
            "total_orders": "Orders"
        }
    )

    order_fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "Orders: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    order_fig.add_vrect(
        x0="2025-06-01",
        x1="2025-10-01",
        fillcolor="gray",
        opacity=0.12,
        line_width=0,
        annotation_text="Crisis Period",
        annotation_position="top left"
    )

    order_fig.add_vline(
        x="2025-06-01",
        line_dash="dash",
        line_width=2,
        annotation_text="Crisis Begins",
        annotation_position="top"
    )

    order_fig.update_layout(
        hovermode="x unified",
        height=450,
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
        order_fig,
        width="stretch"
    )

    st.divider()

    # --------------------------------------------------
    # Monthly Revenue Trend
    # --------------------------------------------------

    st.header("Monthly Revenue Trend")

    try:
        revenue_query = load_sql(
            "sql/monthly_revenue.sql"
        )

        monthly_revenue = pd.read_sql(
            revenue_query,
            engine
        )

    except Exception as e:
        st.error("Unable to load monthly revenue data.")
        st.exception(e)
        return

    monthly_revenue["order_month"] = pd.to_datetime(
        monthly_revenue["order_month"]
    )

    revenue_fig = px.bar(
        monthly_revenue,
        x="order_month",
        y="total_revenue",
        labels={
            "order_month": "Month",
            "total_revenue": "Revenue"
        }
    )

    revenue_fig.update_traces(
        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "Revenue: ₹%{y:,.2f}"
            "<extra></extra>"
        )
    )

    revenue_fig.add_vrect(
        x0="2025-06-01",
        x1="2025-10-01",
        fillcolor="gray",
        opacity=0.12,
        line_width=0,
        annotation_text="Crisis Period",
        annotation_position="top left"
    )

    revenue_fig.add_vline(
        x="2025-06-01",
        line_dash="dash",
        line_width=2,
        annotation_text="Crisis Begins",
        annotation_position="top"
    )

    revenue_fig.update_layout(
        height=450,
        xaxis=dict(
            tickformat="%b %Y",
            title="Month"
        ),
        yaxis=dict(
            title="Revenue",
            tickprefix="₹",
            tickformat=",.0f"
        ),
        margin=dict(
            t=60,
            b=40,
            l=60,
            r=30
        )
    )

    st.plotly_chart(
        revenue_fig,
        width="stretch"
    )

    st.divider()

    # --------------------------------------------------
    # Monthly Customer Rating Trend
    # --------------------------------------------------

    st.header("Monthly Customer Rating Trend")

    try:
        ratings_query = load_sql(
            "sql/monthly_ratings.sql"
        )

        monthly_ratings = pd.read_sql(
            ratings_query,
            engine
        )

    except Exception as e:
        st.error("Unable to load monthly rating data.")
        st.exception(e)
        return

    monthly_ratings["review_month"] = pd.to_datetime(
        monthly_ratings["review_month"]
    )

    rating_fig = px.line(
        monthly_ratings,
        x="review_month",
        y="average_rating",
        markers=True,
        labels={
            "review_month": "Month",
            "average_rating": "Average Rating"
        }
    )

    rating_fig.update_traces(
        line=dict(width=3),
        marker=dict(size=9),
        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "Average Rating: %{y:.2f}"
            "<extra></extra>"
        )
    )

    # Highlight crisis period
    rating_fig.add_vrect(
        x0="2025-06-01",
        x1="2025-10-01",
        fillcolor="gray",
        opacity=0.12,
        line_width=0,
        annotation_text="Crisis Period",
        annotation_position="top left"
    )

    # Crisis start marker
    rating_fig.add_vline(
        x="2025-06-01",
        line_dash="dash",
        line_width=2,
        annotation_text="Crisis Begins",
        annotation_position="top"
    )

    # 4.0 rating reference line
    rating_fig.add_hline(
        y=4.0,
        line_dash="dot",
        line_width=1.5,
        annotation_text="4.0 Rating Benchmark",
        annotation_position="bottom right"
    )

    rating_fig.update_layout(
        hovermode="x unified",
        height=450,
        xaxis=dict(
            tickformat="%b %Y",
            title="Month"
        ),
        yaxis=dict(
            title="Average Rating",
            range=[0, 5],
            dtick=0.5
        ),
        margin=dict(
            t=60,
            b=40,
            l=60,
            r=30
        )
    )

    st.plotly_chart(
        rating_fig,
        width="stretch"
    )

    st.divider()

    # --------------------------------------------------
    # Dashboard Summary
    # --------------------------------------------------

    st.header("Dashboard Summary")

    st.write(
        """
        The Executive Dashboard provides an initial view of QuickBite's
        business performance across demand, revenue, and customer experience.
        Detailed analysis of the crisis impact is explored in the subsequent
        analytical sections.
        """
    )