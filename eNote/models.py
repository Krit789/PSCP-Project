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
    is_public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):

    def get_id(self):
        return str(self.session_token)

    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(16), unique=True, nullable=False)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(32), nullable=False)
    password_salt = db.Column(db.String(32), nullable=False)
    profile_img = db.Column(db.String(20))
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_notes = db.Column(db.Integer, default=0)
    deleted_notes = db.Column(db.Integer, default=0)
    note_bg = db.Column(db.Integer, default=6)
    notes = db.relationship('Note')
