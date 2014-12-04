from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import random_projection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import RidgeClassifier  
from sklearn import random_projection
from config import *
from utils import *
import numpy as np
import pandas as pd

def main(output=RESULTS):
    # change ROOT ID in config.py to your computer's path so that is writes to correct file
    # load and puts data and desired numpy format
    movies = load_balanced_movies(MOVIES_DATA, False) # True is for debugging
    data = pd.DataFrame(movies)
    pd.options.mode.chained_assignment = None  # default='warn' ignore
    summaries = data[['summary']]
    summaries['summary'] = summaries['summary'].str.replace('[^\w\s]','').str.lower()  ## cleans out puncutation and characters
    Y = np.array(data[['year']])
    Y = np.ravel(Y)
    X = np.array(summaries['summary'])

    # standard CountVectorizer for bag of words
    # vectorizer = CountVectorizer()
    # X = vectorizer.fit_transform(X)

    # print "Old Shape Dim" 
    # print X.shape 

    # uses random projections to reduce dimensionality
    # transformer = random_projection.SparseRandomProjection()
    # X_new = transformer.fit_transform(X)
    # print "New Shape Dim"
    # print X_new.shape 

    # perform vectorization and dim reduction using Hashing Vectorizer (counts # of times a word appears)
    vectorizer = HashingVectorizer(stop_words='english', n_features=80000)  # uses 80,000 word instances as k
    X = vectorizer.transform(X)

    # instantiate scaling of data for preprocessing
    X = StandardScaler(with_mean=False).fit_transform(X)

    # splits training and test data equally
    xtrain, xtest, ytrain, ytest = train_test_split(X, Y)

    names = ["SGDClassifier", "Linear SVC", "SVC Kernel RBF", "PerceptronL1", "PerceptronL2", "Nearest Neighbors", "Ridge Classifier"] # 
    classifiers = [
        SGDClassifier(loss="hinge", penalty="l2"),
        LinearSVC(),
        SVC(kernel="rbf"),
        Perceptron(penalty='l1'),
        Perceptron(penalty='l2', n_iter=25),
        KNeighborsClassifier(),
        RidgeClassifier(),
        ]

    print "Calculating accuracies"
    # fits chosen classifier on training data
    for name, clf in zip(names, classifiers):
        print name
        clf.fit(xtrain, ytrain)
        print "Accuracy: %0.2f%%" % (100 * clf.score(xtest, ytest)) # Predict and score accuracy

        with open(output, "a+") as outputFile:  # write results to file 
            score = 100 * clf.score(xtest, ytest) 
            outputFile.write("Ran classifier {}    ".format(name) + '\n'
            " Achieved accuracy {}   ".format(score) )

if __name__ == '__main__':
    main()