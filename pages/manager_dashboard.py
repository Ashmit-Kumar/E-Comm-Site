import streamlit as st

from database.db import get_products, add_product


def manager_dashboard():
    # Security Check
    if st.session_state.get("role") not in ["manager", "admin"]:
        st.error("🚨 Access Denied. You do not have permission to view this page.")
        if st.button("Return to Store"):
            st.session_state.page = "store"
            st.rerun()
        return

    st.markdown("## 📊 Manager Dashboard")
    st.markdown("Track store performance, manage inventory, and expand the catalog.")

    products_df = get_products()

    # 3-Tab Layout for a clean workspace
    tab1, tab2, tab3 = st.tabs(["📈 Analytics", "📦 Inventory Overview", "➕ Add New Product"])

    # --- TAB 1: ANALYTICS ---
    with tab1:
        st.markdown("### 📊 Store Health & Financials")

        # --- 1. Advanced Calculations ---
        # Base metrics
        total_products = len(products_df)
        total_inventory_value = (products_df['price'] * products_df['stock']).sum()
        low_stock_items = products_df[products_df['stock'] <= products_df['reorder_point']]
        low_stock_count = len(low_stock_items)
        out_of_stock_count = len(products_df[products_df['stock'] == 0])

        # Profitability metrics
        products_df['profit_per_unit'] = products_df['price'] - products_df['cost']
        products_df['margin_pct'] = (products_df['profit_per_unit'] / products_df['price']) * 100
        products_df['total_potential_profit'] = products_df['profit_per_unit'] * products_df['stock']

        total_potential_profit = products_df['total_potential_profit'].sum()
        avg_margin = products_df['margin_pct'].mean()

        # --- 2. Top-level Metric Cards (Row 1) ---
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.metric("Total Unique Products", total_products)
        with col2:
            with st.container(border=True):
                st.metric("Total Inventory Value", f"${total_inventory_value:,.2f}")
        with col3:
            with st.container(border=True):
                st.metric("Total Potential Profit", f"${total_potential_profit:,.2f}",
                          help="Total profit if all current stock is sold at full price.")

        # --- 3. Top-level Metric Cards (Row 2) ---
        col4, col5, col6 = st.columns(3)
        with col4:
            with st.container(border=True):
                st.metric("Average Profit Margin", f"{avg_margin:.1f}%")
        with col5:
            with st.container(border=True):
                st.metric("Low Stock Alerts", low_stock_count,
                          delta=f"-{low_stock_count} Action Required" if low_stock_count > 0 else "Optimal",
                          delta_color="inverse" if low_stock_count > 0 else "normal")
        with col6:
            with st.container(border=True):
                st.metric("Out of Stock", out_of_stock_count,
                          delta=f"-{out_of_stock_count} Lost Sales" if out_of_stock_count > 0 else "0",
                          delta_color="inverse")

        st.markdown("---")

        # --- 4. Visualizations ---
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("#### Stock Distribution by Category")
            cat_stock = products_df.groupby("category")["stock"].sum()
            st.bar_chart(cat_stock, color="#00FFAA")

        with chart_col2:
            st.markdown("#### Potential Profit by Category")
            cat_profit = products_df.groupby("category")["total_potential_profit"].sum()
            st.bar_chart(cat_profit, color="#8B5CF6")

        st.markdown("---")

        # --- 5. Data Tables ---
        table_col1, table_col2 = st.columns(2, gap="large")

        with table_col1:
            st.markdown("#### ⭐ Top Rated Products")
            # Get top 5 highest-rated products
            top_rated = products_df.nlargest(5, 'rating')[['name', 'category', 'rating', 'margin_pct']]

            # Format the margin percentage for the table
            top_rated['margin_pct'] = top_rated['margin_pct'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(top_rated, hide_index=True, use_container_width=True)

        with table_col2:
            st.markdown("#### ⚠️ Immediate Restock Required")
            if low_stock_count > 0:
                # Sort by lowest stock first
                critical_stock = low_stock_items.sort_values(by='stock')[
                    ['name', 'stock', 'reorder_point', 'lead_time_days']]
                st.dataframe(critical_stock, hide_index=True, use_container_width=True)
            else:
                st.success("All products are currently well-stocked!")

    # --- TAB 2: INVENTORY TABLE ---
    with tab2:
        st.markdown("### Current Catalog")
        display_df = products_df.drop(columns=['description', 'image', 'potential_revenue'], errors='ignore')

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "price": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
                "cost": st.column_config.NumberColumn("Cost ($)", format="$%.2f"),
                "stock": st.column_config.ProgressColumn("Stock Level", min_value=0, max_value=100)
            }
        )

    # --- TAB 3: ADD PRODUCT FORM ---
    with tab3:
        st.markdown("### Add a Product to the Catalog")

        with st.form("new_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Product Name*")
                # Using dynamic categories from existing data, plus an option for a new one
                existing_cats = list(products_df['category'].unique())
                category = st.selectbox("Category*", existing_cats + ["Other (Define in description)"])
                price = st.number_input("Selling Price ($)*", min_value=0.0, step=0.5)
                cost = st.number_input("Cost to Produce/Buy ($)", min_value=0.0, step=0.5)
                image_url = st.text_input("Image URL*", placeholder="https://images.unsplash.com/...")

            with col2:
                stock = st.number_input("Initial Stock Quantity*", min_value=0, step=1)
                reorder = st.number_input("Reorder Point (Low stock alert)", min_value=0, step=1)
                lead_time = st.number_input("Lead Time (Days to restock)", min_value=1, step=1)
                rating = st.slider("Initial Rating", min_value=1.0, max_value=5.0, value=5.0, step=0.1)

            desc = st.text_area("Product Description*")

            st.markdown("*Required fields")
            submitted = st.form_submit_button("💾 Save New Product", type="primary", use_container_width=True)

            if submitted:
                if not name or not image_url or not desc:
                    st.error("Please fill out all required fields (Name, Image URL, Description).")
                else:
                    add_product(name, category, price, cost, stock, reorder, lead_time, rating, desc, image_url)
                    st.success(f"Successfully added **{name}** to the store!")

                    # Refresh to update the analytics and tables immediately
                    import time
                    time.sleep(1)
                    st.rerun()
