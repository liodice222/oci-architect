#imports
from flask import redirect, render_template, request, session, url_for, Blueprint
from app.db import db
from app.models.User import User
#for password hash 
from werkzeug.security import generate_password_hash, check_password_hash
#for login functionality 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#for verifying user email/password security 
import re

#set up Blueprint
auth = Blueprint('auth', __name__)

def is_secure_password(password):
    """Validate the security of a password."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, ""

def is_valid_email(email):
    """Validate the email format."""
    if not email: 
            return False
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

#registration route 
@auth.route('/register', methods=['GET', 'POST'])
def register():
    already_user = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('username')

        # Check if the email is valid
        if not is_valid_email(email):
            return render_template('register.html', message="Invalid email format")
        
        # Validate password security
        is_valid, error_message = is_secure_password(password)
        if not is_valid:
            return render_template('register.html', message=error_message)

        #check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print ("User already exists, please go to Login page")
            already_user = True
            return render_template('register.html', message="User already exists, please go to Login page")
        else:
            already_user = False
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login', message="Registration Successful", already_user = already_user))

    return render_template('register.html', already_user = already_user, current_user = current_user)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_failed = None
    login_attempted = False
    if request.method == 'POST':
        login_attempted = True
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            login_failed = True
        else:
            login_failed = False
            session['username'] = user.username
            login_user(user)
        
        return render_template('index.html', login_failed=login_failed, login_attempted = login_attempted)

    return render_template('index.html', login_failed=login_failed, login_attempted = login_attempted)

#logout route 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))