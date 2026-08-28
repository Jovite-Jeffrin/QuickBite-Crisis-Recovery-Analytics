import streamlit as st


def show():

    # ==================================================
    # HERO SECTION
    # ==================================================

    st.title(
        "QuickBite Crisis Analysis"
    )

    st.subheader(
        "Diagnosing the Business Impact of a Major Crisis"
    )

    st.write(
        """
        A data-driven investigation into how the QuickBite crisis
        affected customer behavior, operational performance,
        customer experience, and business outcomes.
        """
    )

    st.divider()

    # ==================================================
    # CRISIS AT A GLANCE
    # ==================================================

    st.header(
        "The Crisis at a Glance"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Cancellation Rate",
            "11.93%",
            "6.06% → 11.93%",
            delta_color="inverse"
        )

    with col2:

        st.metric(
            "Delivery Variance",
            "17.60 min",
            "2.02 → 17.60 min",
            delta_color="inverse"
        )

    with col3:

        st.metric(
            "SLA Compliance",
            "12.29%",
            "43.61% → 12.29%",
            delta_color="inverse"
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Customer Rating",
            "2.31",
            "4.58 → 2.31",
            delta_color="inverse"
        )

    with col2:

        st.metric(
            "Crisis Period",
            "Jun–Sep 2025"
        )

    with col3:

        st.metric(
            "Pre-Crisis Baseline",
            "Jan–May 2025"
        )

    # ==================================================
    # BUSINESS PROBLEM
    # ==================================================

    st.divider()

    st.header(
        "The Business Problem"
    )

    st.write(
        """
        QuickBite experienced a significant deterioration in
        operational performance and customer experience during the
        crisis period.

        This project investigates the impact across the complete
        business journey — from order placement and delivery
        performance to customer satisfaction, loyalty, and revenue.
        """
    )

    # ==================================================
    # ANALYTICAL FRAMEWORK
    # ==================================================

    st.header(
        "What This Analysis Answers"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Customer Impact"
        )

        st.write(
            """
            How did customer behavior, satisfaction, ratings,
            and loyalty change during the crisis?
            """
        )

        st.subheader(
            "Operational Impact"
        )

        st.write(
            """
            How did cancellations, delivery delays, and SLA
            performance change across the crisis?
            """
        )

    with col2:

        st.subheader(
            "Financial Impact"
        )

        st.write(
            """
            How did the crisis affect order volume, revenue,
            and customer spending?
            """
        )

        st.subheader(
            "Business Recovery"
        )

        st.write(
            """
            Which areas should management prioritize to stabilize
            operations and recover customers and revenue?
            """
        )

    # ==================================================
    # KEY FINDINGS
    # ==================================================

    st.divider()

    st.header(
        "Key Findings"
    )

    findings = [
        (
            "Customer Reliability",
            "Cancellation rates nearly doubled during the crisis."
        ),

        (
            "Delivery Performance",
            "Delivery variance increased dramatically, while SLA compliance deteriorated."
        ),

        (
            "Customer Experience",
            "Average customer ratings declined sharply during the crisis."
        ),

        (
            "Customer Loyalty",
            "Previously high-value customers showed meaningful deterioration in ordering behavior."
        ),

        (
            "Business Recovery",
            "Operational stabilization should precede aggressive customer acquisition."
        )
    ]

    for title, description in findings:

        st.markdown(
            f"**{title}** — {description}"
        )

    # ==================================================
    # EXPLORE THE ANALYSIS
    # ==================================================

    st.divider()

    st.header(
        "Explore the Analysis"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Business Overview"
        )

        st.write(
            "Understand the overall business context and crisis timeline."
        )

        st.subheader(
            "Executive Dashboard"
        )

        st.write(
            "View the most important business and operational KPIs in one place."
        )

    with col2:

        st.subheader(
            "Order Analysis"
        )

        st.write(
            "Explore order behavior, cancellations, revenue, and customer-level impacts."
        )

        st.subheader(
            "Insights & Recommendations"
        )

        st.write(
            "Translate the analysis into management priorities and a recovery plan."
        )

    # ==================================================
    # ANALYTICAL APPROACH
    # ==================================================

    st.divider()

    st.header(
        "Analytical Approach"
    )

    st.write(
        """
        The analysis compares QuickBite's performance across two
        clearly defined periods:

        **Pre-Crisis:** January–May 2025

        **Crisis:** June–September 2025

        The comparison covers customer behavior, order performance,
        cancellations, delivery operations, customer ratings,
        revenue, and high-value customer behavior.
        """
    )

    # ==================================================
    # TECHNOLOGY
    # ==================================================

    st.divider()

    st.header(
        "Technology Stack"
    )

    st.write(
        """
        **PostgreSQL** · **SQL** · **Python** · **Pandas** ·
        **Plotly** · **Streamlit**
        """
    )

    # ==================================================
    # FINAL MESSAGE
    # ==================================================

    st.divider()

    st.info(
        """
        The objective of this project is not only to quantify the
        crisis impact, but to identify the operational and customer
        priorities required for recovery.
        """
    )