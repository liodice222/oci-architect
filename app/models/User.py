from flask_login import UserMixin
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash

#set up user model to be stored in user database  
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    #password_hash = db.Column(db.String(200), nullable=False)

    # Method to set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to verify password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    


