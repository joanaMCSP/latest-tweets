from flask import Flask
from helpers import *

import tweepy
import json
import redis
import time
import config

app = Flask(__name__)
cache = connect_to_redis()

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN_KEY, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

@app.route('/trump', methods=["GET"])
def latest():
    return json.dumps(get_latest())

#get latest ordered by number of likes
@app.route('/trump/popularity', methods=["GET"])
def popularity():
    key = 'trump_popularity'
    latest = load_from_cache(key)
    if latest is None :
        latest = get_latest()
        latest.sort(key=lambda x: x['favorite_count'], reverse=True)
        add_to_cache(key, latest)
    return json.dumps(latest)

#get latest with most recent retweet
@app.route('/trump/activity', methods=["GET"])
def activity():
    key = 'trump_activity'
    activity = load_from_cache(key)
    if activity is None:
        activity = get_latest()[:5]
        tweet_with_latest_retweet = {}
        for tweet in activity:
            #returns most recent retweets of the tweet specified by the id parameter
            latest_retweets = api.retweets(tweet['id'], 1)
            if(latest_retweets):
                created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(latest_retweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                tweet_with_latest_retweet[created_at] = tweet
        latest = [key for key in tweet_with_latest_retweet]
        latest.sort(reverse=True)
        activity = [tweet_with_latest_retweet[tweet] for tweet in latest]
        add_to_cache(key, activity)
    return json.dumps(activity)

def get_latest():
    key = 'trump_latest'
    latest = load_from_cache(key)
    if latest is None :
        latest = api.user_timeline(screen_name = config.USERNAME, count = config.NUMBER_OF_TWEETS)
        add_to_cache(key, latest)
    return latest

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=config.DEBUG)
