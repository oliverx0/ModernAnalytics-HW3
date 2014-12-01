from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from config import *
from utils import *
import numpy as np
import pandas as pd
import random

movies = load_balanced_movies(MOVIES_DATA, True)
data = pd.DataFrame(movies)

summaries = data[['summary']]
summaries['summary'] = summaries['summary'].str.replace('[^\w\s]','').str.lower()  ## cleans out puncutation and characters and lower case
Y = data[['year']]

print summaries.summary
summaries.summary


# perform vectorization using Count Vectorizer (counts # of times a word appears)
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(summaries.summary)

# print vectorizer.get_feature_names()[10:]

## splits test and training data
xtrain, xtest, ytrain, ytest = train_test_split(X, Y)
## fits NB on training data
bayes = MultinomialNB().fit(xtrain, ytrain)

## Predict and score accuracy
print "Accuracy: %0.2f%%" % (100 * bayes.score(xtest, ytest))


