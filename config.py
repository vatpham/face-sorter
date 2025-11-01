import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    UPLOAD_FOLDER = "uploads"
    SORTED_FOLDER = "sorted"
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    MAX_BYTES_PER_FILE = 10 * 1024 * 1024  # 10 MB per image
    MAX_AGE = 24 * 3600  # 24 hours
