import os
import uuid
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    current_app,
    send_from_directory,
    abort,
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.extensions import db
from app.models import File
from .utils import allowed_file


file_bp = Blueprint("files", __name__, url_prefix="/files")


@file_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            flash("No file selected", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Unsupported file type", "danger")
            return redirect(request.url)

        original_filename = secure_filename(file.filename)
        stored_filename = f"{uuid.uuid4()}_{original_filename}"

        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], stored_filename)

        file.save(filepath)

        new_file = File(
            filename=original_filename,
            stored_filename=stored_filename,
            user_id=current_user.id,
        )

        db.session.add(new_file)
        db.session.commit()

        flash("File uploaded successfully", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("files/upload.html")


@file_bp.route("/download/<int:file_id>")
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)

    if file.user_id != current_user.id:
        abort(403)

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"], file.stored_filename, as_attachment=True
    )


@file_bp.route("/delete/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)

    if file.user_id != current_user.id:
        abort(403)

    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file.stored_filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(file)
    db.session.commit()

    flash("File deleted")
    return redirect(url_for("main.dashboard"))
