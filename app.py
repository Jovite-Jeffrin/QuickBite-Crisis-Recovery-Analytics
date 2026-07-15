# import streamlit as st

# st.title("QuickBite Crisis Recovery Dashboard")

# st.write("Welcome to my first Streamlit dashboard!")

# import streamlit as st
# import pandas as pd

# from database import get_engine

# engine = get_engine()

# query = """
# SELECT COUNT(*)
# FROM fact_orders;
# """

# df = pd.read_sql(query, engine)

# st.title("QuickBite Dashboard")

# st.write(df)


import streamlit as st

st.set_page_config(
    page_title="QuickBite Crisis Analytics",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("QuickBite Express")
st.subheader("Crisis Recovery Analytics Platform")

st.write(
    """
    Welcome to the QuickBite Crisis Recovery Analytics Platform     .

    Please select a page from the sidebar to begin the analysis.
    """
)