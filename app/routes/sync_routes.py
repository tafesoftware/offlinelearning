import json
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, abort
from app.auth import teacher_required
from app.database import db_session
from app.sync import generate_export_bundle, import_curriculum_pack

bp = Blueprint("sync", __name__, url_prefix="/sync")

@bp.route("/")
@teacher_required
def index():
    with db_session() as conn:
        cursor = conn.cursor()
        
        # Sync stats
        cursor.execute("SELECT COUNT(*) as cnt FROM submissions WHERE submitted_offline = 1")
        offline_submissions = cursor.fetchone()["cnt"]
        
        cursor.execute("SELECT COUNT(*) as cnt FROM submissions")
        total_submissions = cursor.fetchone()["cnt"]
        
        cursor.execute("SELECT * FROM sync_logs ORDER BY timestamp DESC LIMIT 15")
        logs = [dict(r) for r in cursor.fetchall()]
        
        cursor.execute("SELECT key, value FROM school_settings")
        settings = {r["key"]: r["value"] for r in cursor.fetchall()}

    return render_template("teacher/sync_manager.html", 
                           offline_submissions=offline_submissions,
                           total_submissions=total_submissions,
                           logs=logs,
                           settings=settings)

@bp.route("/export-bundle")
@teacher_required
def export_bundle():
    """
    Downloads the entire school progress, submissions, and completion data
    as a verifiable JSON bundle to a USB thumb drive for transport to district HQ.
    """
    bundle = generate_export_bundle()
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"beacon_school_sync_{timestamp_str}.beacon.json"
    
    json_bytes = json.dumps(bundle, indent=2).encode("utf-8")
    
    return Response(
        json_bytes,
        mimetype="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/json"
        }
    )

@bp.route("/import-pack", methods=["POST"])
@teacher_required
def import_pack():
    """
    Imports a curriculum content pack (.pack.json) provided via USB drive or download.
    """
    if "pack_file" not in request.files:
        flash("No curriculum pack file was uploaded.", "warning")
        return redirect(url_for("sync.index"))
        
    file = request.files["pack_file"]
    if not file or file.filename == "":
        flash("Please select a valid .json or .pack file.", "warning")
        return redirect(url_for("sync.index"))
        
    try:
        content = file.read().decode("utf-8")
        pack_data = json.loads(content)
        stats = import_curriculum_pack(pack_data)
        
        flash(f"Curriculum Pack imported successfully! Added {stats['subjects_added']} subjects, "
              f"{stats['lessons_added']} lessons, {stats['quizzes_added']} quizzes, {stats['questions_added']} questions.", "success")
    except Exception as e:
        flash(f"Failed to import pack: {str(e)}", "danger")
        
    return redirect(url_for("sync.index"))
