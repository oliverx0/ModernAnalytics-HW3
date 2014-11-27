from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from config import *
from code.utils import *
import numpy as np
import random

movies = load_balanced_movies(MOVIES_DATA, True)

decades = []
plots = []

for m in movies:
	decades.append(m['year'])

for p in movies:
	plots.append(m['summary'])

plot_cleanup(plots)

# perform vectorization using Count Vectorizer (counts # of times a word appears)
vectorizer = CountVectorizer(stop_words='english')
X_train = vectorizer.fit_transform(plots)

print vectorizer.get_feature_names()[0:20]

#training stage
naive_bayes = MultinomialNB()
naive_bayes = MultinomialNB().fit(X_train, decades)

#testing stage
Y_train = vectorizer.transform(plots)
prediction = naive_bayes.predict(Y_train)

# print "Accuracy: %0.2f%%" % (100 * naive_bayes.score(, Y_train))