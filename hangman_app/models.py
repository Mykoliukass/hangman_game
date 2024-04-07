from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
