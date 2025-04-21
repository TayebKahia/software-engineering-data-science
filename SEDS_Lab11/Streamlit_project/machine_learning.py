import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error
from utils import fetch_bitcoin_data


# Set the page configuration
st.set_page_config(
    page_title="Machine Learning Model Predictions",
    page_icon="\U0001F916",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Get the date range from session state
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")

if start_date and end_date:
    # Fetch Bitcoin data
    bitcoin_data = fetch_bitcoin_data(start_date, end_date)

    if not bitcoin_data.empty:
        # Load the saved model
        model = joblib.load('rf_model.pkl')

        # Prepare data for prediction
        for i in range(1, 6):
            bitcoin_data[f'Lagged Price {i}'] = bitcoin_data['Price'].shift(i)
        ml_data = bitcoin_data.dropna()

        X = ml_data[[f'Lagged Price {i}' for i in range(1, 6)]]
        y = ml_data['Price']

        # Make predictions using the loaded model
        predictions = model.predict(X)

        # Calculate the Mean Squared Error
        mse = mean_squared_error(y, predictions)
        st.write(f"### Model Performance")
        st.write(f"Mean Squared Error: {mse:.2f}")

        # Visualizing Actual vs Predicted Prices
        fig_ml = go.Figure()
        fig_ml.add_trace(go.Scatter(x=y, y=predictions, mode='markers', name='Predictions'))
        fig_ml.add_trace(go.Scatter(x=y, y=y, mode='lines', name='Ideal Line'))
        fig_ml.update_layout(
            title="Actual vs Predicted Prices",
            xaxis_title="Actual Price", yaxis_title="Predicted Price")
        st.plotly_chart(fig_ml, use_container_width=True)

        # Prediction Error Distribution
        error = predictions - y
        fig_error = go.Figure(go.Histogram(x=error, nbinsx=50, name='Prediction Error'))
        fig_error.update_layout(
            title="Prediction Error Distribution", xaxis_title="Error", yaxis_title="Frequency")
        st.plotly_chart(fig_error, use_container_width=True)

        # Residual Plot
        fig_residual = go.Figure(go.Scatter(x=y, y=error, mode='markers', name='Residuals'))
        fig_residual.update_layout(
            title="Residual Plot", xaxis_title="Actual Price", yaxis_title="Residuals")
        st.plotly_chart(fig_residual, use_container_width=True)

    else:
        st.warning("No data available for making predictions.")
else:
    st.warning("Please select a date range on the Home page.")
