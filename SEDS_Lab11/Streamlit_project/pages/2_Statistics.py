import streamlit as st
import plotly.express as px
import pandas as pd
from utils import fetch_bitcoin_data

# Set the page configuration
st.set_page_config(
    page_title="Descriptive Statistics",
    page_icon="\U0001F4CA",
    layout="wide",  # Expanded layout for better visual experience
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #4B9CD3;
        text-align: center;
    }
    .sub-title {
        font-size: 20px;
        color: #6E7B8A;
        text-align: center;
    }
    .stat-card {
        background-color: #f7f7f7;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
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
st.markdown('<p class="main-title">Descriptive Statistics for Bitcoin Prices</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Explore summary statistics and correlations for the selected date range</p>', unsafe_allow_html=True)

# Check if the date range exists
if start_date and end_date:
    bitcoin_data = fetch_bitcoin_data(start_date, end_date)

    if not bitcoin_data.empty:
        # Show Summary Statistics (mean, std, min, max, etc.)
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.write("### Summary Statistics")
        st.write(bitcoin_data.describe())
        st.markdown('</div>', unsafe_allow_html=True)

        # Additional Statistical Insights: Mean, Median, Standard Deviation
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.write("### Additional Insights")
        st.write(f"**Mean Price:** ${bitcoin_data['Price'].mean():,.2f}")
        st.write(f"**Median Price:** ${bitcoin_data['Price'].median():,.2f}")
        st.write(f"**Standard Deviation of Price:** ${bitcoin_data['Price'].std():,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Add a Lagged Price column and show correlation
        bitcoin_data['Lagged Price'] = bitcoin_data['Price'].shift(1)
        corr_matrix = bitcoin_data.dropna().corr()

        # Create and display the Correlation Heatmap
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        fig_corr = px.imshow(corr_matrix, title="Correlation Heatmap", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_corr, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Allow the user to download the descriptive statistics as a CSV
        csv = bitcoin_data.describe().to_csv(index=True)
        st.download_button(
            label="Download Summary Statistics",
            data=csv,
            file_name="bitcoin_summary_statistics.csv",
            mime="text/csv",
        )

    else:
        st.warning("No data available for the selected date range.")
else:
    st.warning("Please select a date range on the Home page.")
