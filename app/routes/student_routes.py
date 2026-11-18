import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.auth import login_required
from app.database import db_session

bp = Blueprint("student", __name__, url_prefix="/student")

@bp.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    with db_session() as conn:
        cursor = conn.cursor()
        
        # User details
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = dict(cursor.fetchone())
        
        # Fetch subjects with lesson counts and completion stats
        cursor.execute("""
            SELECT s.id, s.title, s.code, s.grade_level, s.description, s.icon,
                   COUNT(DISTINCT l.id) as total_lessons,
                   COUNT(DISTINCT lc.lesson_id) as completed_lessons
            FROM subjects s
            LEFT JOIN lessons l ON s.id = l.subject_id
            LEFT JOIN lesson_completions lc ON l.id = lc.lesson_id AND lc.student_id = ?
            GROUP BY s.id
            ORDER BY s.title
        """, (user_id,))
        subjects = [dict(row) for row in cursor.fetchall()]
        
        # Calculate percentage per subject
        for s in subjects:
            total = s["total_lessons"]
            done = s["completed_lessons"]
            s["progress_pct"] = round((done / total * 100)) if total > 0 else 0

        # Recent quiz scores
        cursor.execute("""
            SELECT q.title as quiz_title, s.title as subject_title, sub.score, sub.total_points, 
                   sub.percentage, sub.passed, sub.synced_at, sub.submitted_offline
            FROM submissions sub
            JOIN quizzes q ON sub.quiz_id = q.id
            JOIN subjects s ON q.subject_id = s.id
            WHERE sub.student_id = ?
            ORDER BY sub.synced_at DESC LIMIT 5
        """, (user_id,))
        recent_quizzes = [dict(row) for row in cursor.fetchall()]
        
        # Badges & Milestones calculation
        cursor.execute("SELECT COUNT(*) as cnt FROM lesson_completions WHERE student_id = ?", (user_id,))
        total_completed = cursor.fetchone()["cnt"]
        
        cursor.execute("SELECT COUNT(*) as cnt FROM submissions WHERE student_id = ? AND passed = 1", (user_id,))
        passed_quizzes = cursor.fetchone()["cnt"]

    badges = [
        {"name": "First Step", "desc": "Completed first lesson", "icon": "star", "earned": total_completed >= 1},
        {"name": "Bookworm", "desc": "Completed 5 lessons", "icon": "book-open", "earned": total_completed >= 5},
        {"name": "Quiz Master", "desc": "Passed 3 quizzes", "icon": "award", "earned": passed_quizzes >= 3},
        {"name": "Offline Scholar", "desc": "Prepared for offline study", "icon": "download", "earned": True}
    ]

    return render_template("student/dashboard.html", user=user, subjects=subjects, 
                           recent_quizzes=recent_quizzes, badges=badges,
                           total_completed=total_completed)

@bp.route("/subject/<int:subject_id>")
@login_required
def subject_detail(subject_id):
    user_id = session["user_id"]
    with db_session() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,))
        subj = cursor.fetchone()
        if not subj:
            abort(404)
        subject = dict(subj)
        
        # Lessons with completion flag
        cursor.execute("""
            SELECT l.*, 
                   CASE WHEN lc.id IS NOT NULL THEN 1 ELSE 0 END as is_completed,
                   (SELECT COUNT(*) FROM quizzes q WHERE q.lesson_id = l.id) as quiz_count
            FROM lessons l
            LEFT JOIN lesson_completions lc ON l.id = lc.lesson_id AND lc.student_id = ?
            WHERE l.subject_id = ?
            ORDER BY l.order_num, l.id
        """, (user_id, subject_id))
        lessons = [dict(row) for row in cursor.fetchall()]
        
        # Standalone quizzes for this subject
        cursor.execute("""
            SELECT q.*, 
                   (SELECT MAX(percentage) FROM submissions sub WHERE sub.quiz_id = q.id AND sub.student_id = ?) as best_score,
                   (SELECT COUNT(*) FROM questions qst WHERE qst.quiz_id = q.id) as question_count
            FROM quizzes q
            WHERE q.subject_id = ? AND q.lesson_id IS NULL
        """, (user_id, subject_id))
        general_quizzes = [dict(row) for row in cursor.fetchall()]
        
    return render_template("student/course_view.html", subject=subject, lessons=lessons, general_quizzes=general_quizzes)

@bp.route("/lesson/<int:lesson_id>")
@login_required
def lesson_view(lesson_id):
    user_id = session["user_id"]
    with db_session() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT l.*, s.title as subject_title, s.id as subject_id,
                   CASE WHEN lc.id IS NOT NULL THEN 1 ELSE 0 END as is_completed
            FROM lessons l
            JOIN subjects s ON l.subject_id = s.id
            LEFT JOIN lesson_completions lc ON l.id = lc.lesson_id AND lc.student_id = ?
            WHERE l.id = ?
        """, (user_id, lesson_id))
        lesson_row = cursor.fetchone()
        if not lesson_row:
            abort(404)
        lesson = dict(lesson_row)
        
        # Get next and previous lesson
        cursor.execute("""
            SELECT id, title FROM lessons 
            WHERE subject_id = ? AND order_num > ?
            ORDER BY order_num ASC LIMIT 1
        """, (lesson["subject_id"], lesson["order_num"]))
        next_lesson = cursor.fetchone()
        
        cursor.execute("""
            SELECT id, title FROM lessons 
            WHERE subject_id = ? AND order_num < ?
            ORDER BY order_num DESC LIMIT 1
        """, (lesson["subject_id"], lesson["order_num"]))
        prev_lesson = cursor.fetchone()
        
        # Linked quizzes
        cursor.execute("""
            SELECT id, title, passing_score FROM quizzes WHERE lesson_id = ?
        """, (lesson_id,))
        quizzes = [dict(row) for row in cursor.fetchall()]

    return render_template("student/lesson_view.html", lesson=lesson, 
                           next_lesson=dict(next_lesson) if next_lesson else None,
                           prev_lesson=dict(prev_lesson) if prev_lesson else None,
                           quizzes=quizzes)

@bp.route("/quiz/<int:quiz_id>")
@login_required
def quiz_view(quiz_id):
    user_id = session["user_id"]
    with db_session() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT q.*, s.title as subject_title, s.id as subject_id
            FROM quizzes q
            JOIN subjects s ON q.subject_id = s.id
            WHERE q.id = ?
        """, (quiz_id,))
        quiz_row = cursor.fetchone()
        if not quiz_row:
            abort(404)
        quiz = dict(quiz_row)
        
        # Fetch questions
        cursor.execute("""
            SELECT id, question_text, options_json, points, explanation
            FROM questions WHERE quiz_id = ? ORDER BY id
        """, (quiz_id,))
        questions = []
        for row in cursor.fetchall():
            q_dict = dict(row)
            q_dict["options"] = json.loads(q_dict["options_json"])
            questions.append(q_dict)
            
        # Best previous submission
        cursor.execute("""
            SELECT MAX(percentage) as best_pct, MAX(passed) as passed
            FROM submissions WHERE quiz_id = ? AND student_id = ?
        """, (quiz_id, user_id))
        prev_sub = cursor.fetchone()
        best_score = prev_sub["best_pct"] if prev_sub and prev_sub["best_pct"] is not None else None

    return render_template("student/quiz_view.html", quiz=quiz, questions=questions, 
                           best_score=best_score, total_points=sum(q["points"] for q in questions))

@bp.route("/offline-center")
@login_required
def offline_center():
    """PWA hub page for managing downloaded offline packs and outbox sync."""
    return render_template("student/offline_hub.html")
