from flask import Flask
from app.config import Config
from .database import db
from flask_migrate import Migrate







def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)



    # Import and register blueprints
    from app.routes.cv_routes import cv_bp
    app.register_blueprint(cv_bp)



    return app