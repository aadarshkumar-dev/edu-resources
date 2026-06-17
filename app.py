from flask import Flask, render_template, request, flash, session, redirect, url_for
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "jgfjiosfjksdfjosd"

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')

DB_NAME = "database.db"

@app.route("/users")
def show_users():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users")
    rows = cursor.fetchall()
    connection.close()

    return render_template("users.html", users=rows)


# ------------------ DB Setup ------------------
def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

init_db()

# ------------------ Signup Route ------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please fill in both fields.")
            return redirect(url_for("signup"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.")
            return redirect(url_for("signup"))

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        try:
            connection = sqlite3.connect(DB_NAME)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            connection.commit()
            connection.close()
            flash("Signup successful! Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists. Try another.")
            return redirect(url_for("signup"))

    # GET request → show signup form
    return render_template("signup.html")

# ------------------ Login Route ------------------
# ------------------ Login Route ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        connection = sqlite3.connect(DB_NAME)  # ✅ use the same DB_NAME everywhere
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        connection.close()

        if user and bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash(f"Login successful! {session['username']}")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))

    # GET request → show login form
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session['username'])

# ------------------ Logout Route ------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
