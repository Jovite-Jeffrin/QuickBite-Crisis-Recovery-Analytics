import streamlit as st


def show():

    # ==================================================
    # PAGE HEADER
    # ==================================================

    st.title(
        "Insights & Recommendations"
    )

    st.write(
        """
        Business interpretation of QuickBite's crisis impact,
        translating the analytical findings into actionable
        management priorities.
        """
    )

    # ==================================================
    # CRISIS DIAGNOSIS
    # ==================================================

    st.header(
        "Crisis Diagnosis"
    )

    st.write(
        """
        The analysis indicates that QuickBite's crisis created a
        broad deterioration across customer experience, operational
        performance, and business outcomes.
        """
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Customer Demand",
            "Declined"
        )

    with col2:

        st.metric(
            "Cancellations",
            "Increased"
        )

    with col3:

        st.metric(
            "Delivery Delays",
            "Increased"
        )

    with col4:

        st.metric(
            "Customer Ratings",
            "Declined"
        )

    with col5:

        st.metric(
            "Revenue",
            "Declined"
        )

    # ==================================================
    # CRISIS IMPACT SNAPSHOT
    # ==================================================

    st.divider()

    st.header(
        "Crisis Impact Snapshot"
    )

    impact_df = {
        "Metric": [
            "Cancellation Rate",
            "Average Delivery Variance",
            "SLA Compliance",
            "Average Rating"
        ],

        "Pre-Crisis": [
            "6.06%",
            "2.02 min",
            "43.61%",
            "4.58"
        ],

        "Crisis": [
            "11.93%",
            "17.60 min",
            "12.29%",
            "2.31"
        ],

        "Business Interpretation": [
            "Customer/order reliability deteriorated",
            "Actual delivery time moved substantially above expectation",
            "On-time service performance deteriorated sharply",
            "Customer satisfaction experienced a major decline"
        ]
    }

    st.dataframe(
        impact_df,
        hide_index=True,
        width="stretch"
    )

    # ==================================================
    # KEY FINDINGS
    # ==================================================

    st.divider()

    st.header(
        "Key Findings"
    )

    # --------------------------------------------------
    # FINDING 1
    # --------------------------------------------------

    st.subheader(
        "1. Customer and Order Reliability Deteriorated"
    )

    st.write(
        """
        The cancellation rate increased from **6.06% before the
        crisis to 11.93% during the crisis**. This represents an
        increase of **5.87 percentage points**, indicating a
        significant deterioration in order reliability.
        """
    )

    # --------------------------------------------------
    # FINDING 2
    # --------------------------------------------------

    st.subheader(
        "2. Delivery Operations Were Severely Disrupted"
    )

    st.write(
        """
        Average delivery variance increased from **2.02 minutes to
        17.60 minutes**. At the same time, SLA compliance declined
        from **43.61% to 12.29%**.

        This indicates that delivery performance became one of the
        most significant operational problems during the crisis.
        """
    )

    # --------------------------------------------------
    # FINDING 3
    # --------------------------------------------------

    st.subheader(
        "3. Customer Satisfaction Declined Sharply"
    )

    st.write(
        """
        Average customer rating declined substantially during the
        crisis, falling from **4.58 in January to 2.31 by September**.

        The sustained deterioration suggests that the crisis had a
        prolonged effect on customer experience rather than being
        limited to a single short-term disruption.
        """
    )

    # --------------------------------------------------
    # FINDING 4
    # --------------------------------------------------

    st.subheader(
        "4. High-Value Customers Require Particular Attention"
    )

    st.write(
        """
        The high-value customer analysis identifies customers in the
        top 5% of pre-crisis spending whose order frequency and
        ratings deteriorated during the crisis.

        These customers represent an important recovery opportunity
        because losing previously high-value customers can have a
        disproportionate impact on long-term revenue.
        """
    )

    # ==================================================
    # RECOMMENDATIONS
    # ==================================================

    st.divider()

    st.header(
        "Recommended Actions"
    )

    # --------------------------------------------------
    # PRIORITY 1
    # --------------------------------------------------

    st.subheader(
        "Priority 1 — Stabilize Delivery Operations"
    )

    st.write(
        """
        **Why:** Delivery variance increased from 2.02 to 17.60
        minutes and SLA compliance fell to 12.29%.

        **Action:**

        - Identify cities and time periods with the highest delivery
          delays.
        - Increase delivery capacity in high-delay areas.
        - Monitor actual versus expected delivery time continuously.
        - Introduce operational alerts when SLA performance
          deteriorates.
        - Review delivery-partner allocation and utilization.
        """
    )

    # --------------------------------------------------
    # PRIORITY 2
    # --------------------------------------------------

    st.subheader(
        "Priority 2 — Reduce Order Cancellations"
    )

    st.write(
        """
        **Why:** Cancellation rate almost doubled from 6.06% to
        11.93%.

        **Action:**

        - Identify restaurants and cities with unusually high
          cancellation rates.
        - Separate restaurant-driven cancellations from
          delivery-driven cancellations where possible.
        - Monitor cancellation rates by operating period.
        - Prioritize intervention for locations showing the largest
          deterioration.
        """
    )

    # --------------------------------------------------
    # PRIORITY 3
    # --------------------------------------------------

    st.subheader(
        "Priority 3 — Rebuild Customer Trust"
    )

    st.write(
        """
        **Why:** Customer ratings deteriorated substantially during
        the crisis.

        **Action:**

        - Conduct restaurant-level food quality and safety audits.
        - Investigate recurring negative customer feedback.
        - Establish stronger restaurant quality monitoring.
        - Track customer sentiment after corrective actions.
        - Communicate visible improvements to customers.
        """
    )

    # --------------------------------------------------
    # PRIORITY 4
    # --------------------------------------------------

    st.subheader(
        "Priority 4 — Recover High-Value Customers"
    )

    st.write(
        """
        **Why:** The high-value customer analysis identifies
        previously loyal customers whose ordering behavior
        deteriorated during the crisis.

        **Action:**

        - Build a targeted win-back program for high-value customers.
        - Use personalized offers rather than broad discounting.
        - Prioritize customers with significant order-frequency
          declines.
        - Monitor repeat-order recovery after intervention.
        """
    )

    # --------------------------------------------------
    # PRIORITY 5
    # --------------------------------------------------

    st.subheader(
        "Priority 5 — Protect Revenue During Recovery"
    )

    st.write(
        """
        **Why:** Revenue deterioration occurred alongside declining
        order volume.

        **Action:**

        - Focus incentives on high-value and recoverable customers.
        - Avoid excessive blanket discounts.
        - Measure incremental orders generated by each promotion.
        - Track revenue recovery against the pre-crisis baseline.
        """
    )

    # ==================================================
    # PRIORITY MATRIX
    # ==================================================

    st.divider()

    st.header(
        "Management Priority Matrix"
    )

    priority_df = {
        "Priority": [
            "Delivery Operations",
            "Cancellation Reduction",
            "Customer Trust",
            "High-Value Customer Recovery",
            "Revenue Recovery"
        ],

        "Impact": [
            "Very High",
            "Very High",
            "Very High",
            "High",
            "High"
        ],

        "Urgency": [
            "Immediate",
            "Immediate",
            "Immediate",
            "30 Days",
            "30–90 Days"
        ],

        "Primary KPI": [
            "SLA Compliance",
            "Cancellation Rate",
            "Average Rating",
            "Repeat Order Rate",
            "Revenue"
        ]
    }

    st.dataframe(
        priority_df,
        hide_index=True,
        width="stretch"
    )

    # ==================================================
    # 30 / 60 / 90 DAY ACTION PLAN
    # ==================================================

    st.divider()

    st.header(
        "30–60–90 Day Recovery Plan"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader(
            "First 30 Days"
        )

        st.write(
            """
            **Stabilize**

            - Address major delivery bottlenecks
            - Identify high-cancellation locations
            - Begin restaurant quality audits
            - Identify high-value customers at risk
            """
        )

    with col2:

        st.subheader(
            "Days 31–60"
        )

        st.write(
            """
            **Recover**

            - Launch targeted customer win-back campaigns
            - Improve delivery-partner allocation
            - Implement restaurant corrective actions
            - Monitor rating and cancellation recovery
            """
        )

    with col3:

        st.subheader(
            "Days 61–90"
        )

        st.write(
            """
            **Optimize**

            - Measure recovery against the pre-crisis baseline
            - Optimize customer incentives
            - Review restaurant performance
            - Scale successful operational interventions
            """
        )

    # ==================================================
    # SUCCESS METRICS
    # ==================================================

    st.divider()

    st.header(
        "Recovery Success Metrics"
    )

    success_df = {
        "Area": [
            "Customer",
            "Operations",
            "Quality",
            "Revenue"
        ],

        "Primary KPI": [
            "Repeat Order Rate",
            "SLA Compliance",
            "Average Rating",
            "Revenue"
        ],

        "Desired Direction": [
            "Increase",
            "Increase",
            "Increase",
            "Increase"
        ]
    }

    st.dataframe(
        success_df,
        hide_index=True,
        width="stretch"
    )

    # ==================================================
    # FINAL EXECUTIVE MESSAGE
    # ==================================================

    st.divider()

    st.header(
        "Executive Recommendation"
    )

    st.info(
        """
        QuickBite's recovery should prioritize **operational
        stabilization before aggressive customer acquisition**.

        The analysis indicates that delivery reliability,
        cancellations, and customer experience deteriorated
        simultaneously. Restoring service quality and rebuilding
        customer trust should therefore be the immediate priority.

        Once operational performance stabilizes, QuickBite can focus
        on recovering high-value customers and rebuilding revenue
        through targeted rather than broad-based incentives.
        """
    )