from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# DATABASE CREDENTIALS
ENGINE = 'mysql'
USERNAME = 'test'
PASSWORD = 'testtest'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'api'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ENGINE + "://" + USERNAME + ":" +PASSWORD + "@" + HOST + ":" + PORT + "/" + DATABASE
app.config['SECRET_KEY'] = 'SEX_BOT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from api import routes, models