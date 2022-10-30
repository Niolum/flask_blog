from enum import unique
import uuid
import hashlib
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_image_alchemy.fields import StdImageField
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from blog import db, fs_storage


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    photo = db.Column(
        StdImageField(
            storage=fs_storage, 
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        ), nullable=True
    )
    posts = db.relationship('Post', lazy='select', backref=db.backref('user', lazy='joined'))
    comments = db.relationship('Comment',lazy='select', backref=db.backref('user', lazy='joined'))

    # def _init__(self, username, password):
    #     self.username = username
    #     self.password = generate_password_hash(password)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return  check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.username}"


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True, unique=True)
    body = db.Column(db.String, nullable=False)
    image = db.Column(
        StdImageField( 
            storage=fs_storage,
            variations={
                'thumbnail': {"width": 500, "height": 500, "crop": True}
            }
        ), nullable=True
    )
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Comment', lazy='select', backref=db.backref('post', lazy='joined'))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"Post {self.title}"


class Tag(db.Model):
    __tablename__= 'tag'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True, index=True, unique=True)

    def __repr__(self):
        return f"Tag {self.title}"


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment {self.id} - {self.owner_id} - {self.post_id}"
