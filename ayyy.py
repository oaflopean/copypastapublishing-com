import app
from models import Subreddits
import praw
import forms
import models
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
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://doadmin:t264wg0yfx9d6sf7@copy-com1234-do-user-4689509-0.db.ondigitalocean.com:25060/cp-admin?sslmode=require"
app.config['STATIC_FOLDER']='static/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'fohx6kiu8kieSino'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                     client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$', user_agent='Copypasta',
                     username="caesarnaples2")
a=open("subreddits.txt",mode="w")
subs=Subreddits.query.all()
counter=1
for item in subs[2000:4000]:
    a.write("r/"+item.sub+"\n\n")
a.close()

# for submission in reddit.subreddit('teenagers').hot(limit=500):
#     counter=0
#     for o in set(listo):
#         print(o)
#     print("Author: "+str(submission.author))
#     save = reddit.redditor(str(submission.author)).submissions.new()
#     for ank in save:
#         counter+=1
#         new = Subreddits()
#         new.sub = str(ank.subreddit)
#         print(counter)
#         listo.append(ank.subreddit)
#
#
#         try:
#             subs=Subreddits.query.filter_by(sub=new.sub).first()
#             if subs:
#                 continue
#             else:
#                 db.session.add(new)
#                 print("new: "+str(ank.subreddit))
#
#                 db.session.commit()
#
#         except KeyError:
#             continue
# a=open("teenagers.txt", mode="w")
# for o in set(listo):
#     a.write("https://www.reddit.com/r/"+o+"\n")
# a.close()