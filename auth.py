import streamlit as st
from database.db import get_users, add_user


def init_session():
    """Ensures all required session keys exist."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "page" not in st.session_state:
        st.session_state.page = "store"  # Default to store now!
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "viewed_products" not in st.session_state:
        st.session_state.viewed_products = []


def login(email, password):
    """Validates credentials and sets up the user session."""
    users = get_users()
    email = email.strip().lower()

    # Check if user exists
    user_match = users[users["email"] == email]

    if user_match.empty:
        st.error("Invalid email or password.")
        return False

    user_record = user_match.iloc[0]

    # Check password
    if str(user_record["password"]) == str(password):
        st.session_state.logged_in = True
        st.session_state.role = user_record["role"]
        st.session_state.user_email = email
        st.session_state.user_name = user_record.get("name", email.split('@')[0])

        # Role-based redirection
        if user_record["role"] == "admin":
            st.session_state.page = "admin"
        elif user_record["role"] == "manager":
            st.session_state.page = "manager"
        else:
            st.session_state.page = "store"

        st.success(f"Welcome back, {st.session_state.user_name}!")
        return True

    st.error("Invalid email or password.")
    return False


def logout():
    """Securely clears all session data."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session()
    st.session_state.page = "store"  # Go back to public store after logout


def signup(name, email, password, confirm_password):
    if not name or not email or not password:
        st.error("All fields are required.")
        return False
    if password != confirm_password:
        st.error("Passwords do not match.")
        return False

    # Get current users to check for duplicates
    users = get_users()
    if email in users['email'].values:
        st.error("An account with this email already exists.")
        return False

    add_user(name, email, password)
    st.success("Account created successfully! Please log in.")
    return True
