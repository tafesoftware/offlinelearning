from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.database import db_session
from app.auth import hash_password, verify_password

bp = Blueprint("auth", __name__, url_prefix="/auth")

def _registration_subjects():
    with db_session() as conn:
        rows = conn.execute("""
            SELECT DISTINCT t.grade_level, t.stream, t.subject_code, s.title
            FROM textbooks t
            JOIN subjects s ON s.code = t.subject_code AND s.grade_level = t.grade_level
            WHERE t.grade_level IN ('Grade 11', 'Grade 12')
            ORDER BY t.grade_level,
                     CASE t.stream
                         WHEN 'Natural Science' THEN 0
                         WHEN 'Social Science' THEN 1
                         ELSE 2
                     END,
                     s.title
        """).fetchall()

    subjects = []
    for row in rows:
        name = row["title"]
        prefix = f"Ethiopian {row['grade_level']} "
        suffix = " - Subject Listing"
        stream_suffix = f" ({row['stream']})"
        if name.startswith(prefix):
            name = name[len(prefix):]
        if name.endswith(suffix):
            name = name[:-len(suffix)]
        if name.endswith(stream_suffix):
            name = name[:-len(stream_suffix)]
        for suffix in (" Student Textbook", " Textbook"):
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break
        subjects.append({
            "grade_level": row["grade_level"],
            "stream": row["stream"],
            "name": name,
        })
    return subjects

def _render_registration():
    return render_template(
        "auth/register.html",
        registration_subjects=_registration_subjects(),
    )

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
        stream = request.form.get("stream", "").strip()
        
        if not username or not password or not full_name:
            flash("All fields including First Name and Last Name are required.", "warning")
            return _render_registration()

        if grade_level in ("Grade 11", "Grade 12"):
            if stream not in ("Natural Science", "Social Science"):
                flash("Choose Natural Science or Social Science for Grades 11 and 12.", "warning")
                return _render_registration()
        else:
            stream = None
            
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                flash("Username already exists. Please pick another.", "danger")
                return _render_registration()
                
            pwd_hash = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role, grade_level, stream)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, pwd_hash, full_name, role, grade_level, stream))
            
            flash("Account registered successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))
            
    return _render_registration()

@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))
