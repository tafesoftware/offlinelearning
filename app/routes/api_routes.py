import json
from flask import Blueprint, jsonify, request, session
from app.database import db_session
from app.sync import process_client_offline_batch

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/ping", methods=["GET"])
def ping():
    """Lightweight endpoint used by PWA to detect server availability / online state."""
    return jsonify({
        "status": "online",
        "server": "Offline LMS Hub",
        "authenticated": "user_id" in session,
        "user_id": session.get("user_id")
    })

@bp.route("/curriculum", methods=["GET"])
def get_curriculum():
    """
    Returns the complete structured curriculum for client-side offline storage (IndexedDB).
    This allows students to download entire subjects for study without an active connection.
    """
    with db_session() as conn:
        cursor = conn.cursor()
        
        # Fetch all subjects
        cursor.execute("SELECT id, title, code, grade_level, description, icon FROM subjects ORDER BY title")
        subjects = [dict(row) for row in cursor.fetchall()]
        
        # Fetch lessons
        cursor.execute("""
            SELECT id, subject_id, title, order_num, content_markdown, summary, estimated_minutes
            FROM lessons ORDER BY subject_id, order_num
        """)
        all_lessons = [dict(row) for row in cursor.fetchall()]
        
        # Fetch quizzes and questions
        cursor.execute("""
            SELECT id, lesson_id, subject_id, title, description, passing_score
            FROM quizzes ORDER BY subject_id
        """)
        all_quizzes = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("""
            SELECT id, quiz_id, question_text, options_json, correct_option_index, explanation, points
            FROM questions ORDER BY id
        """)
        all_questions = [dict(row) for row in cursor.fetchall()]
        
        # Organize nested hierarchy
        quiz_map = {}
        for qz in all_quizzes:
            qz["questions"] = []
            quiz_map[qz["id"]] = qz
            
        for qst in all_questions:
            qst["options"] = json.loads(qst["options_json"])
            if qst["quiz_id"] in quiz_map:
                quiz_map[qst["quiz_id"]]["questions"].append(qst)
                
        lesson_map = {}
        for lsn in all_lessons:
            lsn["quizzes"] = []
            lesson_map[lsn["id"]] = lsn
            
        for qz in quiz_map.values():
            if qz["lesson_id"] and qz["lesson_id"] in lesson_map:
                lesson_map[qz["lesson_id"]]["quizzes"].append(qz)
                
        subj_map = {s["id"]: s for s in subjects}
        for s in subj_map.values():
            s["lessons"] = []
            
        for lsn in lesson_map.values():
            if lsn["subject_id"] in subj_map:
                subj_map[lsn["subject_id"]]["lessons"].append(lsn)
                
        # If student is logged in, attach their completions and scores
        user_progress = {"completions": [], "scores": []}
        if "user_id" in session:
            uid = session["user_id"]
            cursor.execute("SELECT lesson_id, completed_at FROM lesson_completions WHERE student_id = ?", (uid,))
            user_progress["completions"] = [row["lesson_id"] for row in cursor.fetchall()]
            
            cursor.execute("""
                SELECT quiz_id, MAX(score) as best_score, MAX(percentage) as best_percentage, MAX(passed) as passed
                FROM submissions WHERE student_id = ? GROUP BY quiz_id
            """, (uid,))
            user_progress["scores"] = [dict(row) for row in cursor.fetchall()]

    return jsonify({
        "subjects": list(subj_map.values()),
        "user_progress": user_progress
    })

@bp.route("/sync/push", methods=["POST"])
def sync_push():
    """
    Receives offline outbox data from a client device and saves it idempotently.
    Can be called either with an active session or with user credentials in the payload.
    """
    data = request.get_json(force=True, silent=True) or {}
    user_id = session.get("user_id") or data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "Unauthorized or missing user_id"}), 401
        
    try:
        results = process_client_offline_batch(user_id, data)
        return jsonify({
            "status": "success",
            "message": "Offline data synced successfully",
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/lesson/complete", methods=["POST"])
def mark_lesson_complete():
    """Directly marks a lesson as completed."""
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.get_json(force=True, silent=True) or {}
    lesson_id = data.get("lesson_id")
    if not lesson_id:
        return jsonify({"error": "Missing lesson_id"}), 400
        
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lesson_completions (student_id, lesson_id, submitted_offline)
            VALUES (?, ?, 0)
            ON CONFLICT(student_id, lesson_id) DO NOTHING
        """, (session["user_id"], lesson_id))
        
    return jsonify({"status": "success", "lesson_id": lesson_id})
