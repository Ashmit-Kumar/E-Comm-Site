# 🛒 SmartStore - Streamlit E-Commerce Platform

SmartStore is a fully functional, highly interactive e-commerce storefront built entirely in Python using [Streamlit](https://streamlit.io/). It features a public-facing product catalog, shopping cart functionality, secure authentication, and advanced role-based dashboards for store managers and administrators.

## ✨ Features

* **Adaptive UI/UX:** Features a modern, responsive design with a sticky centered header, uniform product image grids (using CSS `object-fit: cover`), and native support for Light/Dark mode via CSS variables.
* **Public Storefront:** Guests can browse the catalog, view high-quality product images, and check stock levels.
* **Authentication System:** Seamless, single-page Login and Sign-up toggle interface. Users must log in to add items to their cart.
* **Role-Based Access Control (RBAC):**
    * **Customers:** Can browse products, view details, and manage their cart.
    * **Managers:** Access a dedicated **Manager Dashboard** to view financial analytics (profit margins, potential revenue), track low-stock alerts, and add new products dynamically to the store.
    * **Admins:** Access the **Admin Console** to monitor user demographics and promote/demote user roles on the fly.
* **In-Memory Database:** Currently uses `pandas` and `st.session_state` to handle real-time updates for users and inventory without requiring an external database setup.

## 🛠️ Tech Stack

* **Frontend & Backend:** Streamlit (Python)
* **Data Manipulation:** Pandas
* **Styling:** Custom HTML/CSS within Streamlit Markdown

## 📂 Project Structure

```text
smartstore/
│
├── app.py                     # Main router, sidebar navigation, and sticky header
├── auth.py                    # Login, signup, and session initialization logic
├── .streamlit/
│   └── config.toml            # Global theme settings (Dark/Light mode colors)
│
├── database/
│   └── db.py                  # In-memory database for users and 12-item product catalog
│
└── pages/
    ├── customer_store.py      # Public product grid UI
    ├── product_page.py        # Individual product details and Add to Cart logic
    ├── login.py               # Combined Login / Sign-up UI
    ├── manager_dashboard.py   # Analytics, inventory table, and "Add Product" form
    └── admin_panel.py         # User management and role assignment
