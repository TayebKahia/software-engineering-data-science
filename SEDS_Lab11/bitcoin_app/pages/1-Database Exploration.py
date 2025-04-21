import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set the page configuration
st.set_page_config(
    page_title="Product Sales Exploration & ML Testing",
    page_icon="📊",
    layout="wide",
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
        margin-bottom: 40px;
    }
    .card {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.header("Navigation Menu")
st.sidebar.subheader("TechBazaar Sales Analysis")
st.sidebar.write("Navigate through the app using the options above:")

# Header Section
st.markdown(
    '<p class="title">Product Sales Analysis Dashboard</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="description">An interactive app for exploring sales data and testing pre-trained regression models.</p>',
    unsafe_allow_html=True,
)

# Database Exploration Section
st.markdown(
    """
    <div class="card">
        <h3>Database Exploration</h3>
        <p>Upload and explore the product sales dataset. Visualize the relationships and trends in the data.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# File uploader for the dataset
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Display a preview of the dataset
    st.markdown("### Preview of the Uploaded Dataset")
    st.dataframe(df.head())

    # Dataset description
    st.markdown("### Dataset Summary")
    st.write(df.describe())

    # Scatter plots for input features vs Sales
    st.markdown("### Scatter Plots")
    st.markdown(
        "Visualize the relationship between input features (`Product_Price`, `Marketing_Cost`) and the output feature (`Sales`)."
    )
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Product Price vs Sales")
        fig, ax = plt.subplots()
        ax.scatter(df["Product_Price"], df["Sales"], alpha=0.5)
        ax.set_xlabel("Product Price")
        ax.set_ylabel("Sales")
        st.pyplot(fig)

    with col2:
        st.markdown("#### Marketing Cost vs Sales")
        fig, ax = plt.subplots()
        ax.scatter(df["Marketing_Cost"], df["Sales"], alpha=0.5, color="orange")
        ax.set_xlabel("Marketing Cost")
        ax.set_ylabel("Sales")
        st.pyplot(fig)

    # Time series plots
    st.markdown("### Time Series Plots")
    st.markdown(
        "Visualize trends for `Product_Price`, `Marketing_Cost`, and `Sales` over time."
    )
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["Date"], df["Product_Price"], label="Product Price", color="blue")
        ax.plot(
            df["Date"], df["Marketing_Cost"], label="Marketing Cost", color="orange"
        )
        ax.plot(df["Date"], df["Sales"], label="Sales", color="green")
        ax.set_xlabel("Date")
        ax.set_ylabel("Values")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("The dataset does not contain a `Date` column.")
else:
    st.warning("Please upload a CSV file to explore the data.")
