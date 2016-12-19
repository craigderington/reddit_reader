#! /usr/bin/python

from flask import Flask
from flask import render_template, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
import requests
import json
import datetime
import random

app = Flask(__name__)
mongo = PyMongo(app)

MONGODB_URI = "mongodb://localhost/"
MONGO_DBNAME = "app"

app.secret_key = os.urandom(50)

subreddits = {
    'Frontpage': 'FrontPage',
    'Explain Like Im 5': 'explainlikeimfive',
    'LifeProTips': 'LPT',
    'Data Is Beautiful': 'dataisbeautiful',
    'Technology': 'technology',
    'Mildly Interesting': 'mildlyinteresting',
    'Today I Learned': 'todayilearned',
    'Earth Porn': 'EarthPorn',
    'Old School School': 'OldSchoolCool',
    'Space': 'space',
    'Science': 'science',
}


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
        news_stories=news_stories,
        reddits=subreddits
    )


@app.route('/reddit/new')
def reddit_new():
    subreddit = random.choice(subreddits.values())
    url = 'http://www.reddit.com/r/' + str(subreddit) + '/.json'
    hdr = {'user-agent': 'gravity'}
    r = requests.get(url, headers=hdr)

    if r.status_code == 200:
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

        flash('The reddit database was successfully updated from /r/' + subreddit + '.')
        return redirect(url_for('reddit'))


@app.route('/reddit/<string:subreddit>', methods=['GET'])
def reddit_filter(subreddit):
    filter_result = mongo.db.reddit.find({'subreddit': subreddit}).sort([('created', -1)])
    return render_template(
        'subreddit.html',
        filter_result=filter_result,
        reddits=subreddits,
        reddit_cat=subreddit
    )


@app.route('/reddit/delete/<string:reddit_id>', methods=['GET'])
def reddit_delete(reddit_id):
    reddit_story = mongo.db.reddit.find_one({'_id': ObjectId(reddit_id)})
    if reddit_story:
        try:
            result = mongo.db.reddit.delete_one({'_id': ObjectId(reddit_id)})
        except ValueError as e:
            flash('The selected reddit article ID can not be found.', 'error')

        flash('The reddit article was successfully deleted...', 'success')
        return redirect(url_for('reddit'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
