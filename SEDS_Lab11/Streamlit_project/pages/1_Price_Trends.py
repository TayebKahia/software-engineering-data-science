import streamlit as st
import plotly.express as px
import pandas as pd
from utils import fetch_bitcoin_data

# Set the page configuration
st.set_page_config(
    page_title="Bitcoin Price Trends",
    page_icon="\U0001F4C8",
    layout="wide",  # Expanded layout for a more spacious feel
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #ff6f61;
        text-align: center;
    }
    .sub-title {
        font-size: 20px;
        color: #4a4a4a;
        text-align: center;
    }
    .metric-card {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .plotly-chart {
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Get the date range from session state
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")

# Page Header
st.markdown('<p class="main-title">Bitcoin Price Trends</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Analyze the price movements of Bitcoin over the selected date range</p>', unsafe_allow_html=True)

# Check if the date range exists
if start_date and end_date:
    bitcoin_data = fetch_bitcoin_data(start_date, end_date)

    if not bitcoin_data.empty:
        # Create Metric Cards for statistics
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_price = bitcoin_data["Price"].mean()
        max_price = bitcoin_data["Price"].max()
        min_price = bitcoin_data["Price"].min()
        st.metric(label="Average Price", value=f"${avg_price:,.2f}", delta=f"{(max_price - min_price):,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Dropdown for choosing the chart type (line, bar, volume)
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Price Line Chart", "Price Bar Chart", "Volume Bar Chart", "Price & Market Cap"],
            help="Choose the type of chart to visualize Bitcoin price trends."
        )

        # Plot different types of charts based on the selection
        if chart_type == "Price Line Chart":
            fig = px.line(bitcoin_data, x="Date", y="Price", title="Bitcoin Price Trend")
            fig.update_traces(line=dict(color="#ff6f61", width=2))
            fig.update_layout(title="Bitcoin Price Trend", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Price Bar Chart":
            fig = px.bar(bitcoin_data, x="Date", y="Price", title="Bitcoin Price Trend (Bar Chart)")
            fig.update_layout(title="Bitcoin Price Trend (Bar Chart)", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Volume Bar Chart":
            fig = px.bar(bitcoin_data, x="Date", y="Total Volume", title="Bitcoin Trading Volume")
            fig.update_layout(title="Bitcoin Trading Volume", xaxis_title="Date", yaxis_title="Volume")
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Price & Market Cap":
            fig = px.line(bitcoin_data, x="Date", y=["Price", "Market Cap"], title="Price & Market Cap Trend")
            fig.update_layout(title="Price & Market Cap Trend", xaxis_title="Date", yaxis_title="USD")
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No data available for the selected date range.")
else:
    st.warning("Please select a date range on the Home page.")
