import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.auth import teacher_required
from app.database import db_session

bp = Blueprint("teacher", __name__, url_prefix="/teacher")

@bp.route("/dashboard")
@teacher_required
def dashboard():
    with db_session() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as cnt FROM users WHERE role = 'student'")
        student_count = cursor.fetchone()["cnt"]
        
        cursor.execute("SELECT COUNT(*) as cnt FROM subjects")
        subject_count = cursor.fetchone()["cnt"]
        
        cursor.execute("SELECT COUNT(*) as cnt FROM lessons")
        lesson_count = cursor.fetchone()["cnt"]
        
        cursor.execute("SELECT COUNT(*) as cnt FROM submissions")
        submission_count = cursor.fetchone()["cnt"]
        
        # Recent submissions
        cursor.execute("""
            SELECT s.id, u.full_name as student_name, q.title as quiz_title, 
                   s.score, s.total_points, s.percentage, s.passed, s.submitted_offline, s.synced_at
            FROM submissions s
            JOIN users u ON s.student_id = u.id
            JOIN quizzes q ON s.quiz_id = q.id
            ORDER BY s.synced_at DESC LIMIT 6
        """)
        recent_submissions = [dict(row) for row in cursor.fetchall()]
        
        # Subjects list
        cursor.execute("""
            SELECT s.*, 
                   (SELECT COUNT(*) FROM lessons l WHERE l.subject_id = s.id) as lesson_count,
                   (SELECT COUNT(*) FROM quizzes q WHERE q.subject_id = s.id) as quiz_count
            FROM subjects s ORDER BY s.title
        """)
        subjects = [dict(row) for row in cursor.fetchall()]

    return render_template("teacher/dashboard.html", 
                           student_count=student_count, 
                           subject_count=subject_count,
                           lesson_count=lesson_count, 
                           submission_count=submission_count,
                           recent_submissions=recent_submissions,
                           subjects=subjects)

@bp.route("/subject/new", methods=["GET", "POST"])
@teacher_required
def new_subject():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        code = request.form.get("code", "").strip().upper()
        grade_level = request.form.get("grade_level", "General")
        description = request.form.get("description", "").strip()
        icon = request.form.get("icon", "book")
        
        if not title or not code:
            flash("Title and Subject Code are required.", "warning")
            return render_template("teacher/course_manage.html")
            
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM subjects WHERE code = ?", (code,))
            if cursor.fetchone():
                flash("Subject Code already exists. Please choose a unique code.", "danger")
                return render_template("teacher/course_manage.html")
                
            cursor.execute("""
                INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, code, grade_level, description, icon, session["user_id"]))
            
        flash(f"Subject '{title}' created successfully!", "success")
        return redirect(url_for("teacher.dashboard"))
        
    return render_template("teacher/course_manage.html")

@bp.route("/subject/<int:subject_id>/lesson/new", methods=["GET", "POST"])
@teacher_required
def new_lesson(subject_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,))
        subject = cursor.fetchone()
        if not subject:
            abort(404)
            
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            order_num = int(request.form.get("order_num", 1))
            estimated_minutes = int(request.form.get("estimated_minutes", 15))
            summary = request.form.get("summary", "").strip()
            content = request.form.get("content_markdown", "").strip()
            
            if not title or not content:
                flash("Title and Lesson Content are required.", "warning")
                return render_template("teacher/lesson_edit.html", subject=dict(subject), lesson=None)
                
            cursor.execute("""
                INSERT INTO lessons (subject_id, title, order_num, content_markdown, summary, estimated_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (subject_id, title, order_num, content, summary, estimated_minutes))
            
            flash(f"Lesson '{title}' created successfully!", "success")
            return redirect(url_for("student.subject_detail", subject_id=subject_id))
            
    return render_template("teacher/lesson_edit.html", subject=dict(subject), lesson=None)

@bp.route("/lesson/<int:lesson_id>/edit", methods=["GET", "POST"])
@teacher_required
def edit_lesson(lesson_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT l.*, s.title as subject_title FROM lessons l JOIN subjects s ON l.subject_id = s.id WHERE l.id = ?", (lesson_id,))
        row = cursor.fetchone()
        if not row:
            abort(404)
        lesson = dict(row)
        
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            order_num = int(request.form.get("order_num", 1))
            estimated_minutes = int(request.form.get("estimated_minutes", 15))
            summary = request.form.get("summary", "").strip()
            content = request.form.get("content_markdown", "").strip()
            
            cursor.execute("""
                UPDATE lessons SET title = ?, order_num = ?, estimated_minutes = ?, summary = ?, content_markdown = ?
                WHERE id = ?
            """, (title, order_num, estimated_minutes, summary, content, lesson_id))
            
            flash(f"Lesson '{title}' updated successfully!", "success")
            return redirect(url_for("student.lesson_view", lesson_id=lesson_id))
            
    return render_template("teacher/lesson_edit.html", subject={"id": lesson["subject_id"], "title": lesson["subject_title"]}, lesson=lesson)

@bp.route("/subject/<int:subject_id>/quiz/new", methods=["GET", "POST"])
@teacher_required
def new_quiz(subject_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,))
        subject = cursor.fetchone()
        if not subject:
            abort(404)
            
        cursor.execute("SELECT id, title FROM lessons WHERE subject_id = ? ORDER BY order_num", (subject_id,))
        lessons = [dict(r) for r in cursor.fetchall()]
        
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            lesson_id = request.form.get("lesson_id") or None
            description = request.form.get("description", "").strip()
            passing_score = int(request.form.get("passing_score", 70))
            
            # Read dynamic questions
            q_texts = request.form.getlist("question_text[]")
            q_opt_a = request.form.getlist("option_a[]")
            q_opt_b = request.form.getlist("option_b[]")
            q_opt_c = request.form.getlist("option_c[]")
            q_opt_d = request.form.getlist("option_d[]")
            q_correct = request.form.getlist("correct_option[]")
            q_expl = request.form.getlist("explanation[]")
            
            cursor.execute("""
                INSERT INTO quizzes (lesson_id, subject_id, title, description, passing_score)
                VALUES (?, ?, ?, ?, ?)
            """, (lesson_id, subject_id, title, description, passing_score))
            quiz_id = cursor.lastrowid
            
            for i in range(len(q_texts)):
                if q_texts[i].strip():
                    opts = [q_opt_a[i].strip(), q_opt_b[i].strip(), q_opt_c[i].strip(), q_opt_d[i].strip()]
                    corr_idx = int(q_correct[i]) if i < len(q_correct) else 0
                    expl = q_expl[i].strip() if i < len(q_expl) else ""
                    cursor.execute("""
                        INSERT INTO questions (quiz_id, question_text, options_json, correct_option_index, explanation)
                        VALUES (?, ?, ?, ?, ?)
                    """, (quiz_id, q_texts[i].strip(), json.dumps(opts), corr_idx, expl))
                    
            flash(f"Quiz '{title}' and question bank created!", "success")
            return redirect(url_for("student.subject_detail", subject_id=subject_id))
            
    return render_template("teacher/quiz_edit.html", subject=dict(subject), lessons=lessons)

@bp.route("/gradebook")
@teacher_required
def gradebook():
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, u.full_name as student_name, u.username as student_username, u.grade_level,
                   subj.title as subject_title, q.title as quiz_title, 
                   s.score, s.total_points, s.percentage, s.passed, s.submitted_offline, 
                   s.client_timestamp, s.synced_at
            FROM submissions s
            JOIN users u ON s.student_id = u.id
            JOIN quizzes q ON s.quiz_id = q.id
            JOIN subjects subj ON q.subject_id = subj.id
            ORDER BY s.synced_at DESC
        """)
        submissions = [dict(row) for row in cursor.fetchall()]
        
    return render_template("teacher/gradebook.html", submissions=submissions)
