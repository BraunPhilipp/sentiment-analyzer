from logger import logger
from api import api

## Tracker

#api.tracker().create('donald trump')
#api.tracker().delete('ruby')
#print(api.tracker().next())

## Reviews

# import reviews.walmart as walmart
#
# for i in range(1, 1000000):
#     rt = walmart.walmart().data
#     print(rt)
#
#     if len(rt) > 0:
#         api.review().create(rt)

#print(api.review().search('en-us'))

## Sentiment

# from sentiment import sentiment
#
# data = ['i love roses', 'dude this is really bad', 'i hate you', 'do not like this', """don't do it"""]
#
# for s in data:
#     print(s + str(sentiment.get(s)))

# print(api.tracker().next())


## Tweets

# from twitter import twitter
#
# track = api.tracker().next()
# twitter.twitter(track['keyword'], track['id'], track['min_id'], track['max_id']).loopTweets()
#


## 5 amazon

# import reviews.amazon as amazon
#
# for i in range(1, 1000000):
#     rt = amazon.amazon().search()
#     print(rt)
#
#     if len(rt) > 0:
#         mysql.reviews().add(rt)

#print(api.tweet_data().search('ruby'))
#print(api.tracker().get())
