from datetime import datetime, timedelta
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st


# --- Initializing Data ---
# In a real-world scenario, these would be loaded from a CSV, SQL, or NoSQL database.


def _initialize_product_data() -> pd.DataFrame:
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "name": [
            "Wireless Mouse", "Running Shoes", "Coffee Maker", "Yoga Mat", "Laptop Stand", "Bluetooth Headphones",
            "Smartwatch", "LED Desk Lamp", "Insulated Water Bottle", "Mechanical Keyboard", "Adjustable Dumbbells",
            "Travel Backpack"
        ],
        "category": [
            "Electronics", "Sports", "Home", "Fitness", "Electronics", "Electronics",
            "Electronics", "Home", "Sports", "Electronics", "Fitness", "Sports"
        ],
        "price": [
            25.0, 70.0, 120.0, 30.0, 40.0, 90.0,
            199.99, 45.0, 25.0, 130.0, 150.0, 85.0
        ],
        "cost": [
            10.0, 35.0, 60.0, 10.0, 15.0, 40.0,
            90.0, 15.0, 8.0, 65.0, 80.0, 30.0
        ],
        "stock": [
            50, 15, 8, 40, 25, 12,
            30, 60, 100, 20, 10, 45
        ],
        "reorder_point": [
            20, 10, 5, 15, 10, 8,
            10, 15, 25, 5, 3, 12
        ],
        "lead_time_days": [
            5, 14, 21, 7, 10, 15,
            14, 7, 5, 20, 30, 10
        ],
        "rating": [
            4.5, 4.2, 4.8, 4.0, 4.6, 4.9,
            4.7, 4.3, 4.8, 4.9, 4.6, 4.5
        ],
        "description": [
            "Ergonomic wireless mouse with precision tracking.",
            "Comfortable running shoes with breathable mesh.",
            "Automatic drip coffee machine with timer.",
            "Eco-friendly non-slip yoga mat.",
            "Adjustable ergonomic aluminum laptop stand.",
            "Over-ear active noise cancelling headphones.",
            "Fitness tracking smartwatch with heart rate and sleep monitor.",
            "Dimmable LED desk lamp with built-in USB charging port.",
            "32oz stainless steel double-wall vacuum insulated bottle.",
            "Tenkeyless mechanical keyboard with customizable RGB backlighting.",
            "Space-saving adjustable dumbbell set, up to 50 lbs per weight.",
            "Water-resistant travel backpack with padded laptop compartment."
        ],
        "image": [
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&q=80",  # Mouse
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80",  # Shoes
            "https://images.unsplash.com/photo-1608354580875-30bd4168b351?q=80&w=687",  # Coffee Maker
            "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=600&q=80",  # Yoga Mat
            "https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?w=600&q=80",  # Laptop Stand
            "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&q=80",  # Headphones
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80",  # Smartwatch
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&q=80",  # Desk Lamp
            "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&q=80",  # Water Bottle
            "https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&q=80",  # Keyboard
            "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&q=80",  # Dumbbells
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&q=80"  # Backpack
        ]
    })


def _initialize_sales_data() -> pd.DataFrame:
    """Generates 30 days of synthetic transaction-level sales data for the ML model."""
    np.random.seed(42)  # Seeded so your demo data stays consistent across reloads
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    sales_records = []
    # Generate 100 random sales transactions
    for _ in range(100):
        sales_records.append({
            "date": np.random.choice(dates),
            "product_id": np.random.randint(1, 7),
            "units_sold": np.random.randint(1, 5)
        })

    return pd.DataFrame(sales_records)


def _initialize_user_data() -> pd.DataFrame:
    return pd.DataFrame({
        "name": ["System Admin", "Store Manager", "Jane Doe"],  # Added: For personalized UI greetings
        "email": ["admin@test.com", "manager@test.com", "user@test.com"],
        "password": ["admin123", "manager123", "user123"],  # In production, use hashed passwords!
        "role": ["admin", "manager", "customer"]
    })


# --- Data Access Functions ---

def get_products():
    """Fetches the product database from session state, or initializes it."""
    if 'product_db' not in st.session_state:
        st.session_state.product_db = _initialize_product_data()
    return st.session_state.product_db


def get_sales_history() -> pd.DataFrame:
    """Returns historical transaction-level sales data for analytics and ML."""
    return _initialize_sales_data()


def get_users() -> pd.DataFrame:
    """Returns user credentials and roles."""
    return _initialize_user_data()


def get_user_by_email(email: str) -> Dict:
    """Helper to fetch a specific user's details."""
    users = get_users()
    user = users[users['email'] == email]
    return user.to_dict('records')[0] if not user.empty else None


# -------------

def add_user(name, email, password):
    """Adds a new customer to the database."""
    # In a real app, you'd do: cursor.execute("INSERT INTO users...")
    # For our demo, we update the session-stored dataframe
    if 'user_db' not in st.session_state:
        st.session_state.user_db = _initialize_user_data()

    new_user = pd.DataFrame([{
        "name": name,
        "email": email,
        "password": password,
        "role": "customer"
    }])

    st.session_state.user_db = pd.concat([st.session_state.user_db, new_user], ignore_index=True)


def add_product(name, category, price, cost, stock, reorder, lead_time, rating, desc, image):
    """Appends a new product to the session state database."""
    db = get_products()

    # Generate a new unique ID
    new_id = db['id'].max() + 1 if not db.empty else 1

    new_item = pd.DataFrame([{
        "id": new_id,
        "name": name,
        "category": category,
        "price": float(price),
        "cost": float(cost),
        "stock": int(stock),
        "reorder_point": int(reorder),
        "lead_time_days": int(lead_time),
        "rating": float(rating),
        "description": desc,
        "image": image
    }])

    st.session_state.product_db = pd.concat([db, new_item], ignore_index=True)


def update_user_role(email, new_role):
    """Updates the role of a specific user in the database."""
    if 'user_db' in st.session_state:
        db = st.session_state.user_db
        # Find the user by email and update their role
        db.loc[db['email'] == email, 'role'] = new_role
        st.session_state.user_db = db
