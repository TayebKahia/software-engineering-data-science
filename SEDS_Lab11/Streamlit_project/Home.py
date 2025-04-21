import streamlit as st
import datetime
import time
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="Bitcoin Price Analysis Dashboard",
    page_icon="./bitcoin.png",  # Replace with your icon file path
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #FF6347;
        text-align: center;
    }
    .description {
        font-size: 18px;
        color: #555;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f5;
        padding: 20px;
    }
    .card {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Calculate default dates: last 10 days
today = datetime.date.today()
ten_days_ago = today - datetime.timedelta(days=10)

# Initialize session state for dates if not already set
if "start_date" not in st.session_state:
    st.session_state["start_date"] = ten_days_ago  # Set default start date

if "end_date" not in st.session_state:
    st.session_state["end_date"] = today  # Set default end date

# Sidebar and page content
st.sidebar.header("Navigate the Dashboard")
st.sidebar.subheader("Bitcoin Price Analysis")
st.sidebar.write("Use the date picker to select the range of data.")
st.sidebar.image("./bitcoin.png", use_column_width=True)  # Replace with your image path

# Page Title and Description
st.markdown(
    '<p class="title">Bitcoin Price Analysis Dashboard</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="description">Select the date range below to analyze Bitcoin price data.</p>',
    unsafe_allow_html=True,
)

# Date input for start and end dates
start_date = st.date_input("Start Date", value=st.session_state["start_date"])
end_date = st.date_input("End Date", value=st.session_state["end_date"])

# Validate the date range
if start_date and end_date:
    if start_date > end_date:
        st.error("Start Date must be before End Date.")
    else:
        # Update session state with selected dates
        st.session_state["start_date"] = start_date
        st.session_state["end_date"] = end_date
        st.success("Date range updated!")

# Check if the page is the Home page and print the URL/DataFrame only here
if st.session_state.get("start_date") and st.session_state.get("end_date"):
    from utils import fetch_bitcoin_data

    with st.spinner("Fetching Bitcoin data..."):
        bitcoin_data = fetch_bitcoin_data(start_date, end_date)

    if not bitcoin_data.empty:
        # Only print URL and DataFrame on the Home page
        st.markdown("### Fetched Data from API:")
        st.write(
            f"Fetching data from URL: https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={int(time.mktime(start_date.timetuple()))}&to={int(time.mktime(end_date.timetuple()))}"
        )

        # Show Bitcoin Data in a DataFrame
        st.write("Displaying first few rows of the Bitcoin data:")
        st.dataframe(bitcoin_data.head())

        # Additional feature: Displaying the data in a chart
        # st.line_chart(bitcoin_data['Price'])

    else:
        st.warning("No data available for the selected date range.")
else:
    st.warning("Please select both start and end dates.")
