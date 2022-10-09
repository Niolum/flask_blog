from enum import unique
from operator import index
from werkzeug.security import check_password_hash, generate_password_hash
from blog import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True, index=True)
    password = db.Column(db.String(60), nullable=True)

    def _init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return f"{self.id}:{self.username}"