import logging
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Profile Fields
    full_name = db.Column(db.String(150), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(150), nullable=True)
    website = db.Column(db.String(150), nullable=True)
    social_media = db.Column(db.String(150), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(150), nullable=True)
    state = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(150), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(150), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_profile(self, full_name=None, bio=None, profile_picture=None):
        try:
            if full_name:
                if len(full_name) > 150:
                    raise ValueError("Full name is too long.")
                self.full_name = full_name
            if bio:
                self.bio = bio
            if profile_picture:
                if len(profile_picture) > 150:
                    raise ValueError("Profile picture URL is too long.")
                self.profile_picture = profile_picture
            self.updated_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"Profile for user {self.username} has been updated.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating profile for user {self.username}: {e}")
            raise

    def __repr__(self):
        return f'<User {self.username}>'
