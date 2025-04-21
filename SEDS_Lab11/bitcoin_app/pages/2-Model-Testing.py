import pickle
import numpy as np
import streamlit as st

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

# Model Testing Section
st.markdown(
    """
    <div class="card">
        <h3>Model Testing</h3>
        <p>Test pre-trained regression models by providing input data to predict product sales.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Allow users to select a model
model_choice = st.selectbox(
    "Select a Regression Model to Test:", options=["Linear Model", "Polynomial Model"]
)

# Load the selected model
if model_choice == "Linear Model":
    model_path = "./resources/linear_model.pkl"
elif model_choice == "Polynomial Model":
    model_path = "./resources/poly_model.pkl"
import os

st.write("Current Working Directory:", os.getcwd())

try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)

    # Input fields for test data
    st.markdown("### Input Data for Prediction")
    product_price = st.number_input(
        "Product Price:", min_value=0.0, value=100.0, step=10.0
    )
    marketing_cost = st.number_input(
        "Marketing Cost:", min_value=0.0, value=50.0, step=5.0
    )
    day_of_week = st.selectbox(
        "Day of the Week:",
        options=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
    )
    month = st.selectbox("Month:", options=list(range(1, 13)))
    year = st.number_input("Year:", min_value=2000, max_value=2100, value=2023, step=1)

    # Convert day_of_week to numeric value
    day_mapping = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    day_of_week_numeric = day_mapping[day_of_week]

    # Prepare the input array for prediction
    input_features = np.array(
        [[product_price, marketing_cost, day_of_week_numeric, month, year]]
    )

    # Display prediction
    if st.button("Predict Sales"):
        prediction = model.predict(input_features)
        st.success(f"Predicted Sales: {prediction[0]:.2f}")
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
