import os
import io
import time
import re
import zipfile
from flask import (
    request,
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    make_response,
    send_file,
    abort,
    session,
    send_from_directory,
    current_app,
    jsonify,
)
from werkzeug.utils import secure_filename

from app.utils import (
    current_user_dirs,
    cleanup_old_sessions,
    allowed_file,
    is_real_image,
    sort_images,
)


def register_routes(app, limiter):
    @app.route("/", methods=["GET", "POST"])
    @limiter.limit("10 per minute")
    def index():
        # Clean old uploads and sorted folders
        now = time.time()
        last = session.get("last_cleanup_ts", 0)
        if now - last > 900:  # 15 minutes
            sid = session.get("sid")
            max_age = current_app.config["MAX_AGE"]
            cleanup_old_sessions(
                current_app.config["UPLOAD_FOLDER"], max_age, current_sid=sid
            )
            cleanup_old_sessions(
                current_app.config["SORTED_FOLDER"], max_age, current_sid=sid
            )
            session["last_cleanup_ts"] = now

        if request.method == "POST":
            _, user_upload, user_sorted = current_user_dirs()
            files = request.files.getlist("file")
            if not files or files[0].filename == "":
                flash("No file selected!")
                return redirect(request.url)

            import shutil

            for folder in [user_upload, user_sorted]:
                if os.path.isdir(folder):
                    shutil.rmtree(folder)  # delete the entire directory
                os.makedirs(folder, exist_ok=True)  # recreate empty folder

            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    save_path = os.path.join(user_upload, filename)
                    file.save(save_path)

                    if (
                        os.path.getsize(save_path)
                        > current_app.config["MAX_BYTES_PER_FILE"]
                    ):
                        os.remove(save_path)
                        flash(f"{filename} is too large (max 10 MB per file)")
                        return redirect(request.url)

                    if not is_real_image(save_path):
                        os.remove(save_path)
                        flash(f"{filename} is not a valid image.")
                        return redirect(request.url)

                else:
                    flash(f"{file.filename} is not an allowed file type.")
                    return redirect(request.url)

            faces = sort_images(user_upload, user_sorted)
            if faces > 0:
                return redirect(url_for("results"))
            flash("No faces found. Try different photos.")
            return redirect(url_for("index"))

        messages = get_flashed_messages()
        resp = make_response(render_template("index.html", messages=messages))
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp

    @app.route("/results")
    def results():
        sid, _, user_sorted = current_user_dirs()
        persons = []
        if os.path.isdir(user_sorted):
            for person_folder in sorted(os.listdir(user_sorted)):
                folder_path = os.path.join(user_sorted, person_folder)
                if os.path.isdir(folder_path):
                    match = re.match(r"person_(\d+)$", person_folder)
                    if match:
                        display_name = f"Person {int(match.group(1)) + 1}"
                    else:
                        display_name = person_folder.replace("_", " ").title()
                    images = [
                        img
                        for img in os.listdir(folder_path)
                        if img.lower().endswith((".jpg", ".jpeg", ".png"))
                    ]
                    persons.append(
                        {
                            "name": person_folder,
                            "display_name": display_name,
                            "images": images,
                        }
                    )

        resp = make_response(render_template("results.html", persons=persons))
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp

    @limiter.limit("5 per minute")
    @app.route("/download/sorted.zip")
    def download_sorted_zip():
        sid, _, user_sorted = current_user_dirs()
        if not os.path.isdir(user_sorted):
            abort(404)

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(user_sorted):
                for f in files:
                    full_path = os.path.join(root, f)
                    arcname = os.path.relpath(full_path, user_sorted)
                    zf.write(full_path, arcname)
        buf.seek(0)
        return send_file(
            buf,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"sorted_{sid}.zip",
        )

    @app.route("/download/person/<person_name>.zip")
    def download_person_zip(person_name):
        sid, _, user_sorted = current_user_dirs()
        person_dir = os.path.join(user_sorted, person_name)

        if not os.path.isdir(person_dir):
            abort(404)

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(person_dir):
                for f in files:
                    full_path = os.path.join(root, f)
                    arcname = os.path.relpath(full_path, person_dir)
                    zf.write(full_path, arcname)
        buf.seek(0)

        return send_file(
            buf,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{person_name}.zip",
        )

    @app.route("/files/<path:subpath>")
    def files(subpath):
        sid, _, user_sorted = current_user_dirs()
        full_path = os.path.join(user_sorted, subpath)
        full_real = os.path.realpath(full_path)
        root_real = os.path.realpath(user_sorted)

        if not full_real.startswith(root_real + os.sep):
            abort(403)
        if not os.path.isfile(full_real):
            abort(404)

        directory = os.path.dirname(full_real)
        filename = os.path.basename(full_real)
        return send_from_directory(directory, filename)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Not found"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403, message="Forbidden"), 403

    @app.errorhandler(429)
    def too_many_requests(e):
        return (
            render_template(
                "error.html",
                code=429,
                message="Too many requests. Please try again later.",
            ),
            429,
        )

    @app.route("/rename-person", methods=["POST"])
    def rename_person():
        sid, _, user_sorted = current_user_dirs()
        data = request.get_json()
        old_name = data.get("old_name", "").strip()
        new_name = data.get("new_name", "").strip()

        if not old_name or not new_name:
            return jsonify({"error": "Invalid names"}), 400

        old_path = os.path.join(user_sorted, old_name)
        new_path = os.path.join(user_sorted, new_name)

        if not os.path.isdir(old_path):
            return jsonify({"error": "Folder not found"}), 404

        if os.path.exists(new_path):
            return jsonify({"error": "Name already exists"}), 400

        try:
            os.rename(old_path, new_path)
            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

