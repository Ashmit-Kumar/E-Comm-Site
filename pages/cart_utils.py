import streamlit as st


def add_to_cart(product_id, name, price, quantity=1):
    """Adds an item to the session state cart and shows a success toast."""
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    if product_id in st.session_state.cart:
        # Check if corrupted by old session state
        if isinstance(st.session_state.cart[product_id], int):
            st.session_state.cart[product_id] = {'name': name, 'price': price,
                                                 'quantity': st.session_state.cart[product_id] + quantity}
        else:
            st.session_state.cart[product_id]['quantity'] += quantity
    else:
        st.session_state.cart[product_id] = {'name': name, 'price': price, 'quantity': quantity}

    st.toast(f"Added {name} to your cart! 🛒", icon="✅")


@st.dialog("🛒 Your Shopping Cart")
def show_cart_modal():
    """Renders a pop-up modal showing cart contents and a checkout button."""
    if not st.session_state.cart:
        st.info("Your cart is currently empty. Start shopping!")
        return

    total_price = 0.0

    for pid, item in st.session_state.cart.items():
        # Failsafe if old integer data is still stuck in the session
        if isinstance(item, int):
            st.session_state.cart = {}
            st.rerun()

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
        with col2:
            st.markdown(f"{item['quantity']} x ${item['price']:.2f}")
        with col3:
            item_total = item['quantity'] * item['price']
            total_price += item_total
            st.markdown(f"**${item_total:.2f}**")

    st.markdown("---")

    checkout_col1, checkout_col2 = st.columns([1, 1])
    with checkout_col1:
        st.markdown(f"<h3 style='margin: 0;'>Total: ${total_price:.2f}</h3>", unsafe_allow_html=True)
    with checkout_col2:
        if st.button("💳 Secure Checkout", type="primary", use_container_width=True):
            st.session_state.cart = {}  # Empty the cart
            st.success("Payment successful! Thank you for your order.")
            st.rerun()


def render_store_header():
    """Universal header for all store pages."""
    header_col, cart_col = st.columns([4, 1])

    with header_col:
        user_name = st.session_state.get('user_name', 'Guest')
        st.markdown(f"<h2 style='margin-bottom: 0; color: #1E1E1E;'>Welcome, {user_name}</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666; font-size: 0.9rem;'>Discover our latest ML-curated products.</p>",
                    unsafe_allow_html=True)

    with cart_col:
        cart = st.session_state.get("cart", {})

        # ERROR FIX: Safely calculate count even if session state has old integers
        cart_count = 0
        for item in cart.values():
            if isinstance(item, dict):
                cart_count += item.get('quantity', 1)
            else:
                cart_count += 1  # Catch the rogue ints

        st.write("")
        if st.button(f"🛒 Cart ({cart_count})", type="primary", use_container_width=True):
            show_cart_modal()

    st.markdown("---")