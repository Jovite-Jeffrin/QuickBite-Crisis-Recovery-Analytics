import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_engine


def load_sql(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def show():

    # ==================================================
    # PAGE HEADER
    # ==================================================

    st.title(
        "QuickBite Crisis Executive Dashboard"
    )

    st.write(
        """
        Executive overview of QuickBite's business performance
        before and during the crisis period.
        """
    )

    # ==================================================
    # DATABASE CONNECTION
    # ==================================================

    try:

        engine = get_engine()

    except Exception as e:

        st.error(
            "Unable to connect to the database."
        )

        st.exception(e)

        return

    # ==================================================
    # LOAD EXECUTIVE DATA
    # ==================================================

    try:

        query = load_sql(
            "sql/executive_dashboard.sql"
        )

        df = pd.read_sql(
            query,
            engine
        )

    except Exception as e:

        st.error(
            "Unable to load executive dashboard data."
        )

        st.exception(e)

        return

    if df.empty:

        st.warning(
            "No executive dashboard data is available."
        )

        return

    # ==================================================
    # PRE-CRISIS / CRISIS ROWS
    # ==================================================

    pre_crisis = df[
        df["phase"] == "Pre-Crisis"
    ].iloc[0]

    crisis = df[
        df["phase"] == "Crisis"
    ].iloc[0]

    # ==================================================
    # CHANGE CALCULATIONS
    # ==================================================

    revenue_change_pct = (
        (
            crisis["revenue"]
            -
            pre_crisis["revenue"]
        )
        /
        pre_crisis["revenue"]
    ) * 100

    order_change_pct = (
        (
            crisis["total_orders"]
            -
            pre_crisis["total_orders"]
        )
        /
        pre_crisis["total_orders"]
    ) * 100

    cancellation_change_pp = (
        crisis["cancellation_rate"]
        -
        pre_crisis["cancellation_rate"]
    )

    rating_change = (
        crisis["avg_rating"]
        -
        pre_crisis["avg_rating"]
    )

    delivery_change = (
        crisis["avg_delivery_time"]
        -
        pre_crisis["avg_delivery_time"]
    )

    # ==================================================
    # EXECUTIVE SUMMARY
    # ==================================================

    st.info(
        f"""
        QuickBite experienced significant deterioration across
        financial, customer and operational metrics during the
        crisis. Revenue declined by **{abs(revenue_change_pct):.1f}%**,
        total orders declined by **{abs(order_change_pct):.1f}%**,
        cancellation rate increased by
        **{cancellation_change_pp:.2f} percentage points**, and
        average customer rating changed by
        **{rating_change:.2f} points**.
        """
    )

    # ==================================================
    # CORE BUSINESS KPIs
    # ==================================================

    st.header(
        "Core Business Impact"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Revenue",
            f"₹{crisis['revenue']:,.0f}",
            delta=f"{revenue_change_pct:.1f}%",
            delta_color="inverse"
        )

    with col2:

        st.metric(
            "Total Orders",
            f"{crisis['total_orders']:,}",
            delta=f"{order_change_pct:.1f}%",
            delta_color="inverse"
        )

    with col3:

        st.metric(
            "Cancellation Rate",
            f"{crisis['cancellation_rate']:.2f}%",
            delta=f"{cancellation_change_pp:+.2f} pp",
            delta_color="inverse"
        )

    with col4:

        st.metric(
            "Average Rating",
            f"{crisis['avg_rating']:.2f}",
            delta=f"{rating_change:+.2f}",
            delta_color="inverse"
        )

    # ==================================================
    # OPERATIONAL KPI
    # ==================================================

    st.subheader(
        "Delivery Performance"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Average Delivery Time",
            f"{crisis['avg_delivery_time']:.2f} min",
            delta=f"+{delivery_change:.2f} min",
            delta_color="inverse"
        )

    with col2:

        st.metric(
            "Delivery Variance",
            f"{crisis['avg_delivery_variance']:.2f} min",
            delta=(
                f"{crisis['avg_delivery_variance'] - pre_crisis['avg_delivery_variance']:+.2f} min"
            ),
            delta_color="inverse"
        )

    # ==================================================
    # PHASE COMPARISON DATA
    # ==================================================

    st.header(
        "Pre-Crisis vs Crisis"
    )

    # --------------------------------------------------
    # REVENUE
    # --------------------------------------------------

    st.subheader(
        "Revenue Impact"
    )

    revenue_chart = df[
        [
            "phase",
            "revenue"
        ]
    ].copy()

    revenue_fig = px.bar(
        revenue_chart,
        x="phase",
        y="revenue",
        text="revenue",
        labels={
            "phase": "Period",
            "revenue": "Revenue"
        }
    )

    revenue_fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: ₹%{y:,.0f}"
            "<extra></extra>"
        )
    )

    revenue_fig.update_layout(
        height=400,
        xaxis_title="",
        yaxis_title="Revenue (₹)",
        margin=dict(
            t=40,
            b=40,
            l=70,
            r=30
        )
    )

    st.plotly_chart(
        revenue_fig,
        width="stretch"
    )

    # ==================================================
    # ORDERS & CANCELLATIONS
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Order Volume"
        )

        order_fig = px.bar(
            df,
            x="phase",
            y="total_orders",
            text="total_orders",
            labels={
                "phase": "Period",
                "total_orders": "Orders"
            }
        )

        order_fig.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Orders: %{y:,}"
                "<extra></extra>"
            )
        )

        order_fig.update_layout(
            height=400,
            xaxis_title="",
            yaxis_title="Orders",
            margin=dict(
                t=40,
                b=40,
                l=60,
                r=30
            )
        )

        st.plotly_chart(
            order_fig,
            width="stretch"
        )

    with col2:

        st.subheader(
            "Cancellation Rate"
        )

        cancellation_fig = px.bar(
            df,
            x="phase",
            y="cancellation_rate",
            text="cancellation_rate",
            labels={
                "phase": "Period",
                "cancellation_rate":
                    "Cancellation Rate (%)"
            }
        )

        cancellation_fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Cancellation Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )

        cancellation_fig.update_layout(
            height=400,
            xaxis_title="",
            yaxis_title="Cancellation Rate (%)",
            margin=dict(
                t=40,
                b=40,
                l=60,
                r=30
            )
        )

        st.plotly_chart(
            cancellation_fig,
            width="stretch"
        )

    # ==================================================
    # CUSTOMER EXPERIENCE
    # ==================================================

    st.header(
        "Customer Experience"
    )

    rating_fig = px.bar(
        df,
        x="phase",
        y="avg_rating",
        text="avg_rating",
        labels={
            "phase": "Period",
            "avg_rating": "Average Rating"
        }
    )

    rating_fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average Rating: %{y:.2f}"
            "<extra></extra>"
        )
    )

    rating_fig.update_layout(
        height=400,
        yaxis=dict(
            title="Average Rating",
            range=[0, 5]
        ),
        xaxis_title="",
        margin=dict(
            t=40,
            b=40,
            l=60,
            r=30
        )
    )

    st.plotly_chart(
        rating_fig,
        width="stretch"
    )

    # ==================================================
    # DELIVERY PERFORMANCE
    # ==================================================

    st.header(
        "Delivery Performance"
    )

    delivery_chart_df = df[
        [
            "phase",
            "avg_delivery_time",
            "avg_delivery_variance"
        ]
    ].melt(
        id_vars="phase",
        var_name="metric",
        value_name="minutes"
    )

    delivery_chart_df["metric"] = (
        delivery_chart_df["metric"].replace(
            {
                "avg_delivery_time":
                    "Actual Delivery Time",

                "avg_delivery_variance":
                    "Delivery Variance"
            }
        )
    )

    delivery_fig = px.bar(
        delivery_chart_df,
        x="phase",
        y="minutes",
        color="metric",
        barmode="group",
        text="minutes",
        labels={
            "phase": "Period",
            "minutes": "Minutes",
            "metric": "Metric"
        }
    )

    delivery_fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{fullData.name}: %{y:.2f} min"
            "<extra></extra>"
        )
    )

    delivery_fig.update_layout(
        height=450,
        xaxis_title="",
        yaxis_title="Minutes",
        margin=dict(
            t=40,
            b=40,
            l=60,
            r=30
        )
    )

    st.plotly_chart(
        delivery_fig,
        width="stretch"
    )

    # ==================================================
    # EXECUTIVE TAKEAWAYS
    # ==================================================

    st.header(
        "Executive Takeaways"
    )

    st.markdown(
        f"""
        **1. Financial Impact**

        Revenue declined by **{abs(revenue_change_pct):.1f}%**
        during the crisis.

        **2. Demand Impact**

        Total order volume declined by
        **{abs(order_change_pct):.1f}%**.

        **3. Operational Impact**

        Average delivery time increased by
        **{delivery_change:.2f} minutes**, while delivery variance
        increased substantially.

        **4. Customer Experience**

        Average customer rating changed from
        **{pre_crisis['avg_rating']:.2f}**
        to
        **{crisis['avg_rating']:.2f}**.

        **5. Cancellation Pressure**

        Cancellation rate increased from
        **{pre_crisis['cancellation_rate']:.2f}%**
        to
        **{crisis['cancellation_rate']:.2f}%**.
        """
    )