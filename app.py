import streamlit as st

# 1. Global Configuration — MUST be the very first Streamlit command
st.set_page_config(
    page_title="SmartStore AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STICKY HEADER ---
# We use position: sticky and top: 2.8rem so it sits neatly just below Streamlit's default hamburger menu
sticky_header = """
<style>
    .sticky-header {
        position: sticky;
        top: 2.8rem; 
        background-color: var(--background-color); /* Automatically adapts to Light/Dark mode! */
        z-index: 999; /* Keeps it above the product cards when scrolling */
        padding: 10px 0px;
        border-bottom: 2px solid var(--primary-color); /* Neon accent line */
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .sticky-header img {
        height: 40px;
        margin-right: 15px;
    }

    .sticky-header h1 {
        margin: 0;
        padding: 0;
        font-size: 2rem;
        color: var(--text-color);
        font-weight: 800;
        letter-spacing: 1.5px;
    }
</style>

<div class="sticky-header">
    <img src="https://cdn-icons-png.flaticon.com/512/3081/3081648.png" alt="SmartStore Logo">
    <h1>SMARTSTORE</h1>
</div>
"""

# Render the header globally
st.markdown(sticky_header, unsafe_allow_html=True)

# --- CUSTOM CSS FOR MINIMALIST UI ---
# This hides default Streamlit branding and adds subtle hover effects
miminialist_css = """
<style>
    # /* Hide Streamlit default header, footer, and menu */
    # #MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # header {visibility: hidden;}

    /* Smooth out button hovers for a premium feel */
    .stButton>button {
        border-radius: 6px;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Clean up sidebar padding */
    .css-1d391kg { padding-top: 1rem; }
</style>
"""
st.markdown(miminialist_css, unsafe_allow_html=True)

# Imports placed after page config to avoid Streamlit Initialization errors
from auth import init_session
from pages.admin_panel import admin_panel
from pages.customer_store import customer_store
from pages.login import login_page
from pages.manager_dashboard import manager_dashboard
from pages.product_page import product_page

# Initialize Session State
init_session()

# --- 2. Initial State Setup ---
if "page" not in st.session_state:
    st.session_state.page = "store"  # Default to store, not login

# --- 3. Sidebar Navigation (Adaptive) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>SMARTSTORE</h2>", unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("logged_in", False):
        # Public View Sidebar
        st.info("Log in to checkout and see personalized deals.")
        if st.session_state.page != "login":
            if st.button("🔐 Login / Sign Up", use_container_width=True, type="primary"):
                st.session_state.page = "login"
                st.rerun()
    else:
        # Logged In Sidebar (Admin/Manager/Customer)
        user_name = st.session_state.get('user_name', 'User')
        st.markdown(f"<div style='text-align: center;'>Logged in as <b>{user_name}</b></div>", unsafe_allow_html=True)

        # Navigation based on roles
        if st.button("🛍️ Browse Store", use_container_width=True):
            st.session_state.page = "store"
            st.rerun()

        role = st.session_state.get("role")
        if role == "manager":
            if st.button("📊 Manager Dashboard", use_container_width=True):
                st.session_state.page = "manager"
                st.rerun()
        elif role == "admin":
            if st.button("⚙️ Admin Console", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            from auth import logout

            logout()
            st.session_state.page = "store"
            st.rerun()

# --- 4. The Main Content Router ---
current_page = st.session_state.get("page", "store")

if current_page == "store":
    customer_store()
elif current_page == "login":
    login_page()
elif current_page == "product":
    product_page()
elif current_page == "manager":
    manager_dashboard()
elif current_page == "admin":
    admin_panel()
