'''Database configuration for Flask SQLAlchemy'''
from flask_login import UserMixin
from datetime import datetime
from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText())
    content = db.Column(db.UnicodeText())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_edit = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.relationship('Note')
