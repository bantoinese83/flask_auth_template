import logging
import os
import secrets

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    load_dotenv()
    logger.info("Environment variables loaded successfully.")
except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    raise


class Config:
    try:
        SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', secrets.token_hex(32))
        JWT_TOKEN_LOCATION = ['cookies']
        JWT_ACCESS_COOKIE_PATH = '/'
        JWT_REFRESH_COOKIE_PATH = '/token/refresh'
        JWT_COOKIE_CSRF_PROTECT = True
        REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 30  # 30 days
        UPLOAD_FOLDER = 'static/uploads'

        # OAuth's credentials here (use environment variables for security)
        GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
        FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
        GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
        LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')

        # Validate required environment variables
        if not all([GOOGLE_CLIENT_ID, FACEBOOK_CLIENT_ID, GITHUB_CLIENT_ID, LINKEDIN_CLIENT_ID]):
            raise ValueError("One or more OAuth client IDs are missing.")

        logger.info("Configuration loaded successfully.")
    except Exception as e:
        logger.error(f"Error in configuration: {e}")
        raise
