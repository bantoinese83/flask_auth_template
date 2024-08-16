import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Load configuration
    try:
        app.config.from_object(Config)
        logger.info("Configuration loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

    # Initialize extensions
    try:
        db.init_app(app)
        jwt.init_app(app)
        logger.info("Extensions initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing extensions: {e}")
        raise

    # Initialize extensions
    csrf = CSRFProtect(app)
    csrf.init_app(app)

    # Register blueprints
    try:
        with app.app_context():
            from app.auth.routes import auth
            app.register_blueprint(auth)
            logger.info("Blueprints registered successfully.")
    except Exception as e:
        logger.error(f"Error registering blueprints: {e}")
        raise

    return app