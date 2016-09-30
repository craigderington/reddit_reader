#### Simple Reddit Reader
Simple Reddit Reader using Flask and MongoDB.

* Flask
* MongoDB
* PyMongo
* Bootstrap

I love to read reddit.  I'm on the reddit website daily.  A majority of my news and information comes from reddit.
But let's face it, their website looks awful.  Like a reddit'er threw up their sushi lunch all over it.

To make reading reddit a bit more pleasurable, I have created this simple reddit reader.

The subreddits I read most regularly are stored as a dictionary in app.py.

I display the keys for the subreddit dict in the sidebar navigation as a means to filter the reddit data.  I can pass the subreddit filter to the reddit_filter route and reduce the number of articles returned in the view.

You can also delete articles and duplicate entries.

TODO:
* improve filter
* sort options
* rework the get new stories function so it's not just a random choice of subreddits.
