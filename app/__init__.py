from urllib.parse import urlsplit

from flask import Flask, abort, redirect, request, session, url_for
from app.config import Config
from app.database import init_db
from app.routes.auth_routes import bp as auth_bp
from app.routes.student_routes import bp as student_bp
from app.routes.teacher_routes import bp as teacher_bp
from app.routes.sync_routes import bp as sync_bp
from app.routes.api_routes import bp as api_bp
from app.routes.library_routes import bp as library_bp
from app.routes.pages_routes import bp as pages_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database tables and settings
    with app.app_context():
        init_db()

    # Register modular Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(sync_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(pages_bp)

    @app.context_processor
    def inject_language():
        language = session.get("language", "en")
        return {"current_language": language if language in ("en", "am") else "en"}

    @app.route("/language", methods=["POST"])
    def set_language():
        language = request.form.get("language")
        if language not in ("en", "am"):
            abort(400)

        session["language"] = language
        target = request.form.get("next", "")
        parsed_target = urlsplit(target)
        if target.startswith("/") and not target.startswith("//") and not parsed_target.netloc:
            return redirect(target)
        return redirect(url_for("pages.home"))

    @app.route("/")
    def index():
        if "user_id" in session:
            if session.get("role") in ("teacher", "admin"):
                return redirect(url_for("teacher.dashboard"))
            return redirect(url_for("student.dashboard"))
        return redirect(url_for("pages.home"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("base.html"), 404

    return app
