from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from config import *
from utils import *
import numpy as np
import pandas as pd
import random

movies = load_balanced_movies(MOVIES_DATA, False)
data = pd.DataFrame(movies)

summaries = data[['summary']]
pd.options.mode.chained_assignment = None  # default='warn'
summaries['summary'] = summaries['summary'].str.replace('[^\w\s]','').str.lower()  ## cleans out puncutation and characters and lower case
Y = data[['year']]
Y = np.ravel(Y)

# perform vectorization using Count Vectorizer (counts # of times a word appears)
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(summaries.summary)

## splits test and training data
xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=0.5) ## split evenly test and training data

## fits NB on training data
bayes = MultinomialNB().fit(xtrain, ytrain)

## Predict and score accuracy
print "Accuracy: %0.2f%%" % (100 * bayes.score(xtest, ytest))


