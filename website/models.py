from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    user_name = db.Column(db.String(150), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="user_comment", lazy=True)




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(10000), nullable=False)
    # can create a foreign key; referencing the id variable in the User class, so that is why it is lowercase u
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="post_comment", lazy=True)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(10000), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class Figures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    figure = db.Column(db.String(1000), nullable=False)
    image_address = db.Column(db.String(100000), nullable=False)
    body = db.Column(db.String(1000000), nullable=False)