import streamlit as st

from database.db import get_products
from pages.cart_utils import render_store_header


def get_stock_badge(stock: int) -> str:
    """Returns a styled HTML badge based on inventory levels."""
    if stock > 20:
        return "<span style='color: #10B981; font-size: 0.8rem; font-weight: 600;'>● In Stock</span>"
    elif stock > 0:
        return f"<span style='color: #F59E0B; font-size: 0.8rem; font-weight: 600;'>● Low Stock ({stock} left)</span>"
    else:
        return "<span style='color: #EF4444; font-size: 0.8rem; font-weight: 600;'>● Out of Stock</span>"


def customer_store():
    render_store_header()
    products = get_products()

    # --- 1. Search & Filter Bar ---
    search_col, cat_col, price_col = st.columns([2, 1, 1])

    with search_col:
        search = st.text_input("Search", placeholder="🔍 Search for gadgets, gear...", label_visibility="collapsed")
    with cat_col:
        categories = ["All Categories"] + list(products["category"].unique())
        selected_cat = st.selectbox("Category", categories, label_visibility="collapsed")
    with price_col:
        with st.popover("Price Range 💰", use_container_width=True):
            min_p, max_p = float(products["price"].min()), float(products["price"].max())
            price_range = st.slider("Select Range", min_p, max_p, (min_p, max_p), label_visibility="collapsed")

    # --- 2. Filtering Logic ---
    filtered_df = products[
        (products["price"].between(price_range[0], price_range[1]))
    ]
    if selected_cat != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == selected_cat]
    if search:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search, case=False)]

    st.write("")  # Spacer

    # --- 3. Product Grid ---
    if filtered_df.empty:
        st.info("No products found matching your exact criteria. Try adjusting your filters!", icon="🔍")
    else:
        cols = st.columns(4)
        for i, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[i % 4]:
                # The Product Card
                with st.container(border=True):
                    img_url = f"https://placehold.co/400x300/f8f9fa/333333?text={row['name'].replace(' ', '+')}"
                    st.markdown(
                        f"""
                            <div style="height: 200px; overflow: hidden; border-radius: 8px; margin-bottom: 10px;">
                                <img src="{row['image']}" style="width: 100%; height: 100%; object-fit: cover;">
                            </div>
                            """,
                        unsafe_allow_html=True
                    )

                    # Product Info
                    st.markdown(f"**{row['name']}**")

                    # Category and Rating
                    st.markdown(
                        f"<div style='display: flex; justify-content: space-between; font-size: 0.8rem; color: #666;'>"
                        f"<span>{row['category']}</span>"
                        f"<span>⭐ {row['rating']}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    # Price and Stock Status
                    st.markdown(
                        f"<div style='margin-top: 5px; margin-bottom: 10px;'>"
                        f"<span style='font-size: 1.2rem; font-weight: 700;'>${row['price']:.2f}</span><br>"
                        f"{get_stock_badge(row['stock'])}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    # Call to Action
                    button_label = "View Details" if row['stock'] > 0 else "View (Out of Stock)"
                    if st.button(button_label, key=f"btn_{row['id']}", use_container_width=True):
                        st.session_state.selected_product = row["id"]
                        st.session_state.page = "product"
                        st.rerun()