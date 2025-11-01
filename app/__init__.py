import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload and sorted directories exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["SORTED_FOLDER"], exist_ok=True)

    # Initialize rate limiter
    def rate_key():
        from flask import session

        sid = session.get("sid", "anon")
        ip = get_remote_address()
        return f"{sid}:{ip}"

    limiter = Limiter(
        app=app, key_func=rate_key, default_limits=["200 per day", "50 per hour"]
    )

    # Register routes
    from app.routes import register_routes

    register_routes(app, limiter)

    return app
