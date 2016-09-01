#! /usr/bin/python

from flask import Flask
from flask import render_template, redirect, url_for
from flask_pymongo import PyMongo
import os
import requests
import json
import datetime

app = Flask(__name__)
mongo = PyMongo(app)

MONGODB_URI = "mongodb://localhost/"
MONGO_DBNAME = "app"


@app.route('/')
def index():
    welcome_message = "Select a subreddit to view..."
    return render_template(
        'index.html',
        welcome_message=welcome_message
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = mongo.db.users.find()
    return render_template(
        'login.html',
        user=user
    )


@app.route('/test')
def test():
    return render_template(
        'default.html',
        foo=42
    )


@app.route('/reddit', methods=['GET'])
def reddit():
    news_stories = mongo.db.reddit.find().sort([('created', -1)])
    return render_template(
        'index.html',
        news_stories=news_stories
    )


@app.route('/reddit/new')
def reddit_new():
    url = 'http://www.reddit.com/r/technology/.json'
    hdr = {'user-agent': 'r_superbot by gravity'}
    r = requests.get(url, headers=hdr)
    parsed = r.json()
    for item in parsed['data']['children']:
        structure = {
            'id': item['data']['id'],
            'subreddit': item['data']['subreddit'],
            'title': item['data']['title'],
            'link': item['data']['url'],
            'name': item['data']['name'],
            'likes': item['data']['likes'],
            'domain': item['data']['domain'],
            'created': datetime.datetime.fromtimestamp(item['data']['created'])
        }

        mongo.db.reddit.insert(structure)

    return redirect(url_for('reddit'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
