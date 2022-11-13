'''Database configuration for Flask SQLAlchemy'''
from flask_login import UserMixin
from sqlalchemy import func
from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(30000))
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_edit = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note')
    