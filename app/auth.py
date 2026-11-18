import hashlib
import os
import hmac
from functools import wraps
from flask import session, redirect, url_for, flash, g, request
from app.database import db_session

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}${key.hex()}"

def verify_password(stored_hash: str, password: str) -> bool:
    """Verifies a password against the stored salt and hash."""
    try:
        salt_hex, key_hex = stored_hash.split("$")
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(key, expected_key)
    except Exception:
        return False

def get_current_user():
    """Retrieves the currently logged-in user from the database."""
    if "user_id" not in session:
        return None
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name, role, grade_level FROM users WHERE id = ?", (session["user_id"],))
        row = cursor.fetchone()
        return dict(row) if row else None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        if session.get("role") not in ("teacher", "admin"):
            flash("Access restricted to teachers and administrators.", "danger")
            return redirect(url_for("student.dashboard"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        if session.get("role") != "admin":
            flash("Access restricted to administrators.", "danger")
            return redirect(url_for("student.dashboard"))
        return f(*args, **kwargs)
    return decorated_function
