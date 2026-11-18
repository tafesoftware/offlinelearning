from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.database import db_session
from app.auth import hash_password, verify_password

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, full_name, role FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and verify_password(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["full_name"] = user["full_name"]
                session["role"] = user["role"]
                
                flash(f"Welcome back, {user['full_name']}!", "success")
                next_url = request.args.get("next")
                if next_url:
                    return redirect(next_url)
                if user["role"] in ("teacher", "admin"):
                    return redirect(url_for("teacher.dashboard"))
                return redirect(url_for("student.dashboard"))
            else:
                flash("Invalid username or password. Please try again.", "danger")
                
    return render_template("auth/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        full_name = request.form.get("full_name", "").strip()

        if not full_name and (first_name or last_name):
            full_name = f"{first_name} {last_name}".strip()

        role = request.form.get("role", "student")
        grade_level = request.form.get("grade_level", "Grade 9")
        
        if not username or not password or not full_name:
            flash("All fields including First Name and Last Name are required.", "warning")
            return render_template("auth/register.html")
            
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                flash("Username already exists. Please pick another.", "danger")
                return render_template("auth/register.html")
                
            pwd_hash = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role, grade_level)
                VALUES (?, ?, ?, ?, ?)
            """, (username, pwd_hash, full_name, role, grade_level))
            
            flash("Account registered successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))
            
    return render_template("auth/register.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))
