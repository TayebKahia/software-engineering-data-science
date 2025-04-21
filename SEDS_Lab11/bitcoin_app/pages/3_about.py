import streamlit as st


# Set the page configuration
st.set_page_config(
    page_title="About This Dashboard",
    page_icon="\U0001F4D6",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.write("""
### Overview
This Bitcoin Price Analysis Dashboard is a tool to visualize, analyze, and predict Bitcoin price trends. 
It leverages historical data from **CoinGecko** and applies **machine learning** techniques to forecast future trends.

The application is designed with three main objectives:
- Provide **interactive visualizations** of Bitcoin price trends.
- Offer **statistical insights** into the dataset.
- Demonstrate the use of **machine learning models** for predictive analysis.

### Features
1. **Price Trends:** View historical price changes with interactive line charts.
2. **Statistics:** Analyze descriptive statistics and correlations in the dataset.
3. **Machine Learning:** Predict Bitcoin prices using a simple linear regression model.

### About the Author
This dashboard was created as part of the "Software Engineering for Data Science" course. If you have any feedback or suggestions, feel free to get in touch using the links below.

### Resources
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)
- [Streamlit Documentation](https://docs.streamlit.io/)

### Contact
- **Email:** example@example.com
- **GitHub:** [github.com/example](https://github.com/example)
- **Course Link:** [Software Engineering for Data Science](https://elearn.esi-sba.dz/course/index.php?categoryid=30)

Thank you for using this dashboard!
""")
