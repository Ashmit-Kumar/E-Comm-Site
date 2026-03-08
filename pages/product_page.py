import streamlit as st

from database.db import get_products
from pages.cart_utils import render_store_header, add_to_cart


def product_page():
    # 1. Use the new universal header so it matches the store perfectly!
    render_store_header()

    # 2. Back Navigation
    if st.button("← Back to Store"):
        st.session_state.page = "store"
        st.rerun()

    # 3. Load Product Data
    product_id = st.session_state.get("selected_product")
    if not product_id:
        st.error("No product selected.")
        return

    products = get_products()
    product_data = products[products["id"] == product_id]

    if product_data.empty:
        st.error("Product not found.")
        return

    product = product_data.iloc[0]

    # 4. Product UI Layout
    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        img_url = f"https://placehold.co/600x600/f8f9fa/333333?text={product['name'].replace(' ', '+')}"
        st.markdown(
            f"""
                <div style="height: 400px; overflow: hidden; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <img src="{product['image']}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                """,
            unsafe_allow_html=True
        )

    with col2:
        st.title(product["name"])
        st.markdown(f"**Category:** {product['category']} | ⭐ {product['rating']}")
        st.markdown(f"<h2 style='color: #1E1E1E;'>${product['price']:.2f}</h2>", unsafe_allow_html=True)

        st.markdown("### Description")
        st.write(product["description"])

        st.markdown("---")

        # 5. The Working Add to Cart Button!
        if product["stock"] > 0:
            if st.session_state.get("logged_in", False):
                quantity = st.number_input("Quantity", min_value=1, max_value=product["stock"], value=1)
                if st.button("🛍️ Add to Cart", type="primary", use_container_width=True):
                    add_to_cart(product['id'], product['name'], product['price'], quantity)
                    st.rerun()
            else:
                # Guest View
                st.warning("Please log in to add items to your cart.")
                if st.button("🔐 Login to Purchase", type="primary", use_container_width=True):
                    st.session_state.page = "login"
                    st.rerun()
