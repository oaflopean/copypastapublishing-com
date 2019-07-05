from flask import Flask, render_template, request, url_for, redirect, flash
      
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

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
app = Flask(__name__)




app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://doadmin:t264wg0yfx9d6sf7@copy-com1234-do-user-4689509-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require"
app.config['STATIC_FOLDER']='static/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'fohx6kiu8kieSino'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from forms import SearchSub, RegistrationForm, LoginForm, RegistrationAppForm, PostForm, Title, Chapter
from models import User, Post, Bots, Result, Books, Chapter

class ReusableForm(Form):
    name = TextField('subreddit:', validators=[validators.required()])
#
# # Data to serve with our AP
class Entry(Form):
    first=TextField('first:', validators=[validators.required()])
    last=TextField('last:', validators=[validators.required()])
    title=TextField('title:', validators=[validators.required()])
    desc=TextField('desc:', validators=[validators.required()])
    pseudonym=TextField('pseudonym:', validators=[validators.required()])
#move to forms.py


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('register_app'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! You're registered.")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/register/app', methods=['GET', 'POST'])
def register_app():
   if current_user.is_authenticated:
      form = RegistrationAppForm()
      if form.validate_on_submit():

        olduser= User.query.filter_by(username=current_user.username)
           
        if olduser:
            bot_add=Bots.query.filter_by(username=current_user.username).first()
            bot_add.app_name=form.app_name.data
            bot_add.client_id=form.client_id.data
            bot_add.secret=form.secret.data
            bot_add.password=form.password.data
            db.session.add(bot_add)
            db.session.update(bot_add)
            reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                              client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$', user_agent='Copypasta', username="caesarnaples2")

            reddit(subreddit("copypastapublishin").add_moderator("copypastapublishin", current_user.username))
            return redirect(url_for('keywords'))

        else:
            bot_add=Bots()
            bot_add.username=current_user.username
            bot_add.app_name=form.app_name.data
            bot_add.client_id=form.client_id.data
            bot_add.secret=form.secret.data
            db.session.add(bot_add)
            db.session.commit()
            reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                              client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$', user_agent='Copypasta', username="caesarnaples2")

            reddit(subreddit("copypastapublishin").add_moderator("copypastapublishin", current_user.username))
            flash("Congratulations! Your app is registered.")
            return redirect(url_for('kw'))
        return render_template('register_app.html', title='Register your app now', form=form)
   else:
       return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('home'))
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user is None or not user.check_password(form.password.data):
         flash('Invalid username or password')
         return redirect(url_for('login'))
      else:
          login_user(user, remember=form.remember_me.data)
          next_page = request.args.get('next')
          if not next_page or url_parse(next_page).netloc != '':
              next_page = url_for('home')
          return redirect(next_page)
   return render_template('login.html', title='If you\'re already registered, then login now', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def read_all():
    return json.dumps(db.Entries.find())

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

@app.route('/blog')
def blog():
    title="Editor Blog: Jordan Jones"

    return render_template('blog-index.html', title=title)

@app.route('/books', methods=['GET', 'POST'])
@login_required
def books2():
    title="Create an Ebook"
    
    form=Title()
  
    all_books = Books.query.filter_by(username=current_user.username).all()
    print(all_books)
    if form.validate_on_submit():
        book=Books(username=current_user.username, title=form.title.data, author=form.author.data)
        print(book.title)
        print(book.author)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books2'))
    return render_template('books.html', form=form, title=title, all_books=all_books)

@app.route('/ten-minute-pitch')
def pitch():
    title="Ten Minute Pitch: Write a Query Letter"

    return render_template('pitch.html', title=title)

@app.route('/invitation')
def invite():
    title="Huge Impossible Word Search"

    return render_template('invite.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', methods=["POST", "GET"])
def home():
    sub="writing"
    title="Copypasta Publishing: Social Media Marketing"
    form = ReusableForm(request.form)

    if request.method == 'POST':
        name=request.form['name']
        return redirect('/keywords/r/'+name)

    if form.validate():
        # Save the comment here.
        flash('Keywords from r/' + name)
     

    phrasey={"body":[]}

    url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=1500'
    data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()
    for link in data['data']['children']:
        phrasey["body"].append(link['data']['title'])

  #  phrases_string="\n".join(phrasey["body"])
   #print(phrases_string)

    #r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

    #r.extract_keywords_from_text(phrases_string)

    #phrases=r.get_ranked_phrases()
    title=title
    return render_template('index.html', phrases=phrasey["body"], form=form, title=title)


@app.route('/keywords/r/<sub>', methods=["POST", "GET"])
@login_required
def rake2(sub):
   post={}
   form2=PostForm()
   if form2.validate_on_submit():
      post[kw]=form2.kw
      post[sub]=form2.sub
      res = requests.post(url_for('botpost'),headers='Content-Type: application/json',data=json.dumps(post))

      return redirect(url_for('rake2', sub=sub))
   title="Reddit Influencers on r/"+sub
   phrasey={"titles":[],"text":[]}
   url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=300'
   form = ReusableForm(request.form)
   if request.method == 'POST':
       name=request.form['name']
       return redirect('/keywords/r/'+name)

   if form.validate():
        # Save the comment here.
       flash('Keywords from r/' + name)   
   data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()
   if data:
       for link in data['data']['children']:
           phrasey["text"].append(link['data']['title'])
      
           phrasey["text"].append(link['data']['selftext'])


   else:
       return render_template('keywords.html',sub=sub,form=form,  form2=form2, phrases=phrasey, title="Subreddit not found.")

   p = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

   p.extract_keywords_from_text(' '.join(phrasey['text']))

   texts=p.get_ranked_phrases() # To get keyword phrases ranked highest to lowest
     
                # json={"first":first, "last"=last, "title":title,"desc":desc,"pseudonym":pseudonym}
                # return render_template('entries.html', entries=json)
   return render_template('keywords.html',sub=sub,form=form,  form2=form2, phrases=texts, title=title)

    
    
@app.route('/keywords', methods=["POST", "GET"])
@login_required
def kw():     
   sub=None
   texts={}
   title="Reddit Influencers on Multiple Subreddits"

   sort="new"
   form = ReusableForm(request.form)
   if request.method == 'POST':
       name=request.form['name']
       return redirect('/keywords/r/'+name)

   if form.validate():
        # Save the comment here.
       flash('Keywords from r/' + name)      
   return render_template('keywords.html',sub=sub, form=form, phrases=texts, sort=sort, title=title)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")
@app.route('/websites')
def library():

    r=glob.glob("texts/*")
    print(r)
    r=random.sample(r, len(r))
    d={"text":[]}
    for a in r:
        b=open(a)
        c=b.read()
        f=c.split('\n\n')
        for g in f:
                g=g.replace('\n',' ')
                if g!=' ':
                    d["text"].append(g)

    e= d['text']
    reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                            client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$',
                            user_agent='Ravenclaw', username='caesarnaples2')
     

    return render_template("library.html", text=e,title="Copypasta Publishing: Blurbs from Websites")

@app.route('/bot', methods=["POST"])
def botpost():
   req=request.values
   print(req)
   kw=req.get('kw')
   sub=req.get('sub')
   this_bot = Bots.query.filter_by(username=current_user.username).first()
   try:
       client_id=this_bot.client_id
   except AttributeError:
       return redirect("register/app")
   secret=this_bot.secret
   password=this_bot.password
   username=this_bot.username
   print(this_bot.client_id+this_bot.secret+this_bot.password)
   reddit = praw.Reddit(client_id=client_id,
                            client_secret=secret, password=password,
                            user_agent='Copypasta', username=username)
     
     
   try:
       reddit.subreddit('copypastapublishin').submit(sub, selftext=kw)   

   except praw.exceptions.APIException:
       return redirect("keywords/r/sub") 
   #reddit.subreddit('copypastapublishin').submit(f[0:300], url="https://www.reddit.com/search?q="+sub+" "+kw)
     
   return redirect('https://www.reddit.com/r/copypastapublishin/new')
