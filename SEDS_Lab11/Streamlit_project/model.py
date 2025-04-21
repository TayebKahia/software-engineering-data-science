import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
import joblib
from utils import fetch_bitcoin_data


# Function to train the model and save it
def train_and_save_model(start_date, end_date):
    bitcoin_data = fetch_bitcoin_data(start_date, end_date)

    if not bitcoin_data.empty:
        # Add multiple lagged features
        for i in range(1, 6):
            bitcoin_data[f'Lagged Price {i}'] = bitcoin_data['Price'].shift(i)
        ml_data = bitcoin_data.dropna()

        # Features and Target
        X = ml_data[[f'Lagged Price {i}' for i in range(1, 6)]]
        y = ml_data['Price']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model - Random Forest Regressor with GridSearchCV for hyperparameter tuning
        rf_param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15, None],
            'min_samples_split': [2, 5, 10]
        }
        rf_grid_search = GridSearchCV(RandomForestRegressor(random_state=42), rf_param_grid, cv=5)
        rf_grid_search.fit(X_train, y_train)

        # Save the model using joblib
        joblib.dump(rf_grid_search.best_estimator_, 'rf_model.pkl')

        print("Model trained and saved successfully.")
        return rf_grid_search.best_estimator_
    else:
        print("No data available for training.")
        return None


# Example usage
start_date = "2024-12-06"  # replace with the actual start date
end_date = "2024-12-10"    # replace with the actual end date
train_and_save_model(start_date, end_date)
