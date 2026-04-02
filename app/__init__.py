from flask import Flask
from config import Config

from app.extensions import db, migrate, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.files.routes import file_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(file_bp)

    from app.middleware import register_middleware

    register_middleware(app)

    from app.errors import register_error_handlers

    register_error_handlers(app)

    return app
