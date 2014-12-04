from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import random_projection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import random_projection
from config import *
from utils import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # load and puts data and desired numpy format
    movies = load_balanced_movies(MOVIES_DATA, False)  # True is for debugging
    data = pd.DataFrame(movies)
    pd.options.mode.chained_assignment = None  # default='warn'
    summaries = data[['summary']]
    summaries['summary'] = summaries['summary'].str.replace('[^\w\s]','').str.lower()  ## cleans out puncutation and characters
    Y = np.array(data[['year']])
    Y = np.ravel(Y)
    X = np.array(summaries['summary']) # converts to arrays

    n_features = [5000,20000,80000] # used for hashing vectorizer input
    n_components = np.int32(np.linspace(1000, 80000, 10)) #evaluates 10 diff component sizes equally spaced, for random proj
    performance = []

    # standard CountVectorizer for bag of words
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)
    print "Old Shape Dim" 
    print X.shape 

    transformer = random_projection.SparseRandomProjection()
    X_new = transformer.fit_transform(X)
    print "New Shape Dim"
    print X_new.shape 

    for n in n_components:
        transformer = random_projection.SparseRandomProjection(n_components=n)  # varying number of components
        X_new = transformer.fit_transform(X)
        X_new.toarray()
        X = StandardScaler(with_mean=False).fit_transform(X)
        xtrain, xtest, ytrain, ytest = train_test_split(X, Y)
        print "Ran Linear SVC with {} features".format(n)
        SVM = LinearSVC().fit(xtrain, ytrain)
        print "Accuracy: %0.2f%%" % (100 * SVM.score(xtest, ytest)) # Predict and score accuracy
        performance.append(100 * SVM.score(xtest, ytest))

    plt.plot(n_components, performance, linewidth=2.0)
    plt.title('Performance vs Dimensionality')
    plt.xlabel('Number of components for random projections')
    plt.ylabel('Accuracy')
    plt.savefig('5f.jpg')
    plt.show()



if __name__ == '__main__':
    main()