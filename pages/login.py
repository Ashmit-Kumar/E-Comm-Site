import streamlit as st
from auth import login, signup


def login_page():
    # 1. THE EXIT BUTTON
    # This allows users to escape the login screen and go back to browsing
    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Back to Store", type="secondary"):
            st.session_state.page = "store"
            st.rerun()

    # Initialize a local state to toggle between Login and Signup
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    st.markdown(
        f"<h1 style='text-align: center;'>{'Create Account' if st.session_state.auth_mode == 'signup' else 'Welcome Back'}</h1>",
        unsafe_allow_html=True)

    # Center the form
    _, col, _ = st.columns([1, 2, 1])

    with col:
        with st.container(border=True):
            if st.session_state.auth_mode == "login":
                # --- LOGIN FORM ---
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")

                if st.button("Login", type="primary", use_container_width=True):
                    if login(email, password):
                        st.rerun()

                st.markdown("---")
                if st.button("New here? Create an account", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()

            else:
                # --- SIGNUP FORM ---
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email Address")
                new_pass = st.text_input("Create Password", type="password")
                conf_pass = st.text_input("Confirm Password", type="password")

                if st.button("Sign Up", type="primary", use_container_width=True):
                    if signup(new_name, new_email, new_pass, conf_pass):
                        st.session_state.auth_mode = "login"
                        st.rerun()

                st.markdown("---")
                if st.button("Already have an account? Log in", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()