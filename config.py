from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mydatabase.db'
app.config["SQALCHAMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)