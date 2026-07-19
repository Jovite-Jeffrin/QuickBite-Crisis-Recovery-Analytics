import streamlit as st
import pandas as pd

from database import get_engine


def show():
    """
    Render the Executive Dashboard.
    """

    st.title("Executive Dashboard")
    st.subheader("Business Performance Overview")

    st.write(
        """
        This dashboard provides a high-level summary of QuickBite's
        operational and financial performance during the food safety crisis.

        The KPIs shown below will later be populated dynamically
        from the PostgreSQL database.
        """
    )

    st.divider()

    # --------------------------------------------------
    # Database Connection Check
    # --------------------------------------------------

    try:
        engine = get_engine()

        st.success("Successfully connected to PostgreSQL.")

    except Exception as e:

        st.error("Unable to connect to PostgreSQL.")

        st.exception(e)

        return

    st.divider()

    # --------------------------------------------------
    # KPI Placeholders
    # --------------------------------------------------

    st.header("Key Performance Indicators")

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            label="Total Orders",
            value="--"
        )

    with metric2:
        st.metric(
            label="Total Revenue",
            value="--"
        )

    with metric3:
        st.metric(
            label="Cancellation Rate",
            value="--"
        )

    with metric4:
        st.metric(
            label="Average Rating",
            value="--"
        )

    st.divider()

    # --------------------------------------------------
    # Dashboard Status
    # --------------------------------------------------

    st.info(
        """
        KPI calculations and interactive visualizations
        will be added in the next phase of development.
        """
    )