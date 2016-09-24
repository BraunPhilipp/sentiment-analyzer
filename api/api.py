
"""
API HTTP Requests
"""

import urllib
import http.client
import json
from logger import logger
import requests

class api(object):

    def __init__(self):
        self.connection = http.client.HTTPConnection("API_DOMAIN", 80)
        self.headers = {"Content-type": "application/json", "Accept": "application/json"}
    def __del__(self):
        self.connection.close()

class tracker(api):

    def __init__(self):
        api.__init__(self)

    def create(self, keyword):
        data = {"keyword":keyword, "min_id":"0", "max_id":"0", "volume":"0"}
        json_data = json.dumps(data)
        self.connection.request("POST", "/api/trackers?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        print(response.read())

        if (response.status != 200):
            logger.log("API > Could not add Keyword")

    def update(self, id, min_id, max_id, volume):
        data = {"id":id, "min_id":min_id, "max_id":max_id, "volume":volume}
        json_data = json.dumps(data)
        self.connection.request("PUT", "/api/trackers?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        print(response.read())
        if (response.status != 200):
            logger.log("API > Could not update Keyword")

    def next(self):
        response = requests.get("http://API_DOMAIN/api/trackers/next?api_key=API_KEYWORD").json()
        return response[0]

    def get(self):
        data = requests.get("http://API_DOMAIN/api/trackers?api_key=API_KEYWORD").json()
        return data

    def delete(self, keyword):
        data = {"keyword":keyword}
        json_data = json.dumps(data)
        self.connection.request("DELETE", "/api/trackers?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        if (response.status != 200):
            logger.log("API > Could not delete Keyword")

class review(api):

    # http://localhost:3000/api/reviews
    # curl -i -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"text":"This is bad!", "category":"english", "score":"0"}' http://localhost:3000/api/reviews

    def __init__(self):
        api.__init__(self)

    def create(self, data):
        '''
        data = {'category':'...', 'text':'...', 'score':'...'}
        '''
        _data = {}
        _data['data'] = data
        json_data = json.dumps(_data)
        self.connection.request("POST", "/api/reviews?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        print(response.read())
        if (response.status != 200):
            logger.log("API > Failed to add Review")

    def search(self, category):
        response = requests.get("http://API_DOMAIN/api/reviews/search?q="+category+"&api_key=API_KEYWORD").json()
        data = [{'text':r['text'],'score':r['score']} for r in response]
        return data

class tweet_data(api):

    def __init__(self):
        api.__init__(self)

    def create(self, data):
        _data = {}
        _data['data'] = data
        json_data = json.dumps(_data)
        self.connection.request("POST", "/api/tweet_datums?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        print(response.read())
        if (response.status != 200):
            logger.log("API > Failed to add Tweets")

    def search(self, keyword):
        data = requests.get("http://API_DOMAIN/api/tweet_datums/search?q="+keyword+"&api_key=API_KEYWORD").json()
        return data

class tweet_volume(api):

    def __init__(self):
        api.__init__(self)

    def create(self, data):
        json_data = json.dumps(data)
        self.connection.request("POST", "/api/tweet_volumes?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        print(response.read())
        if (response.status != 200):
            logger.log("API > Failed to add Volume")

class tweet_sentiment(api):

    def __init__(self):
        api.__init__(self)

    def create(self, keyword, date, sentiment):
        data = {'keyword':keyword, 'date':date, 'sentiment':sentiment}
        json_data = json.dumps(data)
        self.connection.request("POST", "/api/tweet_sentiments?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        print(response.read())
        if (response.status != 200):
            logger.log("API > Failed to add Sentiment")

    def delete(self, keyword, date):
        data = {'keyword':keyword, 'date':date}

        json_data = json.dumps(data)
        self.connection.request("DELETE", "/api/tweet_sentiments?api_key=API_KEYWORD", json_data, self.headers)

        response = self.connection.getresponse()
        print(response.read())
        if (response.status != 200):
            logger.log("API > Could not delete Sentiment")

    # def delete(self, keyword, date):
    #     ## delete by date

#tracker().create('ruby')
#tracker().delete('ruby')
#review().create({'category':'en-us', 'text':'I dont like that!', 'score':'0'})
