import string
import math
import re
import datetime

import pymysql.cursors

from logger import logger

# Access Tokens
SERVER_IP = "MYSQL_IP"
SERVER_USER = "root"
SERVER_PASS = "MYSQL_PASSWORD"

class mysql(object):

    def __init__(self):
        self.connection = pymysql.connect(host= SERVER_IP, user= SERVER_USER, password= SERVER_PASS, db= 'wenti_db', charset= 'utf8mb4', cursorclass= pymysql.cursors.DictCursor)
        self.now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __del__(self):
        self.connection.close()

class reviews(mysql):

    def __init__(self):
        mysql.__init__(self)

    def add(self, rt):
        try:
            with self.connection.cursor() as cursor:
                # MYSQL Requests
                for r in rt:
                    cursor.execute("""INSERT INTO `wt_reviews` (`ID`, `review_text`, `review_category`, `review_score`) VALUES (DEFAULT, %s, %s, %s)""", (r['text'], r['category'], r['score']))
            self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > REVIEWS > ADD > " + str(e))
            pass

    def get(self, category):
        rt = []
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                cursor.execute("""SELECT `review_text`, `review_score` FROM `wt_reviews` WHERE `review_category` = %s""", category)
                rt = cursor.fetchall()
        except Exception as e:
            logger.log("MYSQL > REVIEWS > GET > " + str(e))
            pass

        return rt

class tracker(mysql):

    def __init__(self):
        mysql.__init__(self)

    def add(self, keyword):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""INSERT INTO `wt_tracker` (`ID`, `keyword`, `volume`, `min_id`, `max_id`, `created_at`, `updated_at`) VALUES (DEFAULT, %s, '0', '0', '0', %s, %s )""", (keyword, self.now, self.now))
            self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > TRACKER > ADD > " + str(e))
            pass

    def update(self, keyword, min_id, max_id):
        try:
            with self.connection.cursor() as cursor:
                # Get Old Min and Max ID
                cursor.execute("""SELECT `min_id`, `max_id`, `volume` FROM `wt_tracker` WHERE `keyword`= %s """, keyword)
                data = cursor.fetchone()
                # Update new IDs
                if (int(min_id) < data['min_id'] or data['min_id'] == 0):
                    cursor.execute("""UPDATE `wt_tracker` SET `min_id`= %s, `updated_at`= %s, `volume`= %s WHERE `keyword`= %s """, (min_id, self.now, data['volume']+1, keyword))
                if (int(max_id) > data['max_id'] or data['max_id'] == 0):
                    cursor.execute("""UPDATE `wt_tracker` SET `max_id`= %s, `updated_at`= %s, `volume`= %s WHERE `keyword`= %s """, (max_id, self.now, data['volume']+1, keyword))
            self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > TRACKER > UPDATE > " + str(e))
            pass

    def get(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""SELECT `keyword`, `volume`, `updated_at`, `min_id`, `max_id` FROM wt_tracker ORDER BY updated_at """)
                queue = cursor.fetchall()
            self.connection.commit()
            return queue
        except Exception as e:
            logger.log("MYSQL > TRACKER > GET > " + str(e))
            pass

    def remove(self, keyword):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""DELETE FROM wt_tracker WHERE `keyword` = %s""", (keyword,))
            self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > TRACKER > REMOVE > " + str(e))
            pass

class tweet_data(mysql):

    def __init__(self):
        mysql.__init__(self)

    def add(self, tweets):
        try:
            with self.connection.cursor() as cursor:
                # Remove Duplicates
                for tweet in tweets:
                    cursor.execute("""SELECT `tweet_id` FROM `wt_tweet_data` WHERE tweet_keyword= %s AND tweet_id= %s OR tweet_user_id= %s """, (tweet['query'], tweet['tweet_id'], tweet['user_id']))
                    dupl = cursor.fetchall()
                    if (len(dupl) > 0):
                        tweets.remove(tweet)
                # Add remaining entries
                for tweet in tweets:
                    cursor.execute("""INSERT INTO `wt_tweet_data` (`ID`, `tweet_id`, `tweet_date`, `tweet_text`, `tweet_lang`, `tweet_retweet_count`, `tweet_favorite_count`, `tweet_user_id`, `tweet_user_verified`, `tweet_sentiment`, `tweet_score`, `tweet_keyword`) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (tweet['tweet_id'], tweet['date'], tweet['text'], tweet['lang'], tweet['retweets'], tweet['favorites'], tweet['user_id'], tweet['verified'], tweet['sentiment'], tweet['score'], tweet['query']))
                self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > TWEET DATA > ADD > " + str(e))
            pass

    def get(self, query):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                cursor.execute("""SELECT `tweet_id`, `tweet_date`, `tweet_lang`, `tweet_retweet_count`, `tweet_favorite_count`, `tweet_user_id`, `tweet_user_verified`, `tweet_sentiment`, `tweet_score` FROM `wt_tweet_data` WHERE tweet_keyword= %s""", query)
                tweets = cursor.fetchall()
                return tweets
        except Exception as e:
            logger.log("MYSQL > TWEET DATA > GET > " + str(e))
            pass

class tweet_volume(mysql):

    def __init__(self):
        mysql.__init__(self)

    def add(self, volume):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""INSERT INTO `wt_tweet_volume` (`ID`, `keyword`, `date`, `volume`) VALUES (DEFAULT, %s, %s, %s)""", (volume['query'], volume['max_date'], volume['volume']))
                self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > TWEET VOLUME > ADD > " + str(e))
            pass

class tweet_sentiment(mysql):

    def __init__(self):
        mysql.__init__(self)

    def add(self, query, date, sentiment):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""INSERT INTO `wt_tweet_sentiment` (`ID`, `keyword`, `date`, `sentiment`) VALUES (DEFAULT, %s, %s, %s)""", (query, date, sentiment))
            self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > TWEET SENTIMENT > ADD > " + str(e))
            pass

    def remove(self, query, date):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""DELETE FROM `wt_tweet_sentiment` WHERE `keyword`=%s AND `date`=%s""", (query, date))
            self.connection.commit()
        except Exception as e:
            logger.log("MYSQL > TWEET SENTIMENT > REMOVE > " + str(e))
            pass
