import streamlit as st

import views.home as home
import views.business_overview as business_overview
import views.executive_dashboard as executive_dashboard
import views.order_analysis as order_analysis
import views.customer_analysis as customer_analysis
import views.delivery_analysis as delivery_analysis
import views.feedback_analysis as feedback_analysis
import views.revenue_analysis as revenue_analysis
import views.recommendations as recommendations
import views.about as about


st.set_page_config(
    page_title="QuickBite Crisis Recovery Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

PAGES = {
    "Home": home.show,
    "Business Overview": business_overview.show,
    "Executive Dashboard": executive_dashboard.show,
    "Order Analysis": order_analysis.show
    # ,
    # "Customer Analysis": customer_analysis.show,
    # "Delivery Analysis": delivery_analysis.show,
    # "Feedback Analysis": feedback_analysis.show,
    # "Revenue Analysis": revenue_analysis.show,
    # "Recommendations": recommendations.show,
    # "About": about.show
}

st.sidebar.title("Navigation")

selected_page = st.sidebar.radio(
    "Go to",
    list(PAGES.keys())
)

PAGES[selected_page]()