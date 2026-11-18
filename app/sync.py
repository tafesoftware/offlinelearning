import json
import hashlib
import zipfile
import io
import datetime
from pathlib import Path
from app.config import Config
from app.database import db_session

def generate_export_bundle() -> dict:
    """
    Exports all student submissions, lesson completions, and activity logs
    into a structured sneakernet sync bundle with integrity verification.
    """
    with db_session() as conn:
        cursor = conn.cursor()
        
        # School metadata
        cursor.execute("SELECT key, value FROM school_settings")
        settings = {row["key"]: row["value"] for row in cursor.fetchall()}
        
        # Submissions
        cursor.execute("""
            SELECT s.submission_uuid, s.student_id, u.username as student_username, u.full_name as student_name,
                   s.quiz_id, q.title as quiz_title, s.score, s.total_points, s.percentage, s.passed,
                   s.answers_json, s.submitted_offline, s.client_timestamp, s.synced_at
            FROM submissions s
            JOIN users u ON s.student_id = u.id
            JOIN quizzes q ON s.quiz_id = q.id
            ORDER BY s.synced_at DESC
        """)
        submissions = [dict(row) for row in cursor.fetchall()]
        
        # Lesson completions
        cursor.execute("""
            SELECT lc.student_id, u.username as student_username, lc.lesson_id, l.title as lesson_title,
                   lc.completed_at, lc.submitted_offline
            FROM lesson_completions lc
            JOIN users u ON lc.student_id = u.id
            JOIN lessons l ON lc.lesson_id = l.id
            ORDER BY lc.completed_at DESC
        """)
        completions = [dict(row) for row in cursor.fetchall()]
        
        bundle = {
            "beacon_version": Config.VERSION,
            "export_type": "school_records_sync",
            "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "school_info": settings,
            "counts": {
                "submissions": len(submissions),
                "completions": len(completions)
            },
            "data": {
                "submissions": submissions,
                "completions": completions
            }
        }
        
        # Compute SHA256 checksum of payload
        serialized = json.dumps(bundle, sort_keys=True).encode("utf-8")
        checksum = hashlib.sha256(serialized).hexdigest()
        bundle["sha256_checksum"] = checksum
        
        # Log the export
        cursor.execute("""
            INSERT INTO sync_logs (sync_type, items_synced, status, source_info, log_details)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "sneakernet_export",
            len(submissions) + len(completions),
            "SUCCESS",
            "Teacher Sneakernet USB Export",
            f"Exported {len(submissions)} submissions and {len(completions)} completions. Checksum: {checksum[:8]}..."
        ))
        
        return bundle

def import_curriculum_pack(pack_data: dict) -> dict:
    """
    Imports a curriculum content pack (subjects, lessons, quizzes, questions)
    idempotently into the local SQLite database.
    """
    if "data" not in pack_data or "subjects" not in pack_data["data"]:
        raise ValueError("Invalid curriculum pack structure: missing subjects")
        
    stats = {"subjects_added": 0, "lessons_added": 0, "quizzes_added": 0, "questions_added": 0}
    
    with db_session() as conn:
        cursor = conn.cursor()
        
        for subj in pack_data["data"]["subjects"]:
            # Check if subject exists by code
            cursor.execute("SELECT id FROM subjects WHERE code = ?", (subj["code"],))
            existing_subj = cursor.fetchone()
            
            if existing_subj:
                subject_id = existing_subj["id"]
            else:
                cursor.execute("""
                    INSERT INTO subjects (title, code, grade_level, description, icon)
                    VALUES (?, ?, ?, ?, ?)
                """, (subj["title"], subj["code"], subj["grade_level"], subj.get("description", ""), subj.get("icon", "book")))
                subject_id = cursor.lastrowid
                stats["subjects_added"] += 1
                
            # Import Lessons
            for lesson in subj.get("lessons", []):
                cursor.execute("SELECT id FROM lessons WHERE subject_id = ? AND title = ?", (subject_id, lesson["title"]))
                existing_lesson = cursor.fetchone()
                
                if existing_lesson:
                    lesson_id = existing_lesson["id"]
                    # Update content
                    cursor.execute("""
                        UPDATE lessons SET content_markdown = ?, summary = ?, estimated_minutes = ?
                        WHERE id = ?
                    """, (lesson["content_markdown"], lesson.get("summary", ""), lesson.get("estimated_minutes", 15), lesson_id))
                else:
                    cursor.execute("""
                        INSERT INTO lessons (subject_id, title, order_num, content_markdown, summary, estimated_minutes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (subject_id, lesson["title"], lesson.get("order_num", 1), lesson["content_markdown"], 
                          lesson.get("summary", ""), lesson.get("estimated_minutes", 15)))
                    lesson_id = cursor.lastrowid
                    stats["lessons_added"] += 1
                    
                # Import Quizzes attached to this lesson or subject
                for quiz in lesson.get("quizzes", []):
                    cursor.execute("SELECT id FROM quizzes WHERE subject_id = ? AND title = ?", (subject_id, quiz["title"]))
                    existing_quiz = cursor.fetchone()
                    
                    if existing_quiz:
                        quiz_id = existing_quiz["id"]
                    else:
                        cursor.execute("""
                            INSERT INTO quizzes (lesson_id, subject_id, title, description, passing_score)
                            VALUES (?, ?, ?, ?, ?)
                        """, (lesson_id, subject_id, quiz["title"], quiz.get("description", ""), quiz.get("passing_score", 70)))
                        quiz_id = cursor.lastrowid
                        stats["quizzes_added"] += 1
                        
                    # Import Questions
                    for q in quiz.get("questions", []):
                        cursor.execute("SELECT id FROM questions WHERE quiz_id = ? AND question_text = ?", (quiz_id, q["question_text"]))
                        if not cursor.fetchone():
                            cursor.execute("""
                                INSERT INTO questions (quiz_id, question_text, options_json, correct_option_index, explanation, points)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (quiz_id, q["question_text"], json.dumps(q["options"]), q["correct_option_index"], 
                                  q.get("explanation", ""), q.get("points", 10)))
                            stats["questions_added"] += 1
                            
        cursor.execute("""
            INSERT INTO sync_logs (sync_type, items_synced, status, source_info, log_details)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "sneakernet_import",
            sum(stats.values()),
            "SUCCESS",
            pack_data.get("pack_title", "Curriculum Pack Import"),
            f"Imported: {stats}"
        ))
        
    return stats

def process_client_offline_batch(user_id: int, batch: dict) -> dict:
    """
    Processes offline-queued submissions and completions sent by a student's PWA.
    Ensures idempotency via client-generated UUIDs.
    """
    results = {"synced_submissions": 0, "synced_completions": 0, "errors": []}
    
    with db_session() as conn:
        cursor = conn.cursor()
        
        # 1. Process quiz submissions
        for item in batch.get("submissions", []):
            uuid = item.get("submission_uuid")
            if not uuid:
                continue
                
            cursor.execute("SELECT id FROM submissions WHERE submission_uuid = ?", (uuid,))
            if cursor.fetchone():
                # Already synced before, skip duplicate
                continue
                
            quiz_id = item.get("quiz_id")
            score = item.get("score", 0)
            total = item.get("total_points", 1)
            percentage = round((score / max(total, 1)) * 100, 1)
            passed = 1 if percentage >= item.get("passing_score", 70) else 0
            answers_json = json.dumps(item.get("answers", {}))
            client_time = item.get("client_timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat())
            
            cursor.execute("""
                INSERT INTO submissions (
                    submission_uuid, student_id, quiz_id, score, total_points, 
                    percentage, passed, answers_json, submitted_offline, client_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
            """, (uuid, user_id, quiz_id, score, total, percentage, passed, answers_json, client_time))
            results["synced_submissions"] += 1

        # 2. Process lesson completions
        for comp in batch.get("completions", []):
            lesson_id = comp.get("lesson_id")
            if not lesson_id:
                continue
            cursor.execute("""
                INSERT INTO lesson_completions (student_id, lesson_id, submitted_offline)
                VALUES (?, ?, 1)
                ON CONFLICT(student_id, lesson_id) DO NOTHING
            """, (user_id, lesson_id))
            results["synced_completions"] += 1
            
        cursor.execute("""
            INSERT INTO sync_logs (sync_type, items_synced, status, source_info, log_details)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "client_push",
            results["synced_submissions"] + results["synced_completions"],
            "SUCCESS",
            f"Student User ID {user_id}",
            f"Synced {results['synced_submissions']} submissions and {results['synced_completions']} completions"
        ))
        
    return results
