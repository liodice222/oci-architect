from app import create_app
from app.db import db
from flask_login import LoginManager
from app.models.User import User
from flask import redirect, url_for, render_template


app = create_app()

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    #TODO: add Custom error page
    print("rendering unauthorized template")
    return render_template('unauthorized.html', login_url=url_for('auth.login')), 403

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "  # Allow resources only from the same origin
        "script-src 'self'; "  # Allow scripts only from the same origin
        "style-src 'self' https://cdn.jsdelivr.net; "  # Allow styles from your origin and trusted CDNs
        "img-src 'self' data:; "  # Allow images from your origin and inline data URIs
        "object-src 'none';"  # Disallow embedded objects like Flash or PDFs
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)
