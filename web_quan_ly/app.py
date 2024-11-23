from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from psycopg2 import sql
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=session.get("dbname", "test"),
        user=session.get("user", "postgres"),
        password=session.get("password", "123456"),
        host=session.get("host", "localhost"),
        port=session.get("port", "5432")
    )

# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("profile"))  # Chuyển hướng đến trang cá nhân
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Username đã tồn tại. Vui lòng chọn tên khác.", "danger")
            conn.close()
            return redirect(url_for("register"))

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        conn.close()

        flash("Tài khoản đã được tạo thành công.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Logout route
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

# Profile route
@app.route("/profile")
def profile():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    username = session.get("username")
    return render_template("profile.html", username=username)

# Main index route (protected) - Hỗ trợ tìm kiếm và hiển thị danh sách
@app.route("/index", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()

    message = None
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        query = """
            SELECT * FROM danhsach 
            WHERE hoten ILIKE %s OR diachi ILIKE %s
        """
        cur.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        rows = cur.fetchall()
        message = f"Kết quả tìm kiếm cho từ khóa: '{keyword}'"
    else:
        cur.execute("SELECT * FROM danhsach")
        rows = cur.fetchall()

    conn.close()

    users = [{"id": row[0], "hoten": row[1], "diachi": row[2]} for row in rows]

    return render_template("index.html", users=users, message=message)

# Delete user route
@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM danhsach WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!", "success")
    return redirect(url_for("index"))

# Add user route
@app.route("/add", methods=["GET", "POST"])
def add_user():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        hoten = request.form.get("hoten")  # Sử dụng get để tránh KeyError
        diachi = request.form.get("diachi")

        if not hoten or not diachi:
            flash("Vui lòng điền đầy đủ thông tin!", "danger")
            return redirect(url_for("add_user"))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO danhsach (hoten, diachi) VALUES (%s, %s)", (hoten, diachi))
        conn.commit()
        conn.close()
        flash("User added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add_user.html")

# Connect SQL route
@app.route("/connect", methods=["GET", "POST"])
def connect_sql():
    if request.method == "POST":
        dbname = request.form["dbname"]
        user = request.form["user"]
        password = request.form["password"]
        host = request.form["host"]
        port = request.form["port"]

        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()

            session["dbname"] = dbname
            session["user"] = user
            session["password"] = password
            session["host"] = host
            session["port"] = port

            flash("Kết nối cơ sở dữ liệu thành công!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Không thể kết nối cơ sở dữ liệu: {e}", "danger")

    return render_template("connect.html")
@app.route("/search", methods=["POST"])
def search_user():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    keyword = request.form.get("keyword", "").strip()
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT * FROM danhsach 
        WHERE hoten ILIKE %s OR diachi ILIKE %s
    """
    cur.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    conn.close()

    users = [{"id": row[0], "hoten": row[1], "diachi": row[2]} for row in rows]
    message = f"Kết quả tìm kiếm cho từ khóa: '{keyword}'" if keyword else None

    return render_template("index.html", users=users, message=message)

if __name__ == "__main__":
    app.run(debug=True)
