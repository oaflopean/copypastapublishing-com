from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from app import db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    kw = db.Column(db.String())
    sub = db.Column(db.String())
    username = db.Column(db.String(), db.ForeignKey('user.username'))

    def __repr__(self):
        return '<id {}>'.format(self.kw)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Bots(db.Model):
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),  db.ForeignKey('user.username'))
    app_name= db.Column(db.String(128))
    client_id= db.Column(db.String(128))
    secret= db.Column(db.String(128))
    password= db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password=password

    def check_password(self, password):
        return self.password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Books(db.Model):
    __tablename__='books' 
    id  = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(300))
    author=db.Column(db.String(300))
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    description = db.Column(db.String())
    uri=db.Column(db.String())
            
    def __repr__(self):
        return '<Books {}>'.format(self.title)
        
class Chapter(db.Model):
    __tablename__= 'chapter'
    id = db.Column(db.Integer(), primary_key=True)
    parent_id = db.Column(db.Integer(), db.ForeignKey('books.id'))
    text = db.Column(db.String())
    uri=db.Column(db.String(), db.ForeignKey('redditpost.uri'))

class RedditPost(db.Model):
    __tablename__='redditpost' 
    id  = db.Column(db.Integer(), primary_key=True)
    uri = db.Column(db.String(), unique=True)
    title=db.Column(db.String())
    body = db.Column(db.String())
    integer=db.Column(db.Integer())
            
    def __repr__(self):
        return '<RedditPost {}>'.format(self.uri)
       