from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database.db import get_db

app = Flask(__name__)
app.config["SECRET_KEY"] = "super_secret_session_key_123456"

# ----------------- Helpers & Middlewares ----------------- #

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "admin":
            flash("Administrator access required.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_cart_count():
    count = 0
    if "user_id" in session:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT SUM(quantity) as total_qty FROM cart WHERE user_id = %s", (session["user_id"],))
                res = cur.fetchone()
                count = int(res["total_qty"] or 0) if res else 0
        finally:
            conn.close()
    return dict(cart_count=count)

# ----------------- Auth Routes ----------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                if cur.fetchone():
                    flash("Email is already registered.", "danger")
                    return render_template("register.html")

                hashed = generate_password_hash(password)
                cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'user')",
                            (name, email, hashed))
                flash("Registration successful! Please login.", "success")
                return redirect(url_for("login"))
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cur.fetchone()

                if not user or not check_password_hash(user["password"], password):
                    flash("Invalid email or password.", "danger")
                    return render_template("login.html")

                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["email"] = user["email"]
                session["role"] = user["role"]

                flash(f"Welcome back, {user['name']}!", "success")
                if user["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                return redirect(url_for("index"))
        finally:
            conn.close()
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ----------------- Storefront Routes ----------------- #

@app.route("/")
def index():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT 8")
            featured = cur.fetchall()
            return render_template("index.html", featured=featured)
    finally:
        conn.close()

@app.route("/products")
def products():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if search:
        query += " AND (name LIKE %s OR description LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    if category and category != "All":
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY id DESC"

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            all_products = cur.fetchall()
            cur.execute("SELECT DISTINCT category FROM products ORDER BY category ASC")
            categories = [r["category"] for r in cur.fetchall()]
            return render_template("products.html", products=all_products, categories=categories, selected_cat=category, search=search)
    finally:
        conn.close()

@app.route("/products/<int:id>")
def product_detail(id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (id,))
            product = cur.fetchone()
            if not product:
                abort(404)
            return render_template("product_detail.html", product=product)
    finally:
        conn.close()

# ----------------- Cart & Checkout ----------------- #

@app.route("/cart")
@login_required
def cart():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id as cart_id, c.quantity, p.id as product_id, p.name, p.price, p.image, p.stock
                FROM cart c JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            """, (session["user_id"],))
            items = cur.fetchall()
            total = sum(float(item["price"]) * item["quantity"] for item in items)
            return render_template("cart.html", items=items, total=total)
    finally:
        conn.close()

@app.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    qty = int(request.form.get("quantity", 1))
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity = quantity + %s
            """, (session["user_id"], product_id, qty, qty))
            flash("Item added to cart!", "success")
    finally:
        conn.close()
    return redirect(request.referrer or url_for("products"))

@app.route("/cart/update/<int:cart_id>", methods=["POST"])
@login_required
def update_cart(cart_id):
    action = request.form.get("action")
    conn = get_db()
    try:
        with conn.cursor() as cur:
            if action == "increase":
                cur.execute("UPDATE cart SET quantity = quantity + 1 WHERE id = %s AND user_id = %s", (cart_id, session["user_id"]))
            elif action == "decrease":
                cur.execute("SELECT quantity FROM cart WHERE id = %s AND user_id = %s", (cart_id, session["user_id"]))
                row = cur.fetchone()
                if row and row["quantity"] > 1:
                    cur.execute("UPDATE cart SET quantity = quantity - 1 WHERE id = %s AND user_id = %s", (cart_id, session["user_id"]))
                else:
                    cur.execute("DELETE FROM cart WHERE id = %s AND user_id = %s", (cart_id, session["user_id"]))
            elif action == "delete":
                cur.execute("DELETE FROM cart WHERE id = %s AND user_id = %s", (cart_id, session["user_id"]))
    finally:
        conn.close()
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.quantity, p.id as product_id, p.name, p.price, p.stock
                FROM cart c JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            """, (session["user_id"],))
            items = cur.fetchall()
            if not items:
                flash("Your cart is empty.", "warning")
                return redirect(url_for("products"))

            total = sum(float(i["price"]) * i["quantity"] for i in items)

            if request.method == "POST":
                address = request.form.get("address", "").strip()
                if not address:
                    flash("Shipping address is required.", "danger")
                    return render_template("checkout.html", items=items, total=total)

                for item in items:
                    if item["stock"] < item["quantity"]:
                        flash(f"Insufficient stock for {item['name']}.", "danger")
                        return render_template("checkout.html", items=items, total=total)

                cur.execute("INSERT INTO orders (user_id, total_amount, shipping_address, status) VALUES (%s, %s, %s, 'Pending')",
                            (session["user_id"], total, address))
                order_id = cur.lastrowid

                for item in items:
                    cur.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                                (order_id, item["product_id"], item["quantity"], item["price"]))
                    cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (item["quantity"], item["product_id"]))

                cur.execute("DELETE FROM cart WHERE user_id = %s", (session["user_id"],))
                flash("Order placed successfully!", "success")
                return redirect(url_for("order_tracking", id=order_id))

            return render_template("checkout.html", items=items, total=total)
    finally:
        conn.close()

# ----------------- Orders & Profile ----------------- #

@app.route("/orders")
@login_required
def orders():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY id DESC", (session["user_id"],))
            user_orders = cur.fetchall()
            return render_template("orders.html", orders=user_orders)
    finally:
        conn.close()

@app.route("/orders/<int:id>")
@login_required
def order_tracking(id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE id = %s", (id,))
            order = cur.fetchone()
            if not order:
                abort(404)
            if session.get("role") != "admin" and order["user_id"] != session["user_id"]:
                abort(403)
            cur.execute("""
                SELECT oi.*, p.name, p.image FROM order_items oi
                JOIN products p ON oi.product_id = p.id WHERE oi.order_id = %s
            """, (id,))
            items = cur.fetchall()
            return render_template("order_tracking.html", order=order, items=items)
    finally:
        conn.close()

@app.route("/profile")
@login_required
def profile():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, role, created_at FROM users WHERE id = %s", (session["user_id"],))
            user = cur.fetchone()
            return render_template("profile.html", user=user)
    finally:
        conn.close()

# ----------------- Admin Routes ----------------- #

@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as c FROM orders")
            total_orders = cur.fetchone()["c"]
            cur.execute("SELECT SUM(total_amount) as s FROM orders WHERE status != 'Cancelled'")
            rev = cur.fetchone()["s"] or 0
            cur.execute("SELECT COUNT(*) as c FROM products")
            total_prods = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(*) as c FROM users")
            total_users = cur.fetchone()["c"]
            return render_template("admin/dashboard.html", total_orders=total_orders, revenue=rev, total_prods=total_prods, total_users=total_users)
    finally:
        conn.close()

@app.route("/admin/products", methods=["GET", "POST"])
@admin_required
def admin_products():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            if request.method == "POST":
                name = request.form["name"]
                desc = request.form["description"]
                price = float(request.form["price"])
                category = request.form["category"]
                image = request.form["image"]
                stock = int(request.form["stock"])
                cur.execute("INSERT INTO products (name, description, price, category, image, stock) VALUES (%s,%s,%s,%s,%s,%s)",
                            (name, desc, price, category, image, stock))
                flash("Product successfully added!", "success")
                return redirect(url_for("admin_products"))

            cur.execute("SELECT * FROM products ORDER BY id DESC")
            prods = cur.fetchall()
            return render_template("admin/products.html", products=prods)
    finally:
        conn.close()

@app.route("/admin/products/delete/<int:id>", methods=["POST"])
@admin_required
def delete_product(id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s", (id,))
            flash("Product removed successfully.", "info")
    finally:
        conn.close()
    return redirect(url_for("admin_products"))

@app.route("/admin/orders")
@admin_required
def admin_orders():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT o.*, u.name as user_name, u.email as user_email
                FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.id DESC
            """)
            orders = cur.fetchall()
            return render_template("admin/orders.html", orders=orders)
    finally:
        conn.close()

@app.route("/admin/orders/update/<int:id>", methods=["POST"])
@admin_required
def update_order_status(id):
    new_status = request.form.get("status")
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, id))
            flash(f"Order #{id} status updated to {new_status}.", "success")
    finally:
        conn.close()
    return redirect(url_for("admin_orders"))

@app.route("/admin/users")
@admin_required
def admin_users():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, role, created_at FROM users ORDER BY id DESC")
            users = cur.fetchall()
            return render_template("admin/users.html", users=users)
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
