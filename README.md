# 🛒 ShopSphere - Full-Stack E-Commerce Web Application

A full-stack online shopping web application built with **Python (Flask)**, **MySQL**, **HTML5**, **CSS3**, and **JavaScript**. The application supports user authentication, catalog browsing with search and category filters, cart management, checkout with order placement, order tracking, and an administrative dashboard to manage inventory and orders. All pricing is configured in **Indian Rupees (₹)**.

---

## 🚀 Features

### Customer Features
- **User Authentication:** Registration, secure login/logout with hashed passwords.
- **Product Catalog:** Browse 20 pre-seeded products across multiple categories (Electronics, Gaming, Fashion, Footwear, Home & Kitchen, Accessories).
- **Search & Filters:** Search products by keyword and filter dynamically by category.
- **Product Details:** View descriptions, live stock availability, and high-resolution images.
- **Shopping Cart:** Add items, adjust quantities (`+` / `-`), remove items, and see calculated subtotals.
- **Checkout & Order Creation:** Shipping address validation and immediate stock deduction.
- **Order Tracking & History:** View past orders, delivery details, and live status.
- **User Profile:** View account details and registration timestamp.

### Admin Dashboard Features
- **Key Metrics Overview:** Total revenue (₹), total orders placed, active products count, and total registered users.
- **Inventory Management:** Add new products, configure stock, price in ₹, image URLs, and delete products.
- **Order Processing:** Update order fulfillment stages (`Pending` → `Confirmed` → `Processing` → `Shipped` → `Delivered` → `Cancelled`).
- **User Directory:** View all registered accounts and assigned roles.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, PyMySQL, Werkzeug (Password Hashing)
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript (Jinja2 Templates)
- **Styling:** Custom responsive CSS design

---

## 📁 Project Structure

```text
ecommerce-app/
├── app.py                  # Core Flask application and routing
├── config.py               # Database and session configuration
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment variables template
├── database/
│   ├── db.py               # MySQL connection handler
│   ├── schema.sql          # Database tables creation script
│   └── seed.sql            # Initial sample data (20 products + test accounts)
├── static/
│   ├── css/
│   │   └── style.css       # Application stylesheet
│   └── js/
│       └── main.js         # Client-side JavaScript
├── templates/
│   ├── base.html           # Master layout template
│   ├── index.html          # Homepage with featured products
│   ├── products.html       # Full catalog with search/filter
│   ├── product_detail.html # Single product view
│   ├── login.html          # User login
│   ├── register.html       # User registration
│   ├── cart.html           # Shopping cart
│   ├── checkout.html       # Shipping and order review
│   ├── orders.html         # User order history
│   ├── order_tracking.html # Order timeline & item details
│   ├── profile.html        # User profile page
│   └── admin/
│       ├── dashboard.html  # Admin revenue and stats
│       ├── products.html   # Product management (CRUD)
│       ├── orders.html     # Order status updates
│       └── users.html      # Registered users list
└── README.md
