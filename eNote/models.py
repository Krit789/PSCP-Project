'''Database configuration for Flask SQLAlchemy'''
from flask_login import UserMixin
from sqlalchemy import func
from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.UnicodeText())
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_edit = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=True)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note')
