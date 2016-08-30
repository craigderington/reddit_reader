#! /usr/bin/python

from flask import Flask
from flask import render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

MONGODB_URI = "mongodb://localhost/"
MONGO_DBNAME = "test"


@app.route('/')
def hello():
    return "hello world"


@app.route('/test')
def test():
    return render_template(
        'default.html',
        foo=42
    )


@app.route('/reddit', methods=['GET'])
def reddit():
    news_stories = mongo.db.reddit.find()
    return render_template(
        'index.html',
        news_stories=news_stories
    )


@app.route('/reddit/new')
def reddit_new():
    doc = {
        'story': 'This is a new reddit story.',
        'url': 'http://www.reddit.com/r/technology/'
    }

    mongo.db.reddit.insert(doc)
    return redirect(url_for('test'))


if __name__ == '__main__':
    app.run()
