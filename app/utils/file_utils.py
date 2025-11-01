import os
import magic
from PIL import Image
from flask import current_app


def allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def is_real_image(path: str) -> bool:
    try:
        mime = magic.from_file(path, mime=True)
        if mime not in ("image/jpeg", "image/png"):
            return False

        with Image.open(path) as img:
            img.verify()

        return True
    except Exception:
        return False