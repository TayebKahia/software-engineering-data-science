import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go
from utils import fetch_bitcoin_data


st.set_page_config(
    page_title="Machine Learning Model",
    page_icon="\U0001F916",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Use caching to fetch Bitcoin data
@st.cache_data
def get_cached_bitcoin_data(start_date, end_date):
    return fetch_bitcoin_data(start_date, end_date)

# Cache the model training and predictions
@st.cache_resource
def train_model_and_predict(X_train, y_train, X_test):
    # Initialize the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    return model, predictions

# Get the date range from session state
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")

if start_date and end_date:
    # Fetch Bitcoin data with caching
    bitcoin_data = get_cached_bitcoin_data(start_date, end_date)

    if not bitcoin_data.empty:
        bitcoin_data['Lagged Price'] = bitcoin_data['Price'].shift(1)
        ml_data = bitcoin_data.dropna()

        # Features and labels
        X = ml_data[['Lagged Price']]
        y = ml_data['Price']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model and make predictions with caching
        model, predictions = train_model_and_predict(X_train, y_train, X_test)

        # Calculate Mean Squared Error
        mse = mean_squared_error(y_test, predictions)
        st.write("### Model Performance")
        st.write(f"Mean Squared Error: {mse:.2f}")

        # Plot Actual vs Predicted Prices
        fig_ml = go.Figure()
        fig_ml.add_trace(go.Scatter(x=y_test, y=predictions, mode='markers', name='Predictions'))
        fig_ml.add_trace(go.Scatter(x=y_test, y=y_test, mode='lines', name='Ideal Line'))
        fig_ml.update_layout(title="Actual vs Predicted Prices",
                             xaxis_title="Actual Price", yaxis_title="Predicted Price")
        st.plotly_chart(fig_ml, use_container_width=True)

    else:
        st.warning("No data available for machine learning.")
else:
    st.warning("Please select a date range on the Home page.")
