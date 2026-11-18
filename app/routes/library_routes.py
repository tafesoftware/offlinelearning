import os
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, abort, session
from werkzeug.utils import secure_filename
from app.config import Config
from app.auth import login_required, teacher_required
from app.database import db_session

bp = Blueprint("library", __name__, url_prefix="/library")

@bp.route("/")
@login_required
def index():
    grade_filter = request.args.get("grade", "all")
    stream_filter = request.args.get("stream", "all")
    search_query = request.args.get("q", "").strip()

    with db_session() as conn:
        cursor = conn.cursor()
        
        query = """
            SELECT t.*,
                   EXISTS (
                       SELECT 1
                       FROM subjects s
                       JOIN lessons l ON l.subject_id = s.id
                       WHERE s.code = t.subject_code AND s.grade_level = t.grade_level
                   ) AS has_lessons
            FROM textbooks t
            WHERE 1=1
        """
        params = []

        if grade_filter != "all":
            query += " AND t.grade_level = ?"
            params.append(grade_filter)

        if stream_filter != "all":
            query += " AND (t.stream = ? OR t.stream = 'Common')"
            params.append(stream_filter)

        if search_query:
            query += " AND (t.title LIKE ? OR t.subject_code LIKE ? OR t.description LIKE ?)"
            wildcard = f"%{search_query}%"
            params.extend([wildcard, wildcard, wildcard])

        query += """
            ORDER BY
                CASE WHEN t.grade_level GLOB 'Grade [0-9]*'
                     THEN CAST(SUBSTR(t.grade_level, 7) AS INTEGER)
                     ELSE 2147483647
                END ASC,
                CASE t.stream
                    WHEN 'Natural Science' THEN 0
                    WHEN 'Social Science' THEN 1
                    ELSE 2
                END ASC,
                t.grade_level ASC, t.stream ASC, t.title ASC
        """
        cursor.execute(query, params)
        books = [dict(row) for row in cursor.fetchall()]

        grouped_books = {}
        for book in books:
            key = (book["grade_level"], book["stream"])
            grouped_books.setdefault(key, []).append(book)

        book_groups = [
            {
                "grade_level": grade,
                "stream_label": "Common Subjects" if stream == "Common" else stream,
                "books": grouped_books[(grade, stream)],
            }
            for grade, stream in grouped_books
        ]

        # Statistics
        cursor.execute("""
            SELECT COUNT(*) as cnt
            FROM textbooks t
            WHERE t.file_path IS NOT NULL
               OR EXISTS (
                    SELECT 1
                    FROM subjects s
                    JOIN lessons l ON l.subject_id = s.id
                    WHERE s.code = t.subject_code AND s.grade_level = t.grade_level
               )
        """)
        total_books = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(DISTINCT grade_level) as cnt FROM textbooks")
        total_grades = cursor.fetchone()["cnt"]

        cursor.execute("SELECT SUM(download_count) as cnt FROM textbooks")
        total_downloads = cursor.fetchone()["cnt"] or 0

    return render_template("library/index.html", 
                           book_groups=book_groups,
                           grade_filter=grade_filter, 
                           stream_filter=stream_filter, 
                           search_query=search_query,
                           total_books=total_books,
                           total_grades=total_grades,
                           total_downloads=total_downloads)

@bp.route("/book/<int:book_id>/download")
@login_required
def download_book(book_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM textbooks WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if not row:
            abort(404)
        book = dict(row)

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM subjects s
                JOIN lessons l ON l.subject_id = s.id
                WHERE s.code = ? AND s.grade_level = ?
            ) AS has_lessons
        """, (book["subject_code"], book["grade_level"]))
        if not book.get("file_path") and not cursor.fetchone()["has_lessons"]:
            flash("This subject is listed in the catalog, but its textbook or lessons are not available yet.", "info")
            return redirect(url_for("library.index"))

        # Increment download counter
        cursor.execute("UPDATE textbooks SET download_count = download_count + 1 WHERE id = ?", (book_id,))

    file_name = book.get("file_path")
    if file_name and os.path.exists(os.path.join(Config.UPLOADS_DIR, file_name)):
        return send_from_directory(
            Config.UPLOADS_DIR, 
            file_name, 
            as_attachment=True, 
            download_name=f"{book['subject_code']}_{book['grade_level'].replace(' ', '_')}_Textbook.pdf"
        )
    else:
        # If specific PDF file isn't uploaded yet, redirect to interactive offline reader
        flash(f"Serving offline digital edition for {book['title']}.", "info")
        return redirect(url_for("library.reader", book_id=book_id))

@bp.route("/book/<int:book_id>/reader")
@login_required
def reader(book_id):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM textbooks WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if not row:
            abort(404)
        book = dict(row)

        # Check if subject exists in the main LMS to link related quizzes and lessons
        cursor.execute("SELECT id, title FROM subjects WHERE code = ?", (book["subject_code"],))
        linked_subject = cursor.fetchone()

        lessons = []
        if linked_subject:
            cursor.execute("SELECT id, title, order_num, estimated_minutes, summary, content_markdown FROM lessons WHERE subject_id = ? ORDER BY order_num", (linked_subject["id"],))
            lessons = [dict(l) for l in cursor.fetchall()]

    if not book.get("file_path") and not lessons:
        flash("This subject is listed in the catalog, but its textbook or lessons are not available yet.", "info")
        return redirect(url_for("library.index"))

    return render_template("library/reader.html", 
                           book=book, 
                           linked_subject=dict(linked_subject) if linked_subject else None,
                           lessons=lessons)

@bp.route("/upload", methods=["GET", "POST"])
@teacher_required
def upload_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject_code = request.form.get("subject_code", "").strip().upper()
        grade_level = request.form.get("grade_level", "Grade 9")
        stream = request.form.get("stream", "Common")
        publisher = request.form.get("publisher", "Ministry of Education (MoE) Ethiopia")
        description = request.form.get("description", "").strip()

        file = request.files.get("book_file")
        saved_filename = None
        file_size_mb = 0.0

        if file and file.filename != "":
            raw_filename = secure_filename(file.filename)
            saved_filename = f"{subject_code}_{grade_level.replace(' ', '_')}_{raw_filename}"
            target_path = os.path.join(Config.UPLOADS_DIR, saved_filename)
            file.save(target_path)
            file_size_mb = round(os.path.getsize(target_path) / (1024 * 1024), 2)

        if not title or not subject_code:
            flash("Book title and subject code are required.", "warning")
            return render_template("library/upload.html")

        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM textbooks WHERE subject_code = ? AND grade_level = ? ORDER BY id LIMIT 1",
                (subject_code, grade_level),
            )
            existing_book = cursor.fetchone()
            if existing_book:
                cursor.execute("""
                    UPDATE textbooks
                    SET title = ?, stream = ?, publisher = ?, description = ?,
                        file_path = ?, file_size_mb = ?
                    WHERE id = ?
                """, (title, stream, publisher, description, saved_filename, file_size_mb, existing_book["id"]))
            else:
                cursor.execute("""
                    INSERT INTO textbooks (
                        title, subject_code, grade_level, stream, publisher,
                        description, file_path, file_size_mb
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (title, subject_code, grade_level, stream, publisher, description, saved_filename, file_size_mb))

            cursor.execute("SELECT id FROM subjects WHERE code = ?", (subject_code,))
            existing_subject = cursor.fetchone()
            if existing_subject:
                cursor.execute("""
                    UPDATE subjects SET title = ?, grade_level = ?, description = ?
                    WHERE id = ?
                """, (title, grade_level, description, existing_subject["id"]))
            else:
                cursor.execute("""
                    INSERT INTO subjects (title, code, grade_level, description, icon, created_by)
                    VALUES (?, ?, ?, ?, 'book', ?)
                """, (title, subject_code, grade_level, description, session["user_id"]))

        flash(f"Textbook '{title}' registered successfully in the Ethiopian Digital Library!", "success")
        return redirect(url_for("library.index"))

    return render_template("library/upload.html")
