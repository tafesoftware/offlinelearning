import unittest
import json
import os
import sqlite3
import tempfile
from app import create_app
from app.config import Config
from app.database import db_session, init_db
from app.sync import generate_export_bundle, import_curriculum_pack, process_client_offline_batch
from seed import seed_data
from seed_ethiopian_curriculum import seed_grade_11_12_subject_catalog

class BeaconLMSTestCase(unittest.TestCase):
    def setUp(self):
        self.original_database = Config.DATABASE
        self.test_database = os.path.join(tempfile.gettempdir(), f"beacon_test_{os.urandom(8).hex()}.db")
        Config.DATABASE = self.test_database
        seed_data()
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        Config.DATABASE = self.original_database
        for suffix in ("", "-wal", "-shm"):
            path = self.test_database + suffix
            if os.path.exists(path):
                os.remove(path)

    def test_database_seeded(self):
        """Verify curriculum is seeded without demo users or learner activity."""
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM users")
            user_count = cursor.fetchone()["cnt"]
            self.assertEqual(user_count, 0)

            cursor.execute("SELECT COUNT(*) as cnt FROM subjects")
            subj_count = cursor.fetchone()["cnt"]
            self.assertGreaterEqual(subj_count, 4)

            cursor.execute("SELECT COUNT(*) as cnt FROM lessons")
            lesson_count = cursor.fetchone()["cnt"]
            self.assertGreaterEqual(lesson_count, 4)

            cursor.execute("SELECT COUNT(*) as cnt FROM submissions")
            self.assertEqual(cursor.fetchone()["cnt"], 0)

            cursor.execute("SELECT COUNT(*) as cnt FROM lesson_completions")
            self.assertEqual(cursor.fetchone()["cnt"], 0)

    def test_curriculum_seeds_when_users_already_exist(self):
        """Registered users must not prevent curriculum seeding."""
        original_database = Config.DATABASE
        test_database = os.path.join(tempfile.gettempdir(), f"beacon_user_test_{os.urandom(8).hex()}.db")
        try:
            Config.DATABASE = test_database
            init_db()
            with db_session() as conn:
                conn.execute("""
                    INSERT INTO users (username, password_hash, full_name, role)
                    VALUES (?, ?, ?, ?)
                """, ("school_user", "test-hash", "School User", "teacher"))

            seed_data()

            with db_session() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as cnt FROM users")
                self.assertEqual(cursor.fetchone()["cnt"], 1)
                cursor.execute("SELECT COUNT(*) as cnt FROM subjects")
                self.assertGreaterEqual(cursor.fetchone()["cnt"], 4)
        finally:
            Config.DATABASE = original_database
            for suffix in ("", "-wal", "-shm"):
                path = test_database + suffix
                if os.path.exists(path):
                    os.remove(path)

    def test_grade_levels_are_sorted_ascending(self):
        registration = self.client.get("/auth/register")
        option_positions = [
            registration.data.index(f'value="Grade {grade}"'.encode())
            for grade in range(5, 13)
        ]
        self.assertEqual(option_positions, sorted(option_positions))
        self.assertNotIn(b'value="Grade 4"', registration.data)

        with db_session() as conn:
            for grade in (10, 4, 9, 5):
                conn.execute("""
                    INSERT INTO textbooks (title, subject_code, grade_level)
                    VALUES (?, ?, ?)
                """, (f"Grade {grade} Book", f"TEST-{grade}", f"Grade {grade}"))

        with self.client.session_transaction() as user_session:
            user_session["user_id"] = 1
        library = self.client.get("/library/")
        book_positions = [
            library.data.index(f"Grade {grade} Book".encode())
            for grade in (4, 5, 9, 10)
        ]
        self.assertEqual(book_positions, sorted(book_positions))

    def test_public_information_pages(self):
        home = self.client.get("/home")
        self.assertEqual(home.status_code, 200)
        self.assertIn(b"Welcome to Offline LMS", home.data)

        pages = {
            "/contact": b"Contact Us",
            "/location": b"Mount Hope Rural Primary School",
            "/about": b"About System",
        }
        for path, expected_text in pages.items():
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(expected_text, response.data)

    def test_language_selection_persists_across_pages(self):
        english_home = self.client.get("/home")
        self.assertIn(b'<html lang="en">', english_home.data)

        response = self.client.post(
            "/language",
            data={"language": "am", "next": "/home"},
        )
        self.assertEqual(response.status_code, 302)
        amharic_home = self.client.get("/home")
        self.assertIn(b'<html lang="am">', amharic_home.data)
        self.assertIn(b"i18n.js", amharic_home.data)
        self.assertIn(b'name="language" value="am" lang="am" aria-pressed="true"', amharic_home.data)

        amharic_login = self.client.get("/auth/login")
        self.assertIn(b'<html lang="am">', amharic_login.data)

        response = self.client.post(
            "/language",
            data={"language": "en", "next": "/auth/login"},
        )
        self.assertEqual(response.status_code, 302)
        english_login = self.client.get("/auth/login")
        self.assertIn(b'<html lang="en">', english_login.data)

        invalid_language = self.client.post(
            "/language",
            data={"language": "fr", "next": "/home"},
        )
        self.assertEqual(invalid_language.status_code, 400)

    def test_registration_streams_and_subject_preview(self):
        seed_grade_11_12_subject_catalog()
        registration = self.client.get("/auth/register")
        self.assertIn(b'id="stream"', registration.data)
        self.assertIn(
            '<option value="" selected disabled>Grade / ክፍል</option>'.encode(),
            registration.data,
        )
        self.assertIn("አዲስ መለያ ይፍጠሩ".encode(), registration.data)
        self.assertIn("መነሻ".encode(), registration.data)
        self.assertIn("የገጠር እና ሩቅ ትምህርት ቤቶች".encode(), registration.data)
        self.assertIn(b"Biology", registration.data)
        self.assertIn(b"Geography", registration.data)
        self.assertNotIn(b"Student Textbook", registration.data)
        self.assertNotIn("መነሻ".encode(), self.client.get("/auth/login").data)

        registrations = (
            ("grade11_student", "student", "Grade 11", "Social Science", "Grade 11", "Social Science"),
            ("grade12_teacher", "teacher", "Grade 12", "Natural Science", "General", None),
        )
        for username, role, grade, stream, expected_grade, expected_stream in registrations:
            response = self.client.post("/auth/register", data={
                "first_name": "Test",
                "last_name": username,
                "username": username,
                "password": "test-password",
                "role": role,
                "grade_level": grade,
                "stream": stream,
            })
            self.assertEqual(response.status_code, 302)
            with db_session() as conn:
                user = conn.execute(
                    "SELECT grade_level, stream FROM users WHERE username = ?",
                    (username,),
                ).fetchone()
                self.assertEqual(user["grade_level"], expected_grade)
                self.assertEqual(user["stream"], expected_stream)

        response = self.client.post("/auth/register", data={
            "first_name": "Missing",
            "last_name": "Stream",
            "username": "missing_stream",
            "password": "test-password",
            "role": "student",
            "grade_level": "Grade 11",
        })
        self.assertEqual(response.status_code, 200)
        with db_session() as conn:
            user = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                ("missing_stream",),
            ).fetchone()
            self.assertIsNone(user)

        response = self.client.post("/auth/register", data={
            "first_name": "Missing",
            "last_name": "Grade",
            "username": "missing_grade",
            "password": "test-password",
            "role": "student",
        })
        self.assertEqual(response.status_code, 200)
        with db_session() as conn:
            user = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                ("missing_grade",),
            ).fetchone()
            self.assertIsNone(user)

        response = self.client.post("/auth/register", data={
            "first_name": "Invalid",
            "last_name": "Grade",
            "username": "grade_four",
            "password": "test-password",
            "role": "student",
            "grade_level": "Grade 4",
        })
        self.assertEqual(response.status_code, 200)
        with db_session() as conn:
            user = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                ("grade_four",),
            ).fetchone()
            self.assertIsNone(user)

    def test_database_adds_stream_to_existing_users_table(self):
        original_database = Config.DATABASE
        test_database = os.path.join(tempfile.gettempdir(), f"beacon_migration_test_{os.urandom(8).hex()}.db")
        try:
            Config.DATABASE = test_database
            conn = sqlite3.connect(test_database)
            try:
                conn.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        role TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student')),
                        grade_level TEXT DEFAULT 'General',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            finally:
                conn.close()

            init_db()

            with db_session() as conn:
                columns = {
                    row["name"] for row in conn.execute("PRAGMA table_info(users)")
                }
                self.assertIn("stream", columns)
        finally:
            Config.DATABASE = original_database
            for suffix in ("", "-wal", "-shm"):
                path = test_database + suffix
                if os.path.exists(path):
                    os.remove(path)

    def test_grade_11_12_subject_catalog(self):
        seed_grade_11_12_subject_catalog()

        expected = {
            ("Grade 11", "Natural Science"): {
                "MATH-11-NS", "PHYS-11", "CHEM-11", "BIOL-11", "IT-11",
            },
            ("Grade 11", "Social Science"): {
                "MATH-11-SS", "GEOG-11", "HIST-11", "ECON-11", "CITZ-11",
            },
            ("Grade 11", "Common"): {"ENG-11"},
            ("Grade 12", "Natural Science"): {
                "MATH-12-NS", "PHYS-12", "CHEM-12", "BIOL-12",
            },
            ("Grade 12", "Social Science"): {
                "MATH-12-SS", "GEOG-12", "HIST-12", "ECON-12", "CITZ-12",
            },
            ("Grade 12", "Common"): {"ENG-12"},
        }
        with db_session() as conn:
            rows = conn.execute("""
                SELECT grade_level, stream, subject_code, file_path
                FROM textbooks
                WHERE grade_level IN ('Grade 11', 'Grade 12')
            """).fetchall()
            catalog = {}
            for row in rows:
                catalog.setdefault((row["grade_level"], row["stream"]), set()).add(row["subject_code"])
                self.assertIsNone(row["file_path"])
            self.assertEqual(catalog, expected)

        with self.client.session_transaction() as user_session:
            user_session["user_id"] = 1
        response = self.client.get("/library/?grade=Grade%2011&stream=Social%20Science")
        self.assertEqual(response.status_code, 200)
        for code in expected[("Grade 11", "Social Science")] | {"ENG-11"}:
            self.assertIn(code.encode(), response.data)
        self.assertIn(b"Subject listing - content not uploaded", response.data)
        self.assertNotIn(b"Read Book", response.data)

        all_subjects = self.client.get("/library/?grade=all&stream=all")
        section_labels = [
            "Grade 11 - Natural Science",
            "Grade 11 - Social Science",
            "Grade 11 - Common Subjects",
            "Grade 12 - Natural Science",
            "Grade 12 - Social Science",
            "Grade 12 - Common Subjects",
        ]
        section_positions = [all_subjects.data.index(label.encode()) for label in section_labels]
        self.assertEqual(section_positions, sorted(section_positions))

        with self.client.session_transaction() as user_session:
            user_session["role"] = "teacher"
        upload = self.client.post("/library/upload", data={
            "title": "Grade 11 Social Mathematics",
            "subject_code": "MATH-11-SS",
            "grade_level": "Grade 11",
            "stream": "Social Science",
            "publisher": "School Library",
            "description": "Uploaded course material",
        }, follow_redirects=True)
        self.assertEqual(upload.status_code, 200)
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) AS cnt FROM textbooks
                WHERE subject_code = ? AND grade_level = ?
            """, ("MATH-11-SS", "Grade 11"))
            self.assertEqual(cursor.fetchone()["cnt"], 1)
            cursor.execute("SELECT title FROM subjects WHERE code = ?", ("MATH-11-SS",))
            self.assertEqual(cursor.fetchone()["title"], "Grade 11 Social Mathematics")

    def test_auth_registration_with_firstname_lastname(self):
        """Test registration using separate first_name and last_name fields."""
        uname = f"testuser_{os.urandom(3).hex()}"
        res = self.client.post("/auth/register", data={
            "first_name": "Almaz",
            "last_name": "Bekele",
            "username": uname,
            "role": "student",
            "grade_level": "Grade 9",
            "password": "pass123"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Account registered successfully", res.data)

        # Verify saved full_name in db
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT full_name FROM users WHERE username = ?", (uname,))
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["full_name"], "Almaz Bekele")

    def test_auth_login(self):
        """Demo accounts are absent, while newly registered users can log in."""
        res = self.client.post("/auth/login", data={"username": "student1", "password": "wrongpassword"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Invalid username or password", res.data)

        username = f"loginuser_{os.urandom(3).hex()}"
        self.client.post("/auth/register", data={
            "first_name": "Samuel",
            "last_name": "Kiptoo",
            "username": username,
            "role": "student",
            "grade_level": "Grade 5",
            "password": "user-password"
        })
        res = self.client.post("/auth/login", data={
            "username": username,
            "password": "user-password"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Samuel Kiptoo", res.data)
        self.assertIn(b"My Courses", res.data)

    def test_api_curriculum_offline_cache(self):
        """Verify that the API curriculum endpoint returns full course structure for IndexedDB caching."""
        res = self.client.get("/api/curriculum")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("subjects", data)
        self.assertGreater(len(data["subjects"]), 0)
        
        # Verify nested lessons and quizzes
        first_subject = data["subjects"][0]
        self.assertIn("lessons", first_subject)
        self.assertIn("title", first_subject)

    def test_api_sync_push_offline_queue(self):
        """Verify client-side offline outbox sync with idempotent submission."""
        username = f"syncuser_{os.urandom(3).hex()}"
        self.client.post("/auth/register", data={
            "first_name": "Test",
            "last_name": "Student",
            "username": username,
            "role": "student",
            "grade_level": "Grade 5",
            "password": "user-password"
        })
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            student_id = cursor.fetchone()["id"]

        test_uuid = f"test_offline_sub_{os.urandom(4).hex()}"
        batch = {
            "submissions": [
                {
                    "submission_uuid": test_uuid,
                    "quiz_id": 1,
                    "score": 30,
                    "total_points": 40,
                    "passing_score": 70,
                    "answers": {"1": 1, "2": 0},
                    "client_timestamp": "2026-11-18T06:00:00Z"
                }
            ],
            "completions": [
                {
                    "lesson_id": 2,
                    "client_timestamp": "2026-11-18T06:05:00Z"
                }
            ]
        }
        
        res = process_client_offline_batch(student_id, batch)
        self.assertEqual(res["synced_submissions"], 1)
        self.assertEqual(res["synced_completions"], 1)

        # Try to sync the same UUID again -> must be skipped (idempotent, no duplicates)
        res_duplicate = process_client_offline_batch(student_id, batch)
        self.assertEqual(res_duplicate["synced_submissions"], 0)

    def test_sneakernet_export_and_import(self):
        """Test Sneakernet USB export bundle creation and curriculum pack import."""
        # 1. Export bundle
        bundle = generate_export_bundle()
        self.assertIn("sha256_checksum", bundle)
        self.assertIn("data", bundle)
        self.assertIn("submissions", bundle["data"])
        self.assertEqual(len(bundle["data"]["submissions"]), 0)

        # 2. Test importing a curriculum pack
        unique_code = f"HLT-TEST-{os.urandom(3).hex().upper()}"
        sample_pack = {
            "pack_title": "Primary Health & Hygiene Pack",
            "beacon_version": "1.0.0",
            "data": {
                "subjects": [
                    {
                        "title": "Community Health & First Aid",
                        "code": unique_code,
                        "grade_level": "Grade 4",
                        "description": "Basic hygiene, wound dressing, and malaria prevention.",
                        "lessons": [
                            {
                                "title": "Preventing Malaria with Bed Nets",
                                "order_num": 1,
                                "content_markdown": "# Malaria Prevention\n\nSleep under treated nets every night.",
                                "summary": "Use insecticide-treated mosquito nets to prevent malaria infection.",
                                "estimated_minutes": 10,
                                "quizzes": [
                                    {
                                        "title": "Mosquito Protection Quiz",
                                        "passing_score": 70,
                                        "questions": [
                                            {
                                                "question_text": "What is the best way to prevent mosquito bites while sleeping?",
                                                "options": ["Sleeping outside", "Using an insecticide-treated bed net", "Leaving lights on", "Drinking cold water"],
                                                "correct_option_index": 1,
                                                "explanation": "Treated nets physically block and repel Anopheles mosquitoes.",
                                                "points": 10
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }

        stats = import_curriculum_pack(sample_pack)
        self.assertEqual(stats["subjects_added"], 1)
        self.assertEqual(stats["lessons_added"], 1)
        self.assertEqual(stats["quizzes_added"], 1)
        self.assertEqual(stats["questions_added"], 1)

if __name__ == "__main__":
    unittest.main()
