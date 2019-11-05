from api import db
from sqlalchemy import MetaData, Table, Column, Integer, String

# class Employee(db.Model):
#     __tablename__ = 'employes'
#     id = db.Column('id', db.Integer, primary_key=True)
#     first_name = db.Column('first_name', db.String(255))
#     last_name = db.Column('last_name', db.String(255))
#     email = db.Column('email', db.String(255), unique=True)
#     gender = db.Column('gender', db.String(255))
#     ip_address = db.Column('ip_address', db.String(255))
#     app_name = db.Column('app_name', db.String(255))
#     country = db.Column('country', db.String(255))
#     job_title = db.Column('job_title', db.String(255))

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)