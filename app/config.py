import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

UPLOADS_DIR = DATA_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

SYNC_DIR = DATA_DIR / "sync_bundles"
SYNC_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "beacon.db"

class Config:
    SECRET_KEY = os.environ.get("OFFLINE_SECRET_KEY", "offline-rural-lms-super-secret-key-2026")
    DATABASE = str(DB_PATH)
    UPLOADS_DIR = UPLOADS_DIR
    SYNC_DIR = SYNC_DIR
    APP_NAME = "Offline LMS"
    TAGLINE = "Offline-First Learning for Rural & Remote Schools"
    DEFAULT_SCHOOL_NAME = "Mount Hope Rural Primary School"
    VERSION = "1.0.0"
