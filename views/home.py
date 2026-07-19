import streamlit as st


def show():
    """
    Render the Home page.
    """

    # --------------------------------------------------
    # Header
    # --------------------------------------------------
    st.title("QuickBite Express")
    st.subheader("Crisis Recovery Analytics Platform")

    # --------------------------------------------------
    # Welcome
    # --------------------------------------------------
    st.write(
        """
        Welcome to the **QuickBite Crisis Recovery Analytics Platform**.

        This application analyzes the operational and financial impact of the
        2025 food safety crisis using PostgreSQL, Python, and Streamlit.

        The objective is to identify key business challenges, evaluate customer
        behavior, measure operational performance, and provide data-driven
        recommendations for business recovery.
        """
    )

    st.divider()

    # --------------------------------------------------
    # Crisis Summary
    # --------------------------------------------------
    st.header("Crisis Summary")

    st.write(
        """
        In June 2025, QuickBite experienced a major food safety incident that
        significantly affected customer trust and overall business performance.

        The crisis resulted in declining order volumes, increasing cancellations,
        lower customer ratings, delivery disruptions, and revenue loss across
        multiple cities.

        This analytics platform investigates the impact of the crisis across
        customers, restaurants, delivery operations, and financial performance,
        helping stakeholders make informed recovery decisions.
        """
    )

    st.divider()

    # --------------------------------------------------
    # Project Objectives
    # --------------------------------------------------
    st.header("Project Objectives")

    st.markdown(
        """
        - Analyze order trends before, during, and after the crisis.
        - Evaluate customer behavior and retention.
        - Measure delivery performance and SLA compliance.
        - Assess customer feedback and sentiment.
        - Quantify the financial impact of the crisis.
        - Recommend data-driven recovery strategies.
        """
    )

    st.divider()

    # --------------------------------------------------
    # Technology Stack
    # --------------------------------------------------
    st.header("Technology Stack")

    st.markdown(
        """
        - **Database:** PostgreSQL
        - **Programming Language:** Python
        - **Framework:** Streamlit
        - **Data Analysis:** Pandas, NumPy
        - **Visualization:** Plotly
        - **Version Control:** Git & GitHub
        """
    )

    st.divider()

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    st.caption(
        "Developed by Jeffrin A | Data Analytics Portfolio Project"
    )