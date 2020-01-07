import app
from models import Subreddits
import praw
from forms import SearchSub, RegistrationForm, LoginForm, RegistrationAppForm, PostForm, Titles, Chapters
from models import User, Post, Bots, Result, Books,  RedditPost, Subreddits

from flask import Flask, render_template, request, url_for, redirect, flash, render_template_string

import ebooklib
from pymongo import MongoClient
from mongoengine import *
import json
import praw
import requests
import os
import glob
import random
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField, validators
from wtforms.validators import DataRequired, Email
from flask_script import Manager
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField
from rake_nltk import Rake
from wtforms.validators import DataRequired
from datetime import datetime
from operator import itemgetter, attrgetter, methodcaller
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from psycopg2 import errors
from caesarcipher import CaesarCipher
app = Flask(__name__)




login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://oaflopean:99burning944@104.154.59.220:5432/data001"
app.config['STATIC_FOLDER']='static/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'fohx6kiu8kieSino'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
this_bot = Bots.query.filter_by(username="scientolog2").first()
client_id = this_bot.client_id

secret = this_bot.secret
password = this_bot.password
username = this_bot.username
reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret, password=password,
                     user_agent='Copypasta', username=username)
#
# a=open("subreddits.txt",mode="w")
# subs=Subreddits.query.all()
# counter=1
# for item in subs[2000:4000]:
#     a.write("r/"+item.sub+"\n\n")
# a.close()
listo=[]
for submission in reddit.subreddit('teenagers').hot(limit=500):
    counter=0
    for o in set(listo):
        print(o)
    print("Author: "+str(submission.author))
    save = reddit.redditor(str(submission.author)).submissions.new()
    for ank in save:
        counter+=1
        new = Subreddits()
        new.sub = str(ank.subreddit)
        print(counter)
        listo.append(ank.subreddit)


        try:
            subs=Subreddits.query.filter_by(sub=new.sub).first()
            if subs:
                continue
            else:
                db.session.add(new)
                print("new: "+str(ank.subreddit))

                db.session.commit()

        except KeyError:
            continue
# a=open("teenagers.txt", mode="w")
# for o in set(listo):
#     a.write("https://www.reddit.com/r/"+o+"\n")
# a.close()