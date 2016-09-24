from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

CONSUMER_KEY = "CONSUMER_KEY"
CONSUMER_SECRET = "CONSUMER_SECRET"
ACCESS_KEY = "ACCESS_KEY"
ACCESS_SECRET = "ACCESS_SECRET"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # Twitter Authentication
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    stream = Stream(auth, l)

    # Capture data of various keywords
    stream.filter(track=['python', 'javascript', 'ruby', 'c'])
