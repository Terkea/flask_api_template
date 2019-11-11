import datetime

from api import db
from sqlalchemy import Column, DateTime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
