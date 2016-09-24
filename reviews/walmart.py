import string
import numpy as np
import re
import urllib.request
from bs4 import BeautifulSoup
import time
import random
import string

from logger import logger

class walmart:
    """
    Returns walmart reviews in the following structure

    walmart(search_query).data
    data = [(title, score), (title, score), ...]
    """
    def __init__(self, query=""):
        self.query = query
        self.data = []
        # Internal Function
        self.search()

    def search(self):
        if (self.query == ""):
            self.query = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        try:
            page = urllib.request.urlopen("http://www.walmart.com/search/?query="+str(self.query), timeout=5)
            soup = BeautifulSoup(page, "html.parser")

            products = soup.find_all('div', class_='js-tile js-tile-landscape tile-landscape')

            for product in products:
                if (product.find('div', class_='stars stars-small tile-row') != None):
                    self.data += self.reviews("https://www.walmart.com/reviews/product/"+str(product['data-item-id']))
        except Exception as e:
            logger.log("WALMART > SEARCH > " + str(e))
            time.sleep(2)
            pass

    def reviews(self, url):
        # https://www.walmart.com/reviews/product/46784939
        res = []
        try:
            page = urllib.request.urlopen(url, timeout=5)
            soup = BeautifulSoup(page, "html.parser")
            product = soup.find('a', class_='review-product-name').text.lower()
            reviews = soup.find('div', class_='js-review-list')
            reviews = soup.find_all('div', class_='Grid customer-review js-customer-review')

            for review in reviews:
                title = review.find('div', class_='Grid-col u-size-10-12-m customer-review-title').text.lower().split()

                # title = [i[0] for i in pos_tag(title)]
                title = ' '.join([i for i in title if i not in product]).replace('.','')

                # text = review.find('p', class_='js-customer-review-text').text
                score = int(review.find('div', class_='stars customer-stars').find('span', class_='visuallyhidden').text[0])
                # Adding extra Rule for filtering
                if (1 < len(title) < 100 and (score == 1 or score == 5)):
                    res.append({'text' : str(title), 'score' : str(int(round((score-1)/4))), 'category' : 'en-us'})
            return res
        except Exception as e:
            logger.log("WALMART > REVIEWS > " + str(e))
            time.sleep(2)
            return res
