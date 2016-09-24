from logger import logger
from api import api
from twitter import twitter
from datetime import datetime
import urllib

import pandas as pd
import numpy as np

import sys

import reviews.walmart as walmart

def compress(query):
    # COMPRESS SENTIMENT
    tweets = api.tweet_data().search(query)

    # handle currently no data
    if len(tweets) < 1:
        return

    tweets = pd.DataFrame(tweets).dropna()
    tweets.index = tweets['tweet_date'].apply(lambda x: datetime.strptime(x,"%Y-%m-%dT%H:%M:%S.%fZ"))

    def weighted_mean(arr):
        score = [float(score) for score in arr['tweet_score']]
        sentiment = [float(sentiment) for sentiment in arr['tweet_sentiment']]

        return ( np.sum([ i*j for i,j in zip(score, sentiment) ]) / np.sum(score) )

    print(tweets)

    tweets = tweets.resample('D', how=weighted_mean)['tweet_sentiment']

    for date, sentiment in tweets.items():
        sentiment = 1000*round(sentiment,3)
        if(sentiment != 0):
            api.tweet_sentiment().delete(query, str(date))
            api.tweet_sentiment().create(query, str(date), str(sentiment))
        else:
            print("Could not add empty Sentiment")

def get_tweets():
    while 1:
        # Get Old Tweets
        track = api.tracker().next()
        track['keyword'] = urllib.parse.quote_plus(track['keyword'])
        print("> " + str(track['keyword']))
        twitter.twitter(track['keyword'], track['id'], track['min_id'], track['max_id'], 5).loopTweets()

        # Get Recent Tweets
        track = api.tracker().next()
        print("> " + str(track['keyword']))
        twitter.twitter(track['keyword'], 0, 0, 5).loopTweets()

def get_sentiment():
    while 1:
        tracker = api.tracker().get()

        for track in tracker:
            print("> " + track['keyword'])
            compress(track['keyword'])

def add_keyword(keyword):
    api.tracker().create(keyword)

def remove_keyword(keyword):
    api.tracker().delete(keyword)

def get_reviews():
    for i in range(1, 1000000):
        rt = walmart.walmart().data
        print(rt)

        if len(rt) > 0:
            api.review().create(rt)

# Option Selection
opt = sys.argv[1]

if opt == '--tweets':
    get_tweets()
elif opt == '--sentiment':
    get_sentiment()
elif opt == '--keyword_add':
    add_keyword(sys.argv[2])
elif opt == '--keyword_remove':
    remove_keyword(sys.argv[2])
elif opt == '--reviews':
    get_reviews()
else:
    print('Please select an option')
