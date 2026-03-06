import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor

from database.db import get_products, get_sales_history


# --- ML Performance Upgrade: Caching ---
# Training a Random Forest is expensive. We cache this so it only trains once a day.
@st.cache_data(ttl=86400)
def _train_demand_model():
    """
    Trains the regressor using real historical sales data.
    """
    products = get_products()
    sales = get_sales_history()

    # 1. Feature Engineering: Get REAL historical demand (total units sold per product)
    historical_demand = sales.groupby('product_id')['units_sold'].sum().reset_index()

    # 2. Merge to create our master training dataset
    df = products.merge(historical_demand, left_on='id', right_on='product_id', how='left')
    df['units_sold'] = df['units_sold'].fillna(0)  # Fill items with 0 sales

    # 3. Define Features (X) and Target (y)
    # Using behavioral drivers (price, rating) instead of inventory levels
    X = df[["price", "rating"]].values
    y = df["units_sold"].values

    # 4. Train the Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model, df


def get_demand_forecast() -> pd.DataFrame:
    """
    Generates a dataframe perfectly formatted for the Manager Dashboard's column_config.
    """
    try:
        model, df = _train_demand_model()

        # Predict future demand based on current price and rating
        X_current = df[["price", "rating"]].values
        predictions = model.predict(X_current)

        # Build the exact dataframe the Manager Dashboard expects
        forecast_df = df[["name", "stock", "reorder_point", "lead_time_days"]].copy()

        # Add the ML predictions
        forecast_df["predicted_30d_demand"] = np.round(predictions).astype(int)

        # Smart Business Logic: Link action to the reorder point
        forecast_df["action"] = forecast_df.apply(
            lambda x: "⚠️ Order Now" if x["stock"] <= x["reorder_point"] else "✅ Optimal",
            axis=1
        )

        return forecast_df

    except Exception as e:
        # Professional fallback so the manager dashboard doesn't crash if the DB is empty
        print(f"Demand Forecasting Error: {e}")
        return pd.DataFrame()
