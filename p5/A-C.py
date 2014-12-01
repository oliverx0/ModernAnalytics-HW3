from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import random_projection
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import random_projection
from config import *
from utils import *
import numpy as np
import pandas as pd

# load and puts data and desired numpy format
movies = load_balanced_movies(MOVIES_DATA, False)
data = pd.DataFrame(movies)
pd.options.mode.chained_assignment = None  # default='warn'
summaries = data[['summary']]
summaries['summary'] = summaries['summary'].str.replace('[^\w\s]','').str.lower()  ## cleans out puncutation and characters
Y = np.array(data[['year']])
X = np.array(summaries['summary'])

# standard CountVectorizer for bag of words
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(X)
print "Old Shape Dim" 
print X.shape 

# uses random projections to reduce dimensionality
transformer = random_projection.SparseRandomProjection()
X_new = transformer.fit_transform(X)
print "New Shape Dim"
print X_new.shape 

# perform vectorization and dim reduction using Hashing Vectorizer (counts # of times a word appears)
# vectorizer = HashingVectorizer(stop_words='english')  # uses 100,000 word instances as k
# X = vectorizer.transform(X)

# instantiate scaling of data for preprocessing
X = StandardScaler(with_mean=False).fit_transform(X)

# splits training and test data equally
xtrain, xtest, ytrain, ytest = train_test_split(X, Y)

names = ["SGDClassifier", "Linear SVC", "RBF SVM", "PerceptronL1", "PerceptronL2", "Nearest Neighbors", "Random Forest"]
classifiers = [
	SGDClassifier(loss="hinge", penalty="l2"),
	LinearSVC(),
    SVC(kernel="rbf"),
    Perceptron(penalty='l1'),
    Perceptron(penalty='l2', n_iter=25),
    NearestNeighbors(n_neighbots=2),
    RandomForestClassifier(max_depth=5, n_estimators=10),
   	]

# fits chosen classifier on training data
for name, clf in zip(names, classifiers):
	print name
	clf.fit(xtrain, ytrain)
	print "Accuracy: %0.2f%%" % (100 * clf.score(xtest, ytest)) # Predict and score accuracy


 


