import streamlit as st

from database.db import get_users, update_user_role


def admin_panel():
    # Security Check: ONLY Admins allowed
    if st.session_state.get("role") != "admin":
        st.error("🚨 Access Denied. Administrator privileges required.")
        if st.button("Return to Store"):
            st.session_state.page = "store"
            st.rerun()
        return

    st.markdown("## ⚙️ Admin Console")
    st.markdown("Manage system access, user roles, and high-level platform health.")

    users_df = st.session_state.get('user_db', get_users())

    tab1, tab2 = st.tabs(["👥 User Management", "🛡️ Security Logs"])

    # --- TAB 1: USER MANAGEMENT ---
    with tab1:
        st.markdown("### User Demographics")

        # Calculate Role Metrics
        total_users = len(users_df)
        admin_count = len(users_df[users_df['role'] == 'admin'])
        manager_count = len(users_df[users_df['role'] == 'manager'])
        customer_count = len(users_df[users_df['role'] == 'customer'])

        # Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                st.metric("Total Users", total_users)
        with col2:
            with st.container(border=True):
                st.metric("Admins", admin_count)
        with col3:
            with st.container(border=True):
                st.metric("Managers", manager_count)
        with col4:
            with st.container(border=True):
                st.metric("Customers", customer_count)

        st.markdown("---")

        # Layout: Table on the left, Control Form on the right
        table_col, control_col = st.columns([2, 1], gap="large")

        with table_col:
            st.markdown("#### User Database")
            # Hide passwords for security, even from admins!
            display_users = users_df.drop(columns=['password'], errors='ignore')
            st.dataframe(display_users, hide_index=True, use_container_width=True)

        with control_col:
            st.markdown("#### Modify Roles")
            with st.form("role_update_form"):
                # Dropdown to select a user by email
                user_emails = users_df['email'].tolist()
                selected_email = st.selectbox("Select User", user_emails)

                # Dropdown for the new role
                new_role = st.selectbox("Assign New Role", ["customer", "manager", "admin"])

                # Warning note
                st.markdown(
                    "<p style='font-size: 0.8rem; color: gray;'>Note: Promoting a user grants them immediate access to restricted dashboards.</p>",
                    unsafe_allow_html=True)

                submitted = st.form_submit_button("Update User Role", type="primary", use_container_width=True)

                if submitted:
                    # Prevent admins from accidentally demoting themselves
                    if selected_email == st.session_state.user_email and new_role != "admin":
                        st.error("Action Blocked: You cannot demote your own active account.")
                    else:
                        update_user_role(selected_email, new_role)
                        st.success(f"Successfully updated {selected_email} to **{new_role}**!")
                        # Slight delay to show the message before refreshing
                        import time
                        time.sleep(1)
                        st.rerun()

    # --- TAB 2: SECURITY LOGS (Placeholder) ---
    with tab2:
        st.markdown("### System Activity")
        st.info(
            "Audit logging is currently disabled. Future updates will track login attempts, role changes, and inventory deletions here.")
