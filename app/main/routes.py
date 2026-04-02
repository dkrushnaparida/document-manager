from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import File

main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template("files/dashboard.html", files=files)
