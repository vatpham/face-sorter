import os
from uuid import uuid4
from flask import session, current_app


def current_user_dirs():
    sid = session.get("sid")
    if not sid:
        sid = uuid4().hex
        session["sid"] = sid

    upload = os.path.join(current_app.config["UPLOAD_FOLDER"], sid)
    sorted_dir = os.path.join(current_app.config["SORTED_FOLDER"], sid)

    os.makedirs(upload, exist_ok=True)
    os.makedirs(sorted_dir, exist_ok=True)

    return sid, upload, sorted_dir