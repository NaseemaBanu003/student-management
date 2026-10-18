import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "edu-manage-pro-development-secret-key-2026-strong-")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "edu-manage-pro-jwt-secret-key-2026-strong-32b")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "edu-manage-pro-jwt-refresh-secret-key-2026-strong-32b")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    is_testing = os.getenv("FLASK_ENV") == "testing" or os.getenv("TESTING") == "1" or "PYTEST_CURRENT_TEST" in os.environ
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    elif is_testing:
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///edumanage_pro.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5000")
    PROPAGATE_EXCEPTIONS = True
    JSON_SORT_KEYS = False
    TESTING = is_testing
