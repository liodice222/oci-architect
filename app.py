from flask import Flask
from db import db
from dotenv import load_dotenv
import os
from auth import auth as auth_blueprint
from flask_login import LoginManager
from models.User import User

load_dotenv()

app = Flask(__name__)
app.register_blueprint(auth_blueprint)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#debugging for secret key 
print(f"Secret Key: {app.config['SECRET_KEY']}")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


