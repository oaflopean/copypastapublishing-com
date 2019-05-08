from flask import Flask, render_template, request, url_for, redirect
import ebooklib
from pymongo import MongoClient
from mongoengine import *
import json
import praw
import urllib.request
import requests
import glob
import random
from forms import SearchSub
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField, validators
from wtforms.validators import DataRequired, Email

from flask_wtf import FlaskForm
from wtforms import StringField
from rake_nltk import Rake
from wtforms.validators import DataRequired
app = Flask(__name__)
app.config["SECRET_KEY"]= 'my super secret key'.encode('utf8')
app.config['STATIC_FOLDER'] = 'static/'



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



def read_all():
    return json.dumps(db.Entries.find())

@app.route('/blog')
def blog():
    title="Editor Blog: Jordan Jones"

    return render_template('blog-index.html', title=title)

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

    url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=509'
    data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()
    for link in data['data']['children']:
        phrasey["body"].append(link['data']['title'])

    phrases_string=' '.join(phrasey["body"])
    print(phrases_string)

    r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

    r.extract_keywords_from_text(phrases_string)

    phrases=r.get_ranked_phrases()
    title=title
    return render_template('index.html', phrases=phrases, form=form, title=title)

@app.route('/keywords/r/<sub>/<sort>', methods=["POST", "GET"])
def rake1(sub, sort):
    form = ReusableForm(request.form)

    if request.method == 'POST':
        name=request.form['name']
        return redirect('/keywords/r/'+name)

    if form.validate():
        # Save the comment here.
        flash('Keywords from r/' + name)
    
    title="Reddit Influencers or r/"+sub
    phrasey={"titles":[],"text":[]}
    url = 'https://www.reddit.com/r/'+sub+'/'+sort+"/.json?limit=300"

    data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()
    print(data)
    for link in data['data']['children']:
        phrasey["text"].append(link['data']['title'])
        phrasey["text"].append(link['data']['selftext'])



    p = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

    p.extract_keywords_from_text(' '.join(phrasey['text']))

    texts=p.get_ranked_phrases() # To get keyword phrases ranked highest to lowest
    

            # json={"first":first, "last"=last, "title":title,"desc":desc,"pseudonym":pseudonym}
            # return render_template('entries.html', entries=json)

    return render_template('keywords.html',sub=sub, form=form, phrases=texts, sort=sort, title=title)

@app.route('/keywords/r/<sub>', methods=["POST", "GET"])
def rake2(sub):
    title="Reddit Influencers on r/"+sub
    phrasey={"titles":[],"text":[]}
    sort="new"
    url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=300'
    form = ReusableForm(request.form)

    if request.method == 'POST':
        name=request.form['name']
        return redirect('/keywords/r/'+name)

    if form.validate():
        # Save the comment here.
        flash('Keywords from r/' + name)
    data = requests.get(url, headers={'user-agent': 'scraper by /u/ciwi'}).json()
    print(data)
    if data['data']["children"]:

        for link in data['data']['children']:
            phrasey["text"].append(link['data']['title'])
            phrasey["text"].append(link['data']['selftext'])


    else:
        phrasey["text"]="There is no subreddit named "+sub
   
    p = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

    p.extract_keywords_from_text(' '.join(phrasey['text']))

    texts=p.get_ranked_phrases() # To get keyword phrases ranked highest to lowest
    
            # json={"first":first, "last"=last, "title":title,"desc":desc,"pseudonym":pseudonym}
            # return render_template('entries.html', entries=json)
    return render_template('keywords.html',sub=sub,form=form,  phrases=texts, sort=sort, title=title)
@app.route('/keywords', methods=["POST", "GET"])
def kw():    
    sub=None
    texts={}
    sort="new"
    form = ReusableForm(request.form)

    if request.method == 'POST':
        name=request.form['name']
        return redirect('/keywords/r/'+name)

    if form.validate():
        # Save the comment here.
        flash('Keywords from r/' + name)
    
    title="Reddit Influencers on Multiple Subreddits"
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

@app.route('/bot/r/<sub>/<kw>', methods=["GET"])
@app.route('/bot/search/<sub>/<kw>', methods=["GET"])

def botpost(sub, kw):
    reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                     client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$',
                     user_agent='Ravenclaw', username='caesarnaples2')
    
    
    message2 = reddit.subreddit('copypastapublishin').submit(sub, kw, send_replies=True)
    #reddit.subreddit('copypastapublishin').submit(f[0:300], url="https://www.reddit.com/search?q="+sub+" "+kw)
    
    return redirect('https://www.reddit.com/r/copypastapublishin/new')