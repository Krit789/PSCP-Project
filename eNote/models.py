'''Data model for database'''
from flask_login import UserMixin
from datetime import datetime
from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText())
    content = db.Column(db.UnicodeText())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_edit = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):

    def get_id(self):
        return str(self.session_token)

    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(16), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # encryptedkey = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    theme = db.Column(db.String(8), default="day")
    status = db.Column(db.String(16), default="active")
    total_notes = db.Column(db.Integer, default=0)
    deleted_notes = db.Column(db.Integer, default=0)
    notes = db.relationship('Note')
