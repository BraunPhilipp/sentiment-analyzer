from sklearn.naive_bayes import BernoulliNB
# from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer

from nltk import pos_tag
import nltk

import pickle

from api import api

vectorizer = CountVectorizer(min_df=3)
clf = BernoulliNB()

reviews = api.review().search('en-us')
#reviews = [{'review_text':review['review_text'].lower(), 'review_score':review['review_score']} for review in reviews]

corpus = []
ratings = []
for review in reviews:
    corpus.append(review['text'])
    ratings.append(review['score'])

# Bayesian Fitting
X = vectorizer.fit_transform(corpus).toarray()
Y = ratings

clf.fit(X, Y)

def get(text):
    text = nltk.word_tokenize(text.lower())
    text = [i[0] for i in pos_tag(text) if i[-1] != 'NN']
    text = ' '.join([i for i in text])

    #text = ''.join(text)

    return clf.predict(vectorizer.transform([text]))
