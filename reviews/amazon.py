import string
import numpy as np
import re
import urllib.request
from bs4 import BeautifulSoup
import time
import random
import string

from logger import logger

class amazon:

    def __init__(self, query=""):
        self.query = query
        self.data = []
        # Internal Function
        self.search()

    def search(self):
        if (self.query == ""):
            self.query = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
        try:
            # Get possible Search Items
            page = urllib.request.urlopen("http://www.amazon.com/s/ref=nb_sb_noss?field-keywords=" + self.query, timeout=5)
            soup = BeautifulSoup(page, "html.parser")

            products = soup.find_all('li', class_='s-result-item celwidget')

            link_list = []

            for product in products:
                bar = product.find('div', class_='a-row a-spacing-mini')
                rating = bar.find('a', class_='a-size-small a-link-normal a-text-normal')

                if (rating != None):
                    if (1 < len(rating.text) < 5):
                        link_list.append('http://www.amazon.com/product-reviews/' + rating['href'].split('/')[-1])

            for link in link_list:
                page = urllib.request.urlopen(link, timeout=5)
                soup = BeautifulSoup(page, "html.parser")

                reviews = soup.find_all('div', class_='a-section review')

                for review in reviews:
                    title = review.find('a', class_='a-size-base a-link-normal review-title a-color-base a-text-bold').text
                    score = int(review.find('span', class_='a-icon-alt').text[0])

                    self.data.append({'text':title, 'score':int((score-1)/4), 'category':'AMAZON/EN'})

            return self.data

        except Exception as e:
            logger.log(str(e))
            pass
