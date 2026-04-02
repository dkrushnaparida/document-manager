from flask import Blueprint, render_template
from flask_login import login_required, current_user

file_bp = Blueprint("files", __name__, url_prefix="/files")


@file_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", files=current_user.files)
