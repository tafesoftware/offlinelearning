from flask import Blueprint, current_app, render_template
from app.database import db_session

bp = Blueprint("pages", __name__)


@bp.route("/home")
def home():
    return render_template(
        "pages/home.html",
        app_name=current_app.config["APP_NAME"],
        tagline=current_app.config["TAGLINE"],
    )


@bp.route("/contact")
def contact():
    return render_template(
        "pages/info.html",
        page_title="Contact Us",
        intro="For help with accounts, courses, or classroom access, contact your teacher or school administrator.",
        details=[
            "This installation does not have an email address or phone number configured.",
            "The LMS runs locally at your school, so support is provided by your school team.",
        ],
    )


@bp.route("/location")
def location():
    with db_session() as conn:
        rows = conn.execute(
            "SELECT key, value FROM school_settings WHERE key IN (?, ?)",
            ("school_name", "district"),
        ).fetchall()
    settings = {row["key"]: row["value"] for row in rows}

    return render_template(
        "pages/info.html",
        page_title="Location",
        intro="School information configured for this Offline LMS installation:",
        details=[
            f"School: {settings.get('school_name', 'Not configured')}",
            f"District: {settings.get('district', 'Not configured')}",
            "A physical street address has not been configured. Ask your school administrator for directions.",
        ],
    )


@bp.route("/about")
def about():
    return render_template(
        "pages/info.html",
        page_title="About System",
        intro="Offline LMS is an offline-first learning platform for rural and remote schools.",
        details=[
            "Students can access lessons, textbooks, and quizzes on the school's local network.",
            "Learning activity can be saved offline and synchronized when devices reconnect.",
            "Teachers can manage courses, review progress, and exchange curriculum using local sync tools.",
        ],
    )
