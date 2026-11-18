# Beacon LMS: Offline-First Learning Management System for Rural & Remote Schools

Beacon LMS is a lightweight, resilient, offline-first educational platform purpose-built for rural classrooms, solar-powered computer labs, and remote learning environments with zero or intermittent internet connectivity.

---

## 🌟 Core Rural Education Pillars

1. **100% Offline Progressive Web App (PWA)**:
   - Students download courses onto their phones, tablets, or laptops once over the teacher's local Wi-Fi hotspot.
   - Lessons, notes, audio summaries, and interactive quizzes are stored in browser **IndexedDB**.
   - Students take devices home, read lessons, and complete tests without any cellular data or internet.

2. **Offline Outbox & Auto-Sync**:
   - Quiz submissions and lesson completions performed offline are cryptographically queued in an **Outbox** on the student's device.
   - When the student returns to school and reconnects to the local classroom hub, pending submissions sync automatically in seconds.

3. **Sneakernet USB Synchronization**:
   - In extremely remote villages with no internet uplink whatsoever, teachers can click **"Export School Sync Bundle"** to save encrypted, tamper-evident student records (`.beacon.json`) onto a USB thumb drive.
   - The teacher carries the drive to a district education office or mobile data hotspot.
   - Ministry officials provide new curriculum packs (`.pack.json`) on the same USB drive, which the teacher imports into the local school server with a single click.

4. **Zero Cloud/CDN Dependencies**:
   - All styling, fonts, icons, service workers, and interactive scripts are embedded locally.
   - Runs out-of-the-box on standard Python with built-in SQLite (WAL mode for power cut safety).

5. **Audio-Assisted Learning**:
   - Integrated text-to-speech audio reader summarizes key concepts for auditory learners and students developing reading fluency.

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.8+ (uses Python's standard library + Flask)
- Any modern web browser on student devices (Chrome, Edge, Firefox, Safari, Android Webview)

### 2. Launch the Classroom Hub
```powershell
# From the project root
python run.py
```

The launcher will detect your local network configuration and print:
```text
=================================================================
   BEACON LMS - RURAL OFFLINE LEARNING MANAGEMENT SYSTEM
=================================================================
 * Localhost access:          http://127.0.0.1:5000
 * Classroom Wi-Fi / Hotspot: http://192.168.1.105:5000
=================================================================
```

### 3. Classroom Wi-Fi Hotspot Setup
1. Turn on the Wi-Fi Hotspot on the teacher's laptop or a $20 portable 4G/Wi-Fi router (no SIM card or data plan required!).
2. Have students connect their phones or tablets to the hotspot.
3. Students open their browser and navigate to the IP address shown in the console (e.g., `http://192.168.1.105:5000`).

---

## 📂 Project Architecture

```text
offline/
├── app/
│   ├── config.py              # Directory paths & secret configurations
│   ├── database.py            # SQLite engine with WAL mode & resilient transactions
│   ├── auth.py                # PBKDF2-HMAC password hashing & role access control
│   ├── sync.py                # Sneakernet bundle exporter, importer & batch engine
│   ├── routes/
│   │   ├── auth_routes.py     # Login, registration, session management
│   │   ├── student_routes.py  # Dashboard, lesson reader, quiz interface, offline hub
│   │   ├── teacher_routes.py  # Course authoring, quiz creator, gradebook
│   │   ├── sync_routes.py     # USB Sneakernet management & audit logs
│   │   └── api_routes.py      # PWA curriculum distribution & outbox sync endpoints
│   ├── static/
│   │   ├── css/app.css        # Responsive, mobile-first design (zero external CDNs)
│   │   ├── js/
│   │   │   ├── db.js          # Client-side IndexedDB database manager
│   │   │   ├── sync.js        # Connectivity detection & outbox synchronizer
│   │   │   ├── quiz.js        # Offline interactive quiz runner & auto-grader
│   │   │   └── app.js         # Service Worker registration & PWA installation
│   │   ├── icons/             # Ministry logo and PWA icon sizes
│   │   ├── manifest.json      # Web App Manifest for mobile installation
│   │   └── sw.js              # Service Worker for offline caching
│   └── templates/             # Jinja2 templates (Student, Teacher, Auth components)
├── data/
│   ├── beacon.db              # Portable SQLite database file
│   └── sync_bundles/          # Directory for generated sneakernet packages
├── tests/
│   └── test_beacon.py         # Automated test suite (Auth, Sync, Curriculum, Outbox)
├── sample_curriculum_pack.json# Sample curriculum pack for USB import testing
├── run.py                     # Hotspot auto-detecting server entrypoint
├── seed.py                    # Pre-populates curriculum subjects and lessons
└── seed_ethiopian_curriculum.py # Seeds textbook data and the Grade 11–12 subject catalog
```

---

## 🧪 Running Automated Tests

Run the test suite at any time:
```powershell
python -m unittest tests/test_beacon.py
```
All tests verify zero-network database creation, authentication, PWA curriculum serialization, idempotent offline sync, and cryptographic sneakernet bundle generation.

## Ministry Logo

The UI uses the Ethiopian Ministry of Education logo published on the [Federal Ministry of Justice agency page](https://justice.gov.et/en/entity/ministry-of-education/). Local PNG copies are used so the logo remains available offline.
