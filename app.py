from flask import Flask, render_template, request
import ebooklib
from pymongo import MongoClient
from mongoengine import *
import json

from flask_wtf import FlaskForm
from wtforms import StringField
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
    # Create the list of people from our data



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
    title="Copypasta Publishing: Bridges and Roads"
    # if request.method == 'POST':
    #     form = Entry(request.form)
    #
    #     first=request.form['first']
    #     last=request.form['last']
    #     title=request.form['title']
    #     desc=request.form['desc']
    #     pseudonym=request.form['pseudonym']
    #
    #
    # # Save the comment here.
    # #    if form.validate():

            # json={"first":first, "last"=last, "title":title,"desc":desc,"pseudonym":pseudonym}
            # return render_template('entries.html', entries=json)

    if request.method == "GET":
        return render_template('index.html', title=title)
    

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

