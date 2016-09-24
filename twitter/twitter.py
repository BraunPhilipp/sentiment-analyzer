import string
import random
import math
import re
import datetime
import time

import numpy as np
import pandas as pd

import requests
import json
from bs4 import BeautifulSoup

import pymysql.cursors

import nltk

from logger import logger
from sentiment import sentiment

#from mysql import mysql
from api import api

def convertDate(ms):
    return datetime.datetime.fromtimestamp(int(ms)/1000.0)

def avgDate(dates):
    sec = [time.mktime(d.timetuple()) for d in dates]
    mean = datetime.datetime.fromtimestamp(np.mean(sec)).strftime("%Y-%m-%d %H:%M:%S")
    return mean

class twitter:
    def __init__(self, query, query_id, min_id=0, max_id=0, reqst=10):
        self.min_id = min_id
        self.max_id = max_id
        self.query = query
        self.query_id = query_id
        self.reqst = reqst # 0 for realtime

    def getTweets(self):
        try:
            headers = {'user-agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
            if (self.min_id == 0 and self.max_id == 0):
                response = requests.get("https://twitter.com/i/search/timeline?lang=en&src=typd&include_available_features=1&include_entities=1&vertical=default&reset_error_state=true&q="+str(self.query), headers=headers, timeout=20)
            else:
                response = requests.get("https://twitter.com/i/search/timeline?lang=en&src=typd&include_available_features=1&include_entities=1&vertical=default&reset_error_state=true&q="+str(self.query)+"&max_position=TWEET-"+str(self.min_id)+"-"+str(self.max_id)+"-BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", headers=headers, timeout=20)

            # print("https://twitter.com/i/search/timeline?lang=en&f=tweets&q="+str(query)+"&max_position=TWEET-"+str(min_id)+"-"+str(max_id)+"-BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

            # print(response.content)
            data = response.json()
            # print(data)

            data = data["items_html"]
            soup = BeautifulSoup(data, "html.parser")
            
            # tweets = soup.find_all('div', class_="tweet original-tweet js-original-tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable ")
            tweets = soup(attrs={'class': 'original-tweet'})

            tweet_list = []

            for tweet in tweets:
                try:
                    #print(tweet)
                    text = tweet.find('p', class_='TweetTextSize js-tweet-text tweet-text').text
                    regex = re.compile('data-time-ms="(.*?)"')
                    date = regex.search(str(tweet)).group(1)
                    date = str(convertDate(date))
                    retweets = tweet.find_all('span', class_='ProfileTweet-actionCount')[0]['data-tweet-stat-count']
                    favorites = tweet.find_all('span', class_='ProfileTweet-actionCount')[1]['data-tweet-stat-count']
                    user_id = tweet.find('a', class_='account-group js-account-group js-action-profile js-user-profile-link js-nav')['data-user-id']
                    lang = tweet.find('p', class_='TweetTextSize js-tweet-text tweet-text')['lang']
                    regex = re.compile('data-tweet-id="(.*?)"')
                    tweet_id = regex.search(str(tweet)).group(1)
                    verified = '1' if (tweet.find('span', class_='Icon Icon--verified Icon--small') != None) else '0'
                    process = ' '.join(nltk.word_tokenize(text.lower()))
                    sentm = str(sentiment.get(process)[0])
                    score = str(int(1+math.log(1+int(retweets)+int(favorites)+int(verified))))

                    tweet_dict = { 'tweet_text':text, 'tweet_date':date, 'tweet_retweet_count':retweets, 'tweet_favorite_count':favorites, 'tweet_user_id':user_id, 'tweet_lang':lang, 'tweet_id':tweet_id, 'tweet_user_verified':verified, 'tracker_id':self.query_id, 'tweet_sentiment':sentm, 'tweet_score':score }
                    tweet_list.append(tweet_dict)
                except Exception as e:
                    logger.log("TWITTER > " + str(e))
                    continue
            return tweet_list
        except Exception as e:
            time.sleep(5)
            logger.log("TWITTER > GET TWEETS > MIN_ID:"+str(self.min_id)+" MAX_ID:"+str(self.max_id)+" STATUS:TIMEOUT_ERROR")
            self.getTweets()

    def loopTweets(self):
        """
        Add Tweets to MYSQL Database
        """
        delta = 100 # default
        while int(self.min_id) > 164498184868081664 or int(self.min_id) == 0:
            print("Collecting Tweets ...")
            tweets = self.getTweets()

            # Check if tweet_ids empty > min_id minus delta
            if (tweets == None or len(tweets) < 2):
                print("No Tweets Error ...")
                logger.log("TWITTER > LOOP TWEETS > MIN_ID:"+str(self.min_id)+" MAX_ID:"+str(self.max_id)+" STATUS:NO_TWEETS_ERROR")
                # Will only fix the error for older tweets
                if self.min_id != 0 and self.max_id != 0:
                    self.max_id = int(self.min_id) - delta
                    self.min_id = int(self.min_id) - delta
            else:
                tweet_ids = [int(val['tweet_id']) for val in tweets]
                tweet_dts = [datetime.datetime.strptime(val['tweet_date'], "%Y-%m-%d %H:%M:%S") for val in tweets]

                tweet_id_range = max(tweet_ids) - min(tweet_ids)
                tweet_dt_range = (tweet_dts[0] - tweet_dts[-1]).total_seconds() + 1

                #self.min_id = min(tweet_ids)
                #self.max_id = max(tweet_ids)

                volume = int(tweet_id_range / (tweet_dt_range * 1000 + 1))

                num_tweets = int((24*60*60) * (tweet_id_range / tweet_dt_range)) # Number of tweets each day

                delta = int(num_tweets/self.reqst)

                if self.min_id != 0 and self.max_id != 0:
                    self.min_id = int(self.min_id) - delta # Get next ID
                    self.max_id = int(self.max_id) - delta
                else:
                    self.min_id = min(tweet_ids)
                    self.max_id = max(tweet_ids)

                # Get Average Date and Save Volume
                vol_dict = {'tracker_id':self.query_id, 'date':avgDate(tweet_dts), 'volume':volume}
                #mysql.tweet_volume().add(vol_dict)
                api.tweet_volume().create(vol_dict)
                # Log
                logger.log("TWITTER > MIN_ID:"+str(self.min_id)+" MAX_ID:"+str(self.max_id)+" STATUS:SUCCESS DATE:"+str(tweet_dts[-1]))
                # Save Tweets
                print("Saving Tweets ...")
                l_tweets = [val for val in tweets if val['tweet_lang'] == 'en' and 'http' not in val['tweet_text']]
                #mysql.tweet_data().add(l_tweets)
                api.tweet_data().create(l_tweets)
                #mysql.tracker().update(self.query, self.min_id, self.max_id)
                api.tracker().update(self.query_id, self.min_id, self.max_id, len(tweet_ids))
                # TIME SLEEP IS KEY!!!!
                time.sleep(5)
