import sqlite3
import os
from contextlib import contextmanager
from app.config import Config

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student')),
    grade_level TEXT DEFAULT 'General',
    stream TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    grade_level TEXT NOT NULL,
    description TEXT,
    icon TEXT DEFAULT 'book',
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    order_num INTEGER DEFAULT 1,
    content_markdown TEXT NOT NULL,
    summary TEXT,
    estimated_minutes INTEGER DEFAULT 15,
    has_audio_guide INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER,
    subject_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    passing_score INTEGER DEFAULT 70,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(lesson_id) REFERENCES lessons(id) ON DELETE SET NULL,
    FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    options_json TEXT NOT NULL, -- JSON array of strings e.g. ["Option A", "Option B", ...]
    correct_option_index INTEGER NOT NULL, -- 0-indexed
    explanation TEXT,
    points INTEGER DEFAULT 10,
    FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_uuid TEXT UNIQUE NOT NULL, -- For client-generated offline UUIDs
    student_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total_points INTEGER NOT NULL,
    percentage REAL NOT NULL,
    passed INTEGER NOT NULL,
    answers_json TEXT NOT NULL,
    submitted_offline INTEGER DEFAULT 0,
    client_timestamp TIMESTAMP,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lesson_completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    lesson_id INTEGER NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_offline INTEGER DEFAULT 0,
    UNIQUE(student_id, lesson_id),
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sync_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_type TEXT NOT NULL CHECK(sync_type IN ('client_push', 'sneakernet_import', 'sneakernet_export', 'cloud_pull')),
    items_synced INTEGER DEFAULT 0,
    status TEXT NOT NULL,
    source_info TEXT,
    log_details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS school_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS textbooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject_code TEXT NOT NULL,
    grade_level TEXT NOT NULL,
    stream TEXT DEFAULT 'Common',
    publisher TEXT DEFAULT 'Ministry of Education (MoE) Ethiopia',
    curriculum_type TEXT DEFAULT 'New Ethiopian Curriculum',
    edition_year TEXT DEFAULT '2023/2024 Revised Edition',
    description TEXT,
    file_path TEXT,
    file_type TEXT DEFAULT 'PDF',
    file_size_mb REAL DEFAULT 0.0,
    is_available_offline INTEGER DEFAULT 1,
    cover_badge_color TEXT DEFAULT 'primary',
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def get_connection():
    conn = sqlite3.connect(Config.DATABASE, timeout=15.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

@contextmanager
def db_session():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with db_session() as conn:
        conn.executescript(SCHEMA_SQL)
        # Seed default school settings if not present
        cursor = conn.cursor()
        user_columns = {row["name"] for row in cursor.execute("PRAGMA table_info(users)")}
        if "stream" not in user_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN stream TEXT")

        cursor.execute("SELECT COUNT(*) as cnt FROM school_settings")
        if cursor.fetchone()["cnt"] == 0:
            cursor.execute("INSERT INTO school_settings (key, value) VALUES (?, ?)", 
                           ("school_name", Config.DEFAULT_SCHOOL_NAME))
            cursor.execute("INSERT INTO school_settings (key, value) VALUES (?, ?)", 
                           ("district", "Valley North Rural District"))
            cursor.execute("INSERT INTO school_settings (key, value) VALUES (?, ?)", 
                           ("last_sync_date", "Never"))
