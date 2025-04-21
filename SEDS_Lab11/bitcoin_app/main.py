import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Product Sales Exploration & ML Testing",
    page_icon="📊",  # Add an emoji icon for better appeal
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

# Home Page Content
st.markdown(
    """
    <div class="card">
        <h3>Welcome to the Product Sales Analysis Dashboard!</h3>
        <p>
            This application is designed to help you explore sales data for TechBazaar Headphones and test 
            pre-trained machine learning models. Here’s what you can do:
        </p>
        <ul>
            <li><strong>Database Exploration:</strong> Upload and analyze sales data to uncover key insights.</li>
            <li><strong>Visualizations:</strong> Generate scatter plots and time series charts to identify trends.</li>
            <li><strong>Model Testing:</strong> Test pre-trained regression models to predict sales based on input features.</li>
        </ul>
        <p>Use the navigation menu on the left to get started!</p>
    </div>
    """,
    unsafe_allow_html=True,
)
