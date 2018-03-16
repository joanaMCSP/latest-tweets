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
    """"
    get 100 latest tweets
    """
    return json.dumps(get_latest())

@app.route('/trump/popularity', methods=["GET"])
def popularity():
    """"
    get 100 latest tweets ordered by number of likes
    """
    key = 'trump_popularity'
    latest = load_from_cache(key)
    if latest is None :
        latest = get_latest()
        latest.sort(key=lambda x: x['favorite_count'], reverse=True)
        add_to_cache(key, latest)
    return json.dumps(latest)

@app.route('/trump/activity', methods=["GET"])
def activity():
    """"
    get 5 with most recent retweet from 100 latest tweets
    """
    key = 'trump_activity'
    activity = load_from_cache(key)
    if activity is None:
        activity = get_latest()[:5]
        last_retweeted = {}
        for tweet in activity:
            #returns most recent retweets of the tweet specified by the id parameter
            try:
                latest_retweets = api.retweets(tweet['id'], 1)
            except TweepError as e:
                print('Failed to get data. Status code: ', e.message[0]['code'])
            if(latest_retweets):
                created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(latest_retweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                last_retweeted[created_at] = tweet
                
        latest = [key for key in last_retweeted].sort(reverse=True)
        activity = [last_retweeted[tweet] for tweet in latest]
        add_to_cache(key, activity)
    return json.dumps(activity)

def get_latest():
    key = 'trump_latest'
    latest = load_from_cache(key)
    if latest is None :
        try:
            latest = api.user_timeline(screen_name = config.USERNAME, count = config.NUMBER_OF_TWEETS)
        except TweepError as e:
            print('Failed to get data. Status code: ', e.message[0]['code'])
        add_to_cache(key, latest)
    return latest

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=config.DEBUG)
