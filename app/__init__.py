from flask import Flask
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Import and register blueprints
    from app.routes.cv_routes import cv_bp
    app.register_blueprint(cv_bp)

    return app