from models import User
from db import db

#search model to be stored in analytics database 
class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    search_query = db.Column(db.String(200))
    search_result = db.Column(db.Text)

    #define relationship with user model
    user = db.relationship('User', backref = 'searches')