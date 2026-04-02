from flask import Blueprint

file_bp = Blueprint("files", __name__, url_prefix="/files")


@file_bp.route("/test")
def test_files():
    return "Files working"
