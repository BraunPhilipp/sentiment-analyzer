#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oauth2 as oauth
import json
import time
import sys

import string
import pandas as pd


CONSUMER_KEY = "CONSUMER_KEY"
CONSUMER_SECRET = "CONSUMER_SECRET"
ACCESS_KEY = "ACCESS_KEY"
ACCESS_SECRET = "ACCESS_SECRET"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

def convert_twitter_date(date_string):
    """
    Converts a Twitter date with the format "Thu Jan 28 21:25:53 +0000 2016" to a panda
    datetime object.
    """
    month_dict = { "Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07",
        "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12" }

    # Thu Jan 28 21:25:53 +0000 2016
    date = date_string.split(" ")[1:]
    date[0] = month_dict[date[0]]
    del date[3]
    date_string = ":".join(date)

    # Convert to Pandas
    timestamp = pd.to_datetime(date_string, format='%m:%d:%H:%M:%S:%Y')

    return timestamp

def get_twitter_data(search_query, max_id = 0):
    """
    Actively gets twitter data before a certain max_id. search_query defines the used keyword.
    The function returns max_id and a dictionary of the data received for each tweet sorted by timestamp.
    """

    tweets_list = {}

    # Handling First Data Call
    if ( max_id == 0 ):
        twitter_data = "https://api.twitter.com/1.1/search/tweets.json?q="+search_query+"&result_type=mixed&count=100"
    else:
        twitter_data = "https://api.twitter.com/1.1/search/tweets.json?q="+search_query+"&since_id=0&max_id="+str(max_id)+"&result_type=mixed&count=100"

    response, data = client.request(twitter_data)

    data = json.loads(data.decode("utf-8"))

    temp_max_id = 0

    for tweet in data["statuses"]:
        # https://dev.twitter.com/rest/reference/get/search/tweets
        if ( temp_max_id == 0 ):
            temp_max_id = tweet["id"]
        elif ( tweet["id"] < temp_max_id ):
            temp_max_id = tweet["id"]

        tweet_dict = { "id" : tweet["id"], "text" : tweet["text"], "lang" : tweet["lang"], "retweet_count" : tweet["retweet_count"],
            "followers" : tweet["user"]["followers_count"], "following" : tweet["user"]["friends_count"], "verified" : tweet["user"]["verified"],
            "user_id" : tweet["user"]["id_str"], "status_count" : tweet["user"]["statuses_count"] }

        timestamp = convert_twitter_date(tweet["created_at"])
        tweets_list[timestamp] = tweet_dict

    return max_id, tweets_list


    if ( temp_max_id < max_id or max_id == 0 ):
        # Necessary to prevent reaching rate limits
        time.sleep(5)
        # Recursive Call for previous Twitter Data
        get_twitter_data(search_query, temp_max_id-1)

    return max_id, tweets_list
