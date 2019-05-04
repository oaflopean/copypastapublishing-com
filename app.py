from flask import Flask, render_template, request, url_for, redirect
import ebooklib
from pymongo import MongoClient
from mongoengine import *
import json
import praw
import urllib.request
import requests

from forms import SearchSub
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

from flask_wtf import FlaskForm
from wtforms import StringField
from rake_nltk import Rake
from wtforms.validators import DataRequired
app = Flask(__name__)
app.config["SECRET_KEY"]= 'my super secret key'.encode('utf8')
app.config['STATIC_FOLDER'] = 'static/'



connect("partners", host='178.128.171.115', port=27017, username="oaflopean", password="99bananas", authentication_source="admin")
conn = MongoClient(host='178.128.171.115',port=27017)
db = conn['partners']
collection = db['Entries']
#
# class ReusableForm(Form):
#     name = TextField('Name:', validators=[validators.required()])
#
# # Data to serve with our API
# class Entry(Form):
#     first=TextField('first:', validators=[validators.required()])
#     last=TextField('last:', validators=[validators.required()])
#     title=TextField('title:', validators=[validators.required()])
#     desc=TextField('desc:', validators=[validators.required()])
#     pseudonym=TextField('pseudonym:', validators=[validators.required()])


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
    title="Copypasta Publishing: Influencer Results: "+sub

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
    title="Copypasta Publishing: Social Media Publishing: Keywords from r/Writing"
    return render_template('index.html', phrases=phrases, title=title)

@app.route('/keywords/r/<sub>/<sort>', methods=["GET"])
def rake1(sub, sort):
    title="Copypasta Publishing: Influencer Results: r/"+sub
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

    return render_template('keywords.html',sub=sub,  phrases=texts, sort=sort, title=title)

@app.route('/keywords/r/<sub>', methods=["GET"])
def rake2(sub):
    title="Copypasta Publishing: Influencer Results: r/"+sub
    phrasey={"titles":[],"text":[]}
    sort="new"
    url = 'https://www.reddit.com/r/'+sub+'/new/.json?limit=300'

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

    return render_template('keywords.html',sub=sub,  phrases=texts, sort=sort, title=title)
@app.route('/keywords', methods=["GET"])
def kw():    
    sub=None
    texts={}
    sort="new"
    title="Keywords on reddit.com Communities"
    return render_template('keywords.html',sub=sub,  phrases=texts, sort=sort, title=title)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

@app.route('/bot/r/<sub>/<kw>', methods=["GET"])
def botpost(sub, kw):
    reddit = praw.Reddit(client_id='FCBZa-yDqRLNag',
                     client_secret="ggD5MpCO7cQxbScgXaNmNydxPkk", password='AptCmx4$',
                     user_agent='Ravenclaw', username='caesarnaples2')

    reddit.subreddit("copypastapublishin").submit("We found something interesting on "+sub+": "+kw.replace(' ',""), url="https://www.reddit.com/r/"+sub)
    return render_template('index.html', title="Welcome Back")