import datetime
import logging
import os
from urllib.parse import urlencode

import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
import google.oauth2.id_token
import google_auth_oauthlib.flow
import requests
from flask import Blueprint, render_template, flash
from flask import current_app as app
from flask import redirect, url_for, request, session
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, \
    get_jwt_identity, get_current_user, JWTManager
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from app import db
from app.auth.forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, UploadAvatarForm
from app.models import User

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds, _ = google.auth.default(scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)

# Initialize JWTManager
jwt = JWTManager(app)


# Home route
@auth.route('/')
def home():
    registration_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('index.html', registration_form=registration_form, login_form=login_form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=email,
                                               expires_delta=datetime.timedelta(days=30 if remember else 1))
            response = redirect(url_for('auth.dashboard'))
            set_access_cookies(response, access_token)
            flash('Logged in successfully!', 'success')
            logger.info(f"User {email} logged in successfully.")
            return response
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            logger.warning(f"Failed login attempt for {email}.")
            return redirect(url_for('auth.login'))
    return render_template('signin.html', login_form=login_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"User {username} registered successfully.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user {username}: {e}")
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(days=30))
        response = redirect(url_for('auth.dashboard'))
        set_access_cookies(response, access_token)
        flash('Registration successful! You are logged in.', 'success')
        return response
    return render_template('signup.html', registration_form=registration_form)


@auth.route('/edit_profile', methods=['GET', 'POST'])
@jwt_required()
def edit_profile():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.location = form.location.data
        user.bio = form.bio.data
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('auth.dashboard'))
    return render_template('edit_profile.html', form=form, user=user)


@auth.route('/delete_account', methods=['POST'])
@jwt_required()
def delete_account():
    current_user = get_current_user()
    try:
        db.session.delete(current_user)
        db.session.commit()
        flash('Account deleted successfully', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting the account', 'danger')
    return redirect(url_for('auth.logout'))


@auth.route('/upload_avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    current_user = get_current_user()
    if 'avatar' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['avatar']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Upload to Google Drive
        file_metadata = {'name': filename}
        media = MediaFileUpload(file_path, mimetype=file.content_type)
        drive_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        drive_url = f"https://drive.google.com/uc?id={drive_file.get('id')}"

        # Update user's avatar URL in the database
        current_user.avatar_url = drive_url
        db.session.commit()
        flash('Profile picture updated successfully')
        return redirect(url_for('auth.dashboard'))
    else:
        flash('Invalid file type')
        return redirect(request.url)


@auth.route('/change_password', methods=['GET', 'POST'])
@jwt_required()
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Handle password change logic here
        flash('Your password has been updated.', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('change_password.html', form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()


@auth.route('/dashboard', methods=['GET', 'POST'])
@jwt_required()
def dashboard():
    form = UploadAvatarForm()
    user = get_current_user()
    if form.validate_on_submit():
        # Handle the upload logic here (see below)
        flash('Profile picture updated successfully')
        return redirect(url_for('auth.dashboard'))
    return render_template('user_dashboard.html', current_user=user.email, user=user, form=form)


@auth.route('/logout')
def logout():
    response = redirect(url_for('auth.home'))
    unset_jwt_cookies(response)
    flash('You have been logged out.', 'success')
    logger.info("User logged out successfully.")
    return response


# Google OAuth
@auth.route('/login/google')
def login_google():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    )
    flow.redirect_uri = url_for('auth.google_callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


@auth.route('/login/google/callback')
def google_callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', state=state, scopes=SCOPES
    )
    flow.redirect_uri = url_for('auth.google_callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()
    id_info = google.oauth2.id_token.verify_oauth2_token(
        credentials.id_token, request_session, app.config['GOOGLE_CLIENT_ID']
    )
    # Handle user login with id_info
    return redirect(url_for('auth.dashboard'))


# Facebook OAuth
@auth.route('/login/facebook')
def login_facebook():
    facebook_auth_url = 'https://www.facebook.com/v10.0/dialog/oauth'
    params = {
        'client_id': app.config['FACEBOOK_CLIENT_ID'],
        'redirect_uri': url_for('auth.facebook_callback', _external=True),
        'state': 'random_string',
        'scope': 'email'
    }
    return redirect(f"{facebook_auth_url}?{urlencode(params)}")


@auth.route('/login/facebook/callback')
def facebook_callback():
    code = request.args.get('code')
    token_url = 'https://graph.facebook.com/v10.0/oauth/access_token'
    params = {
        'client_id': app.config['FACEBOOK_CLIENT_ID'],
        'redirect_uri': url_for('auth.facebook_callback', _external=True),
        'client_secret': app.config['FACEBOOK_CLIENT_SECRET'],
        'code': code
    }
    response = requests.get(token_url, params=params)
    access_token = response.json().get('access_token')
    # Handle user login with access_token
    return redirect(url_for('auth.dashboard'))


# GitHub OAuth
@auth.route('/login/github')
def login_github():
    github_auth_url = 'https://github.com/login/oauth/authorize'
    params = {
        'client_id': app.config['GITHUB_CLIENT_ID'],
        'redirect_uri': url_for('auth.github_callback', _external=True),
        'scope': 'user:email'
    }
    return redirect(f"{github_auth_url}?{urlencode(params)}")


@auth.route('/login/github/callback')
def github_callback():
    code = request.args.get('code')
    token_url = 'https://github.com/login/oauth/access_token'
    params = {
        'client_id': app.config['GITHUB_CLIENT_ID'],
        'client_secret': app.config['GITHUB_CLIENT_SECRET'],
        'code': code
    }
    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=params, headers=headers)
    access_token = response.json().get('access_token')
    # Handle user login with access_token
    return redirect(url_for('auth.dashboard'))


# LinkedIn OAuth
@auth.route('/login/linkedin')
def login_linkedin():
    linkedin_auth_url = 'https://www.linkedin.com/oauth/v2/authorization'
    params = {
        'response_type': 'code',
        'client_id': app.config['LINKEDIN_CLIENT_ID'],
        'redirect_uri': url_for('auth.linkedin_callback', _external=True),
        'scope': 'r_liteprofile r_emailaddress'
    }
    return redirect(f"{linkedin_auth_url}?{urlencode(params)}")


@auth.route('/login/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': url_for('auth.linkedin_callback', _external=True),
        'client_id': app.config['LINKEDIN_CLIENT_ID'],
        'client_secret': app.config['LINKEDIN_CLIENT_SECRET']
    }
    response = requests.post(token_url, data=params)
    access_token = response.json().get('access_token')
    # Handle user login with access_token
    return redirect(url_for('auth.dashboard'))
