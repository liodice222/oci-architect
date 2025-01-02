from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.db import db
from app.models.User import User
from instance.config import Config

# Initialize app, db, and login manager
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    db.init_app(app)  # Initialize db with app

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Register the main blueprint for routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
