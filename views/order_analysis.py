import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_engine
from utils.sql_loader import load_sql


def show():

    # ==================================================
    # PAGE HEADER
    # ==================================================

    st.title("Order Analysis")

    st.subheader(
        "Understanding demand changes during the crisis"
    )

    st.write(
        """
        This section analyzes order volume before and during the crisis,
        including overall demand changes, city-level impact, and
        restaurant-level impact.
        """
    )

    st.divider()

    # ==================================================
    # DATABASE CONNECTION
    # ==================================================

    try:

        engine = get_engine()

        with engine.connect():
            pass

    except Exception as e:

        st.error(
            "Unable to connect to PostgreSQL."
        )

        st.exception(e)

        return

    # ==================================================
    # Q1 — OVERALL ORDER DECLINE
    # ==================================================

    st.header("Q1 — Overall Order Decline")

    st.write(
        """
        How did overall order volume change during the crisis compared
        with the pre-crisis period?
        """
    )

    try:

        comparison_query = load_sql(
            "sql/q1_order_decline.sql"
        )

        comparison_df = pd.read_sql(
            comparison_query,
            engine
        )

    except Exception as e:

        st.error(
            "Unable to load Q1 order comparison data."
        )

        st.exception(e)

        return

    if comparison_df.empty:

        st.warning(
            "No order data is available for Q1."
        )

    else:

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
            comparison[
                "avg_monthly_pre_crisis_orders"
            ]
        )

        avg_monthly_crisis = float(
            comparison[
                "avg_monthly_crisis_orders"
            ]
        )

        monthly_order_decline_percentage = float(
            comparison[
                "monthly_order_decline_percentage"
            ]
        )

        # --------------------------------------------------
        # Q1 KPIs
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
                delta=(
                    f"-{order_decline_percentage:.2f}%"
                ),
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
                delta=(
                    f"-{monthly_order_decline_percentage:.2f}%"
                ),
                delta_color="inverse"
            )

        # --------------------------------------------------
        # Q1 COMPARISON CHART
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
        # Q1 MONTHLY TREND
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

            st.error(
                "Unable to load monthly order trend."
            )

            st.exception(e)

            return

        if not monthly_orders.empty:

            monthly_orders["order_month"] = (
                pd.to_datetime(
                    monthly_orders["order_month"]
                )
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
                customdata=monthly_orders[
                    ["phase"]
                ],
                hovertemplate=(
                    "<b>%{x|%B %Y}</b><br>"
                    "Orders: %{y:,.0f}<br>"
                    "Phase: %{customdata[0]}"
                    "<extra></extra>"
                )
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
        # Q1 KEY FINDING
        # --------------------------------------------------

        st.subheader("Q1 — Key Finding")

        if monthly_order_decline_percentage > 0:

            st.write(
                f"""
                Order volume declined during the crisis period compared
                with the pre-crisis period. Total orders decreased by
                **{order_decline_percentage:.2f}%**, representing an
                absolute decline of **{order_decline:,} orders**.

                After accounting for the difference in period length,
                average monthly order volume declined by
                **{monthly_order_decline_percentage:.2f}%**, from
                approximately **{avg_monthly_pre_crisis:,.0f} orders
                per month** before the crisis to
                **{avg_monthly_crisis:,.0f} orders per month** during
                the crisis.
                """
            )

        elif monthly_order_decline_percentage < 0:

            st.write(
                f"""
                Contrary to the expected decline, average monthly order
                volume increased during the crisis period by
                **{abs(monthly_order_decline_percentage):.2f}%**.
                """
            )

        else:

            st.write(
                """
                Average monthly order volume remained broadly unchanged
                between the pre-crisis and crisis periods.
                """
            )

    st.divider()

    # ==================================================
    # Q2 — CITY-LEVEL ORDER DECLINE
    # ==================================================

    st.header("Q2 — City-Level Order Decline")

    st.write(
        """
        Which top 5 city groups experienced the highest percentage
        decline in orders during the crisis compared with the
        pre-crisis period?
        """
    )

    try:

        city_query = load_sql(
            "sql/q2_city_order_decline.sql"
        )

        city_decline = pd.read_sql(
            city_query,
            engine
        )

    except Exception as e:

        st.error(
            "Unable to load Q2 city-level order data."
        )

        st.exception(e)

        return

    if city_decline.empty:

        st.warning(
            "No city-level order data is available for Q2."
        )

    else:

        # --------------------------------------------------
        # Q2 TABLE
        # --------------------------------------------------

        display_city_decline = (
            city_decline[
                [
                    "city",
                    "pre_crisis_orders",
                    "crisis_orders",
                    "order_decline",
                    "decline_percentage"
                ]
            ]
            .copy()
        )

        display_city_decline = (
            display_city_decline.rename(
                columns={
                    "city": "City",
                    "pre_crisis_orders": "Pre-Crisis Orders",
                    "crisis_orders": "Crisis Orders",
                    "order_decline": "Order Decline",
                    "decline_percentage": "Decline (%)"
                }
            )
        )

        display_city_decline[
            "Pre-Crisis Orders"
        ] = (
            display_city_decline[
                "Pre-Crisis Orders"
            ].map(
                lambda x: f"{int(x):,}"
            )
        )

        display_city_decline[
            "Crisis Orders"
        ] = (
            display_city_decline[
                "Crisis Orders"
            ].map(
                lambda x: f"{int(x):,}"
            )
        )

        display_city_decline[
            "Order Decline"
        ] = (
            display_city_decline[
                "Order Decline"
            ].map(
                lambda x: f"{int(x):,}"
            )
        )

        display_city_decline[
            "Decline (%)"
        ] = (
            display_city_decline[
                "Decline (%)"
            ].map(
                lambda x: f"{x:.2f}%"
            )
        )

        st.dataframe(
            display_city_decline,
            hide_index=True,
            width="stretch"
        )

        # --------------------------------------------------
        # Q2 CHART
        # --------------------------------------------------

        city_fig = px.bar(
            city_decline,
            x="decline_percentage",
            y="city",
            orientation="h",
            text="decline_percentage",
            labels={
                "decline_percentage":
                    "Order Decline (%)",
                "city": "City"
            },
            custom_data=[
                city_decline[
                    "pre_crisis_orders"
                ],
                city_decline[
                    "crisis_orders"
                ],
                city_decline[
                    "order_decline"
                ]
            ]
        )

        city_fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Decline: %{x:.2f}%<br>"
                "Pre-Crisis Orders: "
                "%{customdata[0]:,.0f}<br>"
                "Crisis Orders: "
                "%{customdata[1]:,.0f}<br>"
                "Order Decline: "
                "%{customdata[2]:,.0f}"
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
        # Q2 KEY FINDING
        # --------------------------------------------------

        top_city = city_decline.iloc[0]

        st.subheader("Q2 — Key Finding")

        st.write(
            f"""
            **{top_city['city']}** experienced the highest percentage
            decline in orders, with a decrease of
            **{top_city['decline_percentage']:.2f}%**
            compared with its pre-crisis order volume.

            The chart and table above show the five cities with the
            largest proportional decline in demand during the crisis.
            """
        )

    st.divider()

    # ==================================================
    # Q3 — RESTAURANT-LEVEL ORDER DECLINE
    # ==================================================

    st.header("Q3 — Restaurant-Level Order Decline")

    st.write(
        """
        Among restaurants with at least 50 pre-crisis orders, which
        high-volume restaurants experienced the largest percentage
        decline in order counts during the crisis period?
        """
    )

    try:

        restaurant_query = load_sql(
            "sql/q3_restaurant_order_decline.sql"
        )

        restaurant_decline = pd.read_sql(
            restaurant_query,
            engine
        )

    except Exception as e:

        st.error(
            "Unable to load Q3 restaurant-level order data."
        )

        st.exception(e)

        return

    if restaurant_decline.empty:

        st.warning(
            "No restaurant-level order data is available for Q3."
        )

    else:

        # --------------------------------------------------
        # Q3 DATA VALIDATION
        # --------------------------------------------------

        required_columns = [
            "restaurant_name",
            "pre_crisis_orders",
            "crisis_orders",
            "order_decline",
            "decline_percentage"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in restaurant_decline.columns
        ]

        if missing_columns:

            st.error(
                "Q3 SQL result is missing required columns:"
            )

            st.write(missing_columns)

            st.write(
                "Columns returned by PostgreSQL:"
            )

            st.write(
                list(restaurant_decline.columns)
            )

            return

        # --------------------------------------------------
        # Q3 SUMMARY TABLE
        # --------------------------------------------------

        display_restaurant_decline = (
            restaurant_decline[
                [
                    "restaurant_name",
                    "pre_crisis_orders",
                    "crisis_orders",
                    "order_decline",
                    "decline_percentage"
                ]
            ]
            .copy()
        )

        display_restaurant_decline = (
            display_restaurant_decline.rename(
                columns={
                    "restaurant_name": "Restaurant",
                    "pre_crisis_orders": "Pre-Crisis Orders",
                    "crisis_orders": "Crisis Orders",
                    "order_decline": "Order Decline",
                    "decline_percentage": "Decline (%)"
                }
            )
        )

        display_restaurant_decline[
            "Pre-Crisis Orders"
        ] = (
            display_restaurant_decline[
                "Pre-Crisis Orders"
            ].map(
                lambda x: f"{int(x):,}"
            )
        )

        display_restaurant_decline[
            "Crisis Orders"
        ] = (
            display_restaurant_decline[
                "Crisis Orders"
            ].map(
                lambda x: f"{int(x):,}"
            )
        )

        display_restaurant_decline[
            "Order Decline"
        ] = (
            display_restaurant_decline[
                "Order Decline"
            ].map(
                lambda x: f"{int(x):,}"
            )
        )

        display_restaurant_decline[
            "Decline (%)"
        ] = (
            display_restaurant_decline[
                "Decline (%)"
            ].map(
                lambda x: f"{float(x):.2f}%"
            )
        )

        st.dataframe(
            display_restaurant_decline,
            hide_index=True,
            width="stretch"
        )

        # --------------------------------------------------
        # Q3 VISUALIZATION
        # --------------------------------------------------

        restaurant_fig = px.bar(
            restaurant_decline,
            x="decline_percentage",
            y="restaurant_name",
            orientation="h",
            text="decline_percentage",
            labels={
                "decline_percentage": "Order Decline (%)",
                "restaurant_name": "Restaurant"
            },
            custom_data=[
                restaurant_decline[
                    "pre_crisis_orders"
                ],
                restaurant_decline[
                    "crisis_orders"
                ],
                restaurant_decline[
                    "order_decline"
                ]
            ]
        )

        restaurant_fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Order Decline: %{x:.2f}%<br>"
                "Pre-Crisis Orders: %{customdata[0]:,.0f}<br>"
                "Crisis Orders: %{customdata[1]:,.0f}<br>"
                "Absolute Decline: %{customdata[2]:,.0f}"
                "<extra></extra>"
            )
        )

        restaurant_fig.update_layout(
            height=550,

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
                l=220,
                r=60
            )
        )

        st.plotly_chart(
            restaurant_fig,
            width="stretch"
        )

        # --------------------------------------------------
        # Q3 KEY FINDING
        # --------------------------------------------------

        top_restaurant = (
            restaurant_decline.iloc[0]
        )

        st.subheader(
            "Q3 — Key Finding"
        )

        st.write(
            f"""
            **{top_restaurant['restaurant_name']}**
            experienced the largest percentage decline among the
            qualifying high-volume restaurants, with orders declining
            by **{float(top_restaurant['decline_percentage']):.2f}%**.

            The restaurant recorded
            **{int(top_restaurant['pre_crisis_orders']):,}**
            pre-crisis orders compared with
            **{int(top_restaurant['crisis_orders']):,}**
            orders during the crisis.
            """
        )



        st.divider()

        # ==================================================
        # Q4 — CANCELLATION ANALYSIS
        # ==================================================

        st.header("Q4 — Cancellation Analysis")

        st.write(
            """
            How did the cancellation rate change between the pre-crisis
            and crisis periods, and which cities were most affected?
            """
        )

        # --------------------------------------------------
        # OVERALL CANCELLATION RATE
        # --------------------------------------------------

        try:

            cancellation_query = load_sql(
                "sql/q4_cancellation_analysis.sql"
            )

            cancellation_df = pd.read_sql(
                cancellation_query,
                engine
            )

        except Exception as e:

            st.error(
                "Unable to load overall cancellation data."
            )

            st.exception(e)

            return

        if cancellation_df.empty:

            st.warning(
                "No cancellation data is available."
            )

        else:

            pre_crisis = cancellation_df[
                cancellation_df["phase"] == "Pre-Crisis"
            ].iloc[0]

            crisis = cancellation_df[
                cancellation_df["phase"] == "Crisis"
            ].iloc[0]

            cancellation_change = (
                float(crisis["cancellation_rate"])
                - float(pre_crisis["cancellation_rate"])
            )

            # --------------------------------------------------
            # KPI CARDS
            # --------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Pre-Crisis Cancellation Rate",
                    f"{pre_crisis['cancellation_rate']:.2f}%"
                )

            with col2:

                st.metric(
                    "Crisis Cancellation Rate",
                    f"{crisis['cancellation_rate']:.2f}%"
                )

            with col3:

                st.metric(
                    "Increase",
                    f"+{cancellation_change:.2f} pp"
                )

            # --------------------------------------------------
            # OVERALL CANCELLATION CHART
            # --------------------------------------------------

            cancellation_chart = cancellation_df[
                [
                    "phase",
                    "cancellation_rate"
                ]
            ].copy()

            cancellation_fig = px.bar(
                cancellation_chart,
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
                yaxis=dict(
                    title="Cancellation Rate (%)",
                    ticksuffix="%"
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
                cancellation_fig,
                width="stretch"
            )

        # --------------------------------------------------
        # CITY-LEVEL CANCELLATION ANALYSIS
        # --------------------------------------------------

        st.subheader(
            "City-Level Cancellation Impact"
        )

        try:

            city_cancellation_query = load_sql(
                "sql/q4_city_cancellation.sql"
            )

            city_cancellation = pd.read_sql(
                city_cancellation_query,
                engine
            )

        except Exception as e:

            st.error(
                "Unable to load city-level cancellation data."
            )

            st.exception(e)

            return

        if city_cancellation.empty:

            st.warning(
                "No city-level cancellation data is available."
            )

        else:

            # --------------------------------------------------
            # CITY TABLE
            # --------------------------------------------------

            city_display = city_cancellation[
                [
                    "city",
                    "pre_crisis_cancellation_rate",
                    "crisis_cancellation_rate",
                    "cancellation_rate_change_pp"
                ]
            ].copy()

            city_display = city_display.rename(
                columns={
                    "city": "City",
                    "pre_crisis_cancellation_rate":
                        "Pre-Crisis Rate",
                    "crisis_cancellation_rate":
                        "Crisis Rate",
                    "cancellation_rate_change_pp":
                        "Change (pp)"
                }
            )

            city_display["Pre-Crisis Rate"] = (
                city_display["Pre-Crisis Rate"]
                .map(lambda x: f"{float(x):.2f}%")
            )

            city_display["Crisis Rate"] = (
                city_display["Crisis Rate"]
                .map(lambda x: f"{float(x):.2f}%")
            )

            city_display["Change (pp)"] = (
                city_display["Change (pp)"]
                .map(lambda x: f"+{float(x):.2f} pp")
            )

            st.dataframe(
                city_display,
                hide_index=True,
                width="stretch"
            )

            # --------------------------------------------------
            # CITY IMPACT CHART
            # --------------------------------------------------

            city_fig = px.bar(
                city_cancellation,
                x="cancellation_rate_change_pp",
                y="city",
                orientation="h",
                text="cancellation_rate_change_pp",
                labels={
                    "cancellation_rate_change_pp":
                        "Increase in Cancellation Rate (pp)",
                    "city": "City"
                },
                custom_data=[
                    city_cancellation[
                        "pre_crisis_cancellation_rate"
                    ],
                    city_cancellation[
                        "crisis_cancellation_rate"
                    ]
                ]
            )

            city_fig.update_traces(
                texttemplate="+%{text:.2f} pp",
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Pre-Crisis: %{customdata[0]:.2f}%<br>"
                    "Crisis: %{customdata[1]:.2f}%<br>"
                    "Increase: +%{x:.2f} pp"
                    "<extra></extra>"
                )
            )

            city_fig.update_layout(
                height=500,
                xaxis=dict(
                    title="Increase in Cancellation Rate (pp)"
                ),
                yaxis=dict(
                    title=""
                ),
                margin=dict(
                    t=40,
                    b=40,
                    l=100,
                    r=70
                )
            )

            st.plotly_chart(
                city_fig,
                width="stretch"
            )

            # --------------------------------------------------
            # KEY FINDING
            # --------------------------------------------------

            most_affected_city = (
                city_cancellation.iloc[0]
            )

            st.subheader(
                "Q4 — Key Finding"
            )

            st.write(
                f"""
                The overall cancellation rate increased from
                **{pre_crisis['cancellation_rate']:.2f}%**
                before the crisis to
                **{crisis['cancellation_rate']:.2f}%**
                during the crisis, representing a
                **+{cancellation_change:.2f} percentage-point increase**.

                **{most_affected_city['city']}** was the most affected city,
                with its cancellation rate increasing from
                **{most_affected_city['pre_crisis_cancellation_rate']:.2f}%**
                to
                **{most_affected_city['crisis_cancellation_rate']:.2f}%**,
                an increase of
                **+{most_affected_city['cancellation_rate_change_pp']:.2f}
                percentage points**.
                """
            )



        st.divider()

        # ==================================================
        # Q5 — DELIVERY SLA
        # ==================================================

        st.header("Q5 — Delivery SLA Performance")

        st.write(
            """
            How did delivery performance change during the crisis, and
            did SLA compliance deteriorate significantly?
            """
        )

        try:

            sla_query = load_sql(
                "sql/q5_delivery_sla.sql"
            )

            sla_df = pd.read_sql(
                sla_query,
                engine
            )

        except Exception as e:

            st.error(
                "Unable to load delivery SLA data."
            )

            st.exception(e)

            return

        if sla_df.empty:

            st.warning(
                "No delivery SLA data is available."
            )

        else:

            # --------------------------------------------------
            # GET PHASE VALUES
            # --------------------------------------------------

            pre_crisis_sla = sla_df[
                sla_df["phase"] == "Pre-Crisis"
            ].iloc[0]

            crisis_sla = sla_df[
                sla_df["phase"] == "Crisis"
            ].iloc[0]

            actual_delivery_change = (
                float(
                    crisis_sla[
                        "avg_actual_delivery_mins"
                    ]
                )
                -
                float(
                    pre_crisis_sla[
                        "avg_actual_delivery_mins"
                    ]
                )
            )

            variance_change = (
                float(
                    crisis_sla[
                        "avg_delivery_variance_mins"
                    ]
                )
                -
                float(
                    pre_crisis_sla[
                        "avg_delivery_variance_mins"
                    ]
                )
            )

            sla_compliance_change = (
                float(
                    crisis_sla[
                        "sla_compliance_rate"
                    ]
                )
                -
                float(
                    pre_crisis_sla[
                        "sla_compliance_rate"
                    ]
                )
            )

            # --------------------------------------------------
            # KPI CARDS
            # --------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Pre-Crisis Avg. Delivery",
                    f"{pre_crisis_sla['avg_actual_delivery_mins']:.2f} min"
                )

            with col2:

                st.metric(
                    "Crisis Avg. Delivery",
                    f"{crisis_sla['avg_actual_delivery_mins']:.2f} min",
                    delta=f"+{actual_delivery_change:.2f} min",
                    delta_color="inverse"
                )

            with col3:

                st.metric(
                    "SLA Compliance",
                    f"{crisis_sla['sla_compliance_rate']:.2f}%",
                    delta=f"{sla_compliance_change:.2f} pp",
                    delta_color="inverse"
                )

            # --------------------------------------------------
            # DELIVERY TIME COMPARISON
            # --------------------------------------------------

            st.subheader(
                "Average Delivery Time"
            )

            delivery_chart_df = sla_df[
                [
                    "phase",
                    "avg_actual_delivery_mins",
                    "avg_expected_delivery_mins"
                ]
            ].copy()

            delivery_chart_df = delivery_chart_df.melt(
                id_vars="phase",
                value_vars=[
                    "avg_actual_delivery_mins",
                    "avg_expected_delivery_mins"
                ],
                var_name="metric",
                value_name="minutes"
            )

            delivery_chart_df["metric"] = (
                delivery_chart_df["metric"].replace(
                    {
                        "avg_actual_delivery_mins":
                            "Actual Delivery",
                        "avg_expected_delivery_mins":
                            "Expected Delivery"
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
                    "metric": "Delivery Type"
                }
            )

            delivery_fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "%{fullData.name}: %{y:.2f} minutes"
                    "<extra></extra>"
                )
            )

            delivery_fig.update_layout(
                height=450,
                yaxis=dict(
                    title="Delivery Time (Minutes)"
                ),
                xaxis=dict(
                    title=""
                ),
                margin=dict(
                    t=50,
                    b=40,
                    l=60,
                    r=30
                )
            )

            st.plotly_chart(
                delivery_fig,
                width="stretch"
            )

            # --------------------------------------------------
            # SLA COMPLIANCE CHART
            # --------------------------------------------------

            st.subheader(
                "SLA Compliance"
            )

            sla_chart_df = sla_df[
                [
                    "phase",
                    "sla_compliance_rate"
                ]
            ].copy()

            sla_fig = px.bar(
                sla_chart_df,
                x="phase",
                y="sla_compliance_rate",
                text="sla_compliance_rate",
                labels={
                    "phase": "Period",
                    "sla_compliance_rate":
                        "SLA Compliance (%)"
                }
            )

            sla_fig.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "SLA Compliance: %{y:.2f}%"
                    "<extra></extra>"
                )
            )

            sla_fig.update_layout(
                height=400,
                yaxis=dict(
                    title="SLA Compliance (%)",
                    ticksuffix="%"
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
                sla_fig,
                width="stretch"
            )

            # --------------------------------------------------
            # KEY FINDING
            # --------------------------------------------------

            st.subheader(
                "Q5 — Key Finding"
            )

            st.write(
                f"""
                Delivery performance deteriorated substantially during the
                crisis. Average actual delivery time increased from
                **{pre_crisis_sla['avg_actual_delivery_mins']:.2f} minutes**
                to
                **{crisis_sla['avg_actual_delivery_mins']:.2f} minutes**,
                an increase of **{actual_delivery_change:.2f} minutes**.

                At the same time, the average gap between actual and expected
                delivery increased from
                **{pre_crisis_sla['avg_delivery_variance_mins']:.2f} minutes**
                to
                **{crisis_sla['avg_delivery_variance_mins']:.2f} minutes**.

                Most importantly, SLA compliance fell from
                **{pre_crisis_sla['sla_compliance_rate']:.2f}%**
                to
                **{crisis_sla['sla_compliance_rate']:.2f}%**,
                a deterioration of
                **{abs(sla_compliance_change):.2f} percentage points**.
                """
            )



        st.divider()

        # ==================================================
        # Q6 — RATINGS FLUCTUATION
        # ==================================================

        st.header("Q6 — Customer Ratings Fluctuation")

        st.write(
            """
            How did customer ratings change month-by-month, and which
            months experienced the sharpest decline?
            """
        )

        try:

            ratings_query = load_sql(
                "sql/q6_ratings_fluctuation.sql"
            )

            ratings_df = pd.read_sql(
                ratings_query,
                engine
            )

        except Exception as e:

            st.error(
                "Unable to load monthly ratings data."
            )

            st.exception(e)

            return

        if ratings_df.empty:

            st.warning(
                "No monthly ratings data is available."
            )

        else:

            # --------------------------------------------------
            # PREPARE DATA
            # --------------------------------------------------

            ratings_df["review_month"] = pd.to_datetime(
                ratings_df["review_month"]
            )

            ratings_df["month_label"] = (
                ratings_df["review_month"]
                .dt.strftime("%b")
            )

            # --------------------------------------------------
            # FIND SHARPEST DROP
            # --------------------------------------------------

            valid_changes = ratings_df[
                ratings_df["rating_change"].notna()
            ]

            sharpest_drop = (
                valid_changes
                .sort_values("rating_change")
                .iloc[0]
            )

            crisis_ratings = ratings_df[
                ratings_df["review_month"]
                >= pd.Timestamp("2025-06-01")
            ]

            pre_crisis_ratings = ratings_df[
                ratings_df["review_month"]
                < pd.Timestamp("2025-06-01")
            ]

            crisis_avg_rating = (
                crisis_ratings["avg_rating"].mean()
            )

            pre_crisis_avg_rating = (
                pre_crisis_ratings["avg_rating"].mean()
            )

            # --------------------------------------------------
            # KPI CARDS
            # --------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Pre-Crisis Avg. Rating",
                    f"{pre_crisis_avg_rating:.2f}"
                )

            with col2:

                st.metric(
                    "Crisis Avg. Rating",
                    f"{crisis_avg_rating:.2f}",
                    delta=(
                        f"{crisis_avg_rating - pre_crisis_avg_rating:.2f}"
                    ),
                    delta_color="inverse"
                )

            with col3:

                st.metric(
                    "Sharpest Monthly Drop",
                    f"{abs(float(sharpest_drop['rating_change'])):.2f}"
                )

            # --------------------------------------------------
            # MONTHLY RATING TREND
            # --------------------------------------------------

            st.subheader(
                "Monthly Average Rating"
            )

            rating_fig = px.line(
                ratings_df,
                x="month_label",
                y="avg_rating",
                markers=True,
                text="avg_rating",
                labels={
                    "month_label": "Month",
                    "avg_rating": "Average Rating"
                }
            )

            rating_fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="top center",
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Average Rating: %{y:.2f}"
                    "<extra></extra>"
                )
            )

            rating_fig.update_layout(
                height=450,
                yaxis=dict(
                    title="Average Rating",
                    range=[0, 5]
                ),
                xaxis=dict(
                    title=""
                ),
                margin=dict(
                    t=50,
                    b=40,
                    l=60,
                    r=30
                )
            )

            # Crisis start marker

            rating_fig.add_vline(
                x=4.5,
                line_dash="dash",
                annotation_text="Crisis Begins",
                annotation_position="top"
            )

            st.plotly_chart(
                rating_fig,
                width="stretch"
            )

            # --------------------------------------------------
            # MONTH-TO-MONTH CHANGE
            # --------------------------------------------------

            st.subheader(
                "Month-to-Month Rating Change"
            )

            change_fig = px.bar(
                ratings_df.dropna(
                    subset=["rating_change"]
                ),
                x="month_label",
                y="rating_change",
                text="rating_change",
                labels={
                    "month_label": "Month",
                    "rating_change":
                        "Rating Change vs Previous Month"
                }
            )

            change_fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Rating Change: %{y:+.2f}"
                    "<extra></extra>"
                )
            )

            change_fig.update_layout(
                height=400,
                yaxis=dict(
                    title="Rating Change",
                    zeroline=True
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
                change_fig,
                width="stretch"
            )

            # --------------------------------------------------
            # KEY FINDING
            # --------------------------------------------------

            st.subheader(
                "Q6 — Key Finding"
            )

            sharpest_month = (
                pd.to_datetime(
                    sharpest_drop["review_month"]
                ).strftime("%B")
            )

            st.write(
                f"""
                Customer ratings experienced their sharpest decline in
                **{sharpest_month}**, falling by
                **{abs(float(sharpest_drop['rating_change'])):.2f} points**
                compared with the previous month.

                Average ratings declined from
                **{pre_crisis_avg_rating:.2f}**
                during the pre-crisis period to
                **{crisis_avg_rating:.2f}**
                during the crisis.

                The most significant deterioration occurred immediately
                after the crisis began, with the monthly average rating
                falling from **4.49 in May to 2.63 in June**.
                """
            )