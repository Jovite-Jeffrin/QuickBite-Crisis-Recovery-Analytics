import streamlit as st


def show():
    """
    Render the Business Overview page.
    """

    # --------------------------------------------------
    # Header
    # --------------------------------------------------
    st.title("Business Overview")
    st.subheader("Understanding the business context behind the analysis")

    # --------------------------------------------------
    # About QuickBite
    # --------------------------------------------------
    st.header("About QuickBite")

    st.write(
        """
        QuickBite is a fictional online food delivery platform operating across
        multiple cities. The company connects customers, restaurants, and
        delivery partners through a digital platform, enabling fast and
        convenient food delivery services.
        """
    )

    st.divider()

    # --------------------------------------------------
    # Business Scenario
    # --------------------------------------------------
    st.header("Business Scenario")

    st.write(
        """
        In June 2025, QuickBite experienced a major food safety incident that
        significantly impacted customer trust and overall business performance.

        Following the crisis, management sought to understand its operational,
        financial, and customer-related impact to develop effective recovery
        strategies. This project analyzes business performance before, during,
        and after the crisis using data-driven insights.
        """
    )

    st.divider()

    # --------------------------------------------------
    # Crisis Timeline
    # --------------------------------------------------
    st.header("Crisis Timeline")

    st.markdown(
        """
        **Pre-Crisis**
        - January 2025 – May 2025

        **Crisis Period**
        - June 2025 – September 2025

        **Post-Crisis**
        - October 2025 onwards
        """
    )

    st.divider()

    # --------------------------------------------------
    # Business Impact
    # --------------------------------------------------
    st.header("Business Impact")

    st.markdown(
        """
        The crisis had a significant impact across multiple business areas:

        - Decline in customer orders
        - Increase in order cancellations
        - Drop in customer ratings
        - Negative customer sentiment
        - Revenue decline
        - Customer churn
        - Operational inefficiencies
        """
    )

    st.divider()

    # --------------------------------------------------
    # Key Business Questions
    # --------------------------------------------------
    st.header("Key Business Questions")

    st.markdown(
        """
        This project aims to answer the following questions:

        - How did order volumes change during the crisis?
        - Which cities and restaurants were affected the most?
        - Did delivery performance deteriorate?
        - How did customer ratings and sentiment evolve?
        - What was the financial impact of the crisis?
        - Which high-value customers stopped ordering?
        - What recovery strategies should the business prioritize?
        """
    )

    st.divider()

    # --------------------------------------------------
    # Closing Note
    # --------------------------------------------------
    st.info(
        "Continue to the Executive Dashboard to explore the key performance "
        "indicators and understand the overall impact of the crisis."
    )