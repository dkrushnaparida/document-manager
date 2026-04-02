from flask import jsonify, render_template


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        if "api" in str(error):
            return jsonify({"error": "Not Found"}), 404

        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal Server Error"}), 500
