import datetime

from api import db
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime


class ApiLog(db.Model):
    __tablename__ = 'api_log'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(50))
    resource = db.Column(db.String(255))
    request_args = db.Column(db.String(16000000))
    token = db.Column(db.String(255))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)