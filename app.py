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
from operator import itemgetter, attrgetter, methodcaller
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from psycopg2 import errors
app = Flask(__name__)




login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://doadmin:t264wg0yfx9d6sf7@copy-com1234-do-user-4689509-0.db.ondigitalocean.com:25060/cp-admin?sslmode=require"
app.config['STATIC_FOLDER']='static/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'fohx6kiu8kieSino'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from forms import SearchSub, RegistrationForm, LoginForm, RegistrationAppForm, PostForm, Titles, Chapters
from models import User, Post, Bots, Result, Books, Chapter, RedditPost, Subreddits

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

@app.route('/baby', methods=['GET', 'POST'])
def jpg():
   render_template('jpg.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('register_app'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data)
        except NameError:
            return(redirect(url_for('register')))

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

        olduser= Bots.query.filter_by(username=current_user.username).first()
           
        if olduser:
            bot_add=Bots.query.filter_by(username=current_user.username).first()
            bot_add.app_name=form.app_name.data
            bot_add.client_id=form.client_id.data
            bot_add.secret=form.secret.data
            bot_add.password=form.password.data
            #db.session.add(bot_add)
            db.session.commit()
            reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                              client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$', user_agent='Copypasta', username="caesarnaples2")
            try:
                reddit.subreddit("copypastapublishin").moderator.add(current_user.username)
            except praw.exceptions.APIException:
                flash("Congratulations! Your app is registered.")
            return redirect(url_for('kw'))

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
            try:
                reddit.subreddit("copypastapublishin").moderator.add(current_user.username)
            except praw.exceptions.APIException:
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
          reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                              client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$', user_agent='Copypasta', username="caesarnaples2")
        
          save=reddit.redditor(form.username.data).submissions.new()
                
          for ank in save:
              new=Subreddits()
              new.sub= str(ank.subreddit)
              print(Subreddits.query.all())
              if Subreddits.query.filter_by(sub=new.sub).first():
                  continue
              else:
                  db.session.add(new)
                  print(ank.subreddit)
                  db.session.commit()
  
          login_user(user, remember=form.remember_me.data)
          next_page = request.args.get('next')
          if not next_page or url_parse(next_page).netloc != '':
              next_page = url_for("jpg.html")
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

@app.route('/admin/', methods=['GET', 'POST'])
@app.route('/admin', methods=['GET', 'POST'])
def admin1():

    if current_user.is_authenticated:
        username=current_user.username
        login=[True,current_user.username]
    else:
        login=[False,"caesarnaples2"]
        username="caesarnaples2"
    if request.args.get("uri", default=None, type=str)!=None:
        uri_type=RedditPost.query.filter_by(uri=request.args.get("uri")).order_by(RedditPost.id.desc()).all()
        kind="uri"
        return render_template('admin.html',uri=request.args.get("uri"),login=login,kind=kind, username=username, content=uri_type)

    elif request.args.get("username", default=None, type=str)!=None:
        uri_type=RedditPost.query.filter_by(username=request.args.get("username")).order_by(RedditPost.id.desc()).all()
        kind="username"
        return render_template('admin.html',kind=kind, username=username,login=login, content=uri_type)
   
    else:
        kind="all"
        uri_type=RedditPost.query.order_by(RedditPost.id.desc()).all()
        return render_template('admin.html',login=login, username=username, kind=kind,content=uri_type)




@app.route('/admin/r/<sub>', methods=['GET', 'POST'])
def admin2(sub):
    if current_user.is_authenticated:
        username=current_user.username
        login=[True,username]
    else:
        username="caesarnaples2"  

        login=[False,username]
    post=RedditPost()
    form2=PostForm()
    if form2.validate_on_submit():
        post["title"]=form2.kw
        res = requests.post(url_for('botpost'),headers='Content-Type: application/json',data=json.dumps(post))

        return redirect(url_for('rake2', sub=sub))
    title="Reddit Influencers on r/"+sub
    url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=300'
    form = ReusableForm(request.form)
    if request.method == 'POST':
        name=request.form['name']
        return redirect('/admin/r/'+name)
    texts=[]
    if form.validate():
       # Save the comment here.
       flash('Keywords from r/' + name)   
    data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()

    if data:
      for link in data['data']['children']:
          uri=link['data']['permalink']
          title2=link['data']['title']
          p = Rake(min_length=2) # Uses stopwords for english from NLTK, and all puntuation characters.
          p.extract_keywords_from_text(link['data']['title']+link['data']['selftext'])
          # To get keyword phrases ranked highest to lowest
          for post in p.get_ranked_phrases_with_scores():
              print(post)

              texts.append(RedditPost(uri=uri, body=post[1], title=title2, integer=int(post[0])))

    texts=sorted(texts, key=attrgetter('integer'), reverse=True)
         # json={"first":first, "last"=last, "title":title,"desc":desc,"pseudonym":pseudonym}
                # return render_template('entries.html', entries=json
    return render_template('admin.html',login=login, sub=sub,form=form, kind=sub, form2=form2, phrases=texts, title=title)

    
   
@app.route('/admin/<kind>', methods=['GET', 'POST'])
def admin3(kind):
    if current_user.is_authenticated:
        username=current_user.username
        login=[True,current_user.username]
    else:
        login=[False, "caesarnaples2"]
        username="caesarnaples2"
    if kind=="books":
      
        book =RedditPost.query.join(Books).filter(RedditPost.uri==Books.uri).order_by(RedditPost.id.desc()).all()

        

        return render_template('admin.html',login=login, username=username, kind=kind, content=book)
  
    if kind=="users":
        content=User.query.join(RedditPost).order_by(RedditPost.id.desc()).all()
        return render_template('admin.html',login=login, kind=kind, username=username,content=content)

    if kind=="subs":
        url2 = 'https://www.reddit.com/api/trending_subreddits/.json'
        data2 = requests.get(url2, headers={'user-agent': 'scraper by /u/ciwi'}).json()
        subs1=Subreddits.query.all()
        data3=[]
        for sub2 in subs1:
            data3.append(sub2.sub) 
        subs=data3+data2["subreddit_names"]+["AskReddit","announcements","funny","pics","todayilearned","science","IAmA","blog","videos","worldnews","gaming","movies","Music","aww","news","gifs","askscience","explainlikeimfive","EarthPorn","books","television","LifeProTips","sports","DIY","Showerthoughts","space","Jokes","tifu","food","photoshopbattles","Art","InternetIsBeautiful","mildlyinteresting","GetMotivated","history","nottheonion","gadgets","dataisbeautiful","Futurology","Documentaries","listentothis","personalfinance","philosophy","nosleep","creepy","OldSchoolCool","UpliftingNews","WritingPrompts","TwoXChromosomes"]
    
        return render_template('admin.html',login=login, kind=kind, subs=subs, username=username,content={}, posts={})






@app.route('/books', methods=['GET', 'POST'])
def books2():
    return render_template("jpg.html") 
        #reddit.subreddit('copypastapublishin').submit(f[0:300], url="https://www.reddit.com/search?q="+sub+" "+kw)
        

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
    title="Create an Ebook"
    if current_user.is_authenticated:
        login=[True,current_user.username]
        username=current_user.username
    else:
        login=[False, 'caesarnaples2']
        username="caesarnaples2"
    form2=Titles()

    if form2.validate_on_submit():
        book=Books()
        book.title=form.title.data
        book.author=form.author.data
        book.description=form.description.data
        try:
          book.username=current_user.username
        except AttributeError:
          book.username="caesarnaples2"
        s  = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        passlen = 12
        book.uri =  "".join(random.sample(s,passlen ))

        kw=book.description
        title=book.title
        author=book.author
        this_bot = Bots.query.filter_by(username="caesarnaples2").first()
        try:
           client_id=this_bot.client_id
        except AttributeError:
           return redirect("register/app")
        secret=this_bot.secret
        password=this_bot.password
        username=this_bot.username
        reddit = praw.Reddit(client_id=client_id,
                                client_secret=secret, password=password,
                                user_agent='Copypasta', username="caesarnaples2")
         
         
        try:
           reddit_url=reddit.subreddit('publishcopypasta').submit(title+ " by "+author, selftext= kw).permalink   
           

           post=RedditPost(uri=book.uri,reddit_url=reddit_url,  login=login, title=book.title, body=book.description, username=book.username)
           book.reddit_url=reddit_url
           db.session.add(post)
           db.session.commit()
           db.session.add(book)
           db.session.commit()
          
        except praw.exceptions.APIException:
           return redirect("admin?="+book.uri) 
        #reddit.subreddit('copypastapublishin').submit(f[0:300], url="https://www.reddit.com/search?q="+sub+" "+kw)
        
        return render_template('admin.html',login=login, username=username, kind="books" ,content=Books.query.filter_by(uri=book.uri).all()
)

    sub="writing"
    title="Copypasta Publishing: Social Media Marketing"
    form = ReusableForm(request.form)
    url2 = 'https://www.reddit.com/api/trending_subreddits/.json?limit=100'
    
    data2= requests.get(url2, headers={'user-agent': 'scraper by /u/ciwi'}).json()
    print(data2)
    if request.method == 'POST':
        name=request.form['name']
        return redirect('/keywords/r/'+name)

    if form.validate():
        # Save the comment here.
        flash('Keywords from r/' + name)
    posts=[]
    subs1=Subreddits.query.all()
    data3=[]
    for sub2 in subs1:
        data3.append(sub2.sub) 
    subs=data3+data2["subreddit_names"]+["AskReddit","announcements","funny","pics","todayilearned","science","IAmA","blog","videos","worldnews","gaming","movies","Music","aww","news","gifs","askscience","explainlikeimfive","EarthPorn","books","television","LifeProTips","sports","DIY","Showerthoughts","space","Jokes","tifu","food","photoshopbattles","Art","InternetIsBeautiful","mildlyinteresting","GetMotivated","history","nottheonion","gadgets","dataisbeautiful","Futurology","Documentaries","listentothis","personalfinance","philosophy","nosleep","creepy","OldSchoolCool","UpliftingNews","WritingPrompts","TwoXChromosomes"]
    url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=10'
    data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()
    for link in data['data']['children']:
            
        phrasey=RedditPost()

        phrasey.uri="https://www.reddit.com/"+link['data']['permalink']
        phrasey.body=link['data']['title']
        posts.append(phrasey)
        #  phrases_string="\n".join(phrasey["body"])
   #print(phrases_string)

    #r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

    #r.extract_keywords_from_text(phrases_string)

    #phrases=r.get_ranked_phrases()
    title=title
    print(posts)
    return render_template('index.html',login=login, kind="books" ,username=username, form2=form2, subs=subs, phrases=posts, form=form, title=title)


@app.route('/keywords/r/<sub>', methods=["POST", "GET"])
def rake2(sub):
   post={}
   form2=PostForm()
   if form2.validate_on_submit():
      post[kw]=form2.kw
      post[sub]=form2.sub
      res = requests.post(url_for('botpost'),headers='Content-Type: application/json',data=json.dumps(post))

      return redirect(url_for('rake2', sub=sub))
   title="Reddit Influencers on r/"+sub
   url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=300'
   url2 = 'https://www.reddit.com/api/trending_subreddits/.json'
   form = ReusableForm(request.form)
   if request.method == 'POST':
       name=request.form['name']
       return redirect('/keywords/r/'+name)
   texts=[]
   if form.validate():
        # Save the comment here.
       flash('Keywords from r/' + name)   
   data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()
   data2 = requests.get(url2, headers={'user-agent': 'scraper by /u/ciwi'}).json()
   print(data2.keys())
   print(data2["subreddit_names"])
   if data:
       for link in data['data']['children']:
           uri=link['data']['permalink']
           title2=link['data']['title']
           p = Rake(min_length=2) # Uses stopwords for english from NLTK, and all puntuation characters.
           p.extract_keywords_from_text(link['data']['title'])
           p.extract_keywords_from_text(link['data']['selftext'])
            # To get keyword phrases ranked highest to lowest
           for post in p.get_ranked_phrases_with_scores():
               print(post)
               texts.append(RedditPost(uri=uri, body=post[1], title=title2, integer=int(post[0])))
   
   else:
       subs=data2["subreddit_names"]+["/r/AskReddit","announcements","funny","pics","todayilearned","science","IAmA","blog","videos","worldnews","gaming","movies","Music","aww","news","gifs","askscience","explainlikeimfive","EarthPorn","books","television","LifeProTips","sports","DIY","Showerthoughts","space","Jokes","tifu","food","photoshopbattles","Art","InternetIsBeautiful","mildlyinteresting","GetMotivated","history","nottheonion","gadgets","dataisbeautiful","Futurology","Documentaries","listentothis","personalfinance","philosophy","nosleep","creepy","OldSchoolCool","UpliftingNews","WritingPrompts","TwoXChromosomes"]

       return render_template('keywords.html',sub=sub,form=form,  form2=form2, subs=subs, phrases=phrasey, title="Subreddit not found.")
   texts=sorted(texts, key=attrgetter('integer'), reverse=True)
   print(texts)
   subs1=Subreddits.query.all()
   data3=[]
   for sub2 in subs1:
       data3.append(sub2.sub) 
       subs=data3+data2["subreddit_names"]+["AskReddit","announcements","funny","pics","todayilearned","science","IAmA","blog","videos","worldnews","gaming","movies","Music","aww","news","gifs","askscience","explainlikeimfive","EarthPorn","books","television","LifeProTips","sports","DIY","Showerthoughts","space","Jokes","tifu","food","photoshopbattles","Art","InternetIsBeautiful","mildlyinteresting","GetMotivated","history","nottheonion","gadgets","dataisbeautiful","Futurology","Documentaries","listentothis","personalfinance","philosophy","nosleep","creepy","OldSchoolCool","UpliftingNews","WritingPrompts","TwoXChromosomes"]
                # json={"first":first, "last"=last, "title":title,"desc":desc,"pseudonym":pseudonym}
                # return render_template('entries.html', entries=json
   return render_template('keywords.html',sub=sub,form=form,  form2=form2, phrases=texts, subs=subs, title=title)

    
    
@app.route('/keywords', methods=["POST", "GET"])
def kw():     
   sub=None
   url2 = 'https://www.reddit.com/api/trending_subreddits/.json'

   data2 = requests.get(url2, headers={'user-agent': 'scraper by /u/ciwi'}).json()
   subs=data2["subreddit_names"]+["/r/AskReddit","announcements","funny","pics","todayilearned","science","IAmA","blog","videos","worldnews","gaming","movies","Music","aww","news","gifs","askscience","explainlikeimfive","EarthPorn","books","television","LifeProTips","sports","DIY","Showerthoughts","space","Jokes","tifu","food","photoshopbattles","Art","InternetIsBeautiful","mildlyinteresting","GetMotivated","history","nottheonion","gadgets","dataisbeautiful","Futurology","Documentaries","listentothis","personalfinance","philosophy","nosleep","creepy","OldSchoolCool","UpliftingNews","WritingPrompts","TwoXChromosomes"]

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
   return render_template('keywords.html',sub=sub,subs=subs, form=form, phrases=texts, sort=sort, title=title)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")
@app.route('/websites')
def library():

    r=glob.glob("texts/*")
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
   kw=req.get('kw').split('|')
   this_bot = Bots.query.filter_by(username="caesarnaples2").first()
   try:
       client_id=this_bot.client_id
   except AttributeError:
       return redirect("register/app")
   secret=this_bot.secret
   password=this_bot.password
   username=this_bot.username
   reddit = praw.Reddit(client_id=client_id,
                            client_secret=secret, password=password,
                            user_agent='Copypasta', username=username)
     
     
   try:
       body="["+kw[1]+"]("+kw[2]+")"
       url=reddit.subreddit('copypastapublishin').submit(kw[0], selftext=body).permalink 

   except praw.exceptions.APIException:
       return redirect("admin/r/"+sub) 
   #reddit.subreddit('copypastapublishin').submit(f[0:300], url="https://www.reddit.com/search?q="+sub+" "+kw)
   s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   passlen = 12
   p =  "".join(random.sample(s,passlen ))
   if current_user.is_authenticated:
       username=current_user.username
   post=RedditPost(reddit_url=url, uri=p, title=kw[0],body=body, username=username)
   db.session.add(post)
   db.session.commit()
   
   return redirect('/admin?uri='+p)
