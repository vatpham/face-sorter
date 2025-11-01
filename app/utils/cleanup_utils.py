import os
import shutil
import time


def cleanup_old_sessions(folder_root: str, max_age: int, current_sid: str | None):
    now = time.time()

    if not os.path.isdir(folder_root):
        return

    for entry in os.listdir(folder_root):
        if entry == current_sid:
            continue

        path = os.path.join(folder_root, entry)
        if not os.path.isdir(path):
            continue

        if now - os.path.getatime(path) > max_age:
            shutil.rmtree(path, ignore_errors=True)

