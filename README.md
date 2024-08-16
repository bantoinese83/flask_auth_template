# Flask User Dashboard

This is a Flask-based web application that provides a user dashboard with functionalities such as profile management, avatar upload, and password change. The application uses Google Drive for storing user avatars.

## Features

- User registration and login
- Profile management (edit profile, change password, delete account)
- Upload and display user avatars
- Store avatars on Google Drive
- CSRF protection for forms

## Technologies Used

- Python
- Flask
- Flask-WTF
- Flask-Login
- Google Drive API
- HTML/CSS (Bulma CSS framework)
- JavaScript

## Setup and Installation

### Prerequisites

- Python 3.6+
- Google Cloud account with Google Drive API enabled
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/bantoinese83/flask_auth_template.git
    cd flask-auth-template
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up Google Drive API:**
    - Enable the Google Drive API in your Google Cloud project.
    - Download the `credentials.json` file and place it in the root directory of the project.

5. **Set environment variables:**
    ```sh
    export FLASK_APP=app
    export FLASK_ENV=development
    ```

6. **Run the application:**
    ```sh
    flask run
    ```

## Usage

1. **Register a new user:**
    - Navigate to `/register` and fill out the registration form.

2. **Login:**
    - Navigate to `/login` and log in with your credentials.

3. **Dashboard:**
    - After logging in, you will be redirected to the dashboard where you can manage your profile.

4. **Upload Avatar:**
    - Use the form on the dashboard to upload a new profile picture. The picture will be stored on Google Drive.

5. **Edit Profile:**
    - Navigate to `/edit_profile` to update your profile information.

6. **Change Password:**
    - Navigate to `/change_password` to change your password.

7. **Delete Account:**
    - Navigate to `/delete_account` to delete your account.

## Project Structure

The project structure is as follows:
```markdown
Flask_Auth_Template/
├── .idea/
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── routes.py
│   │   ├── models.py
│   ├── __init__.py
├── instance/
│   ├── users.db
├── static/
│   ├── css/
│   │   ├── style.css
│   ├── images/
│   │   ├── default_avatar.png
│   │   ├── logo.png
│   ├── js/
│   │   ├── app.js
│   │   ├── lottie.js
│   │   ├── password-strength.js
│   │   ├── password-visibility.js
│   ├── uploads/
├── templates/
│   ├── base.html
│   ├── change_password.html
│   ├── edit_profile.html
│   ├── index.html
│   ├── signin.html
│   ├── signup.html
│   ├── user_dashboard.html
├── .env
├── config.py
├── Flask_Auth_Template.iml
├── README.md
├── run.py
```
## Contributing


1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

