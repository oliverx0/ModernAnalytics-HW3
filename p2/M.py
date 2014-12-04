import math
import re
from config import *
from code.utils import *
import numpy as np
import matplotlib.pylab as plt

#Initialize list of decades
dec_list = []
dec_index = {}

#Load all the movies from the file 
movies = load_balanced_movies(MOVIES_DATA, False)

movies_test = []
movies_training = []

#Generate test set and training set
for i in range(len(movies)):
    if i%2 == 0:
        movies_training.append(movies[i])
    else:
        movies_test.append(movies[i])
        
total_movies = len(movies_training)

#Dictionary
dictionary = {}
decades_count = {}
predicted_decades = {}

#Initialize dictionary
counter = 0
init_decade = INITIAL_DECADE
while(init_decade <= FINAL_DECADE):
    dictionary[init_decade] = {}
    predicted_decades[init_decade] = {}
    dec_list.append(init_decade)
    decades_count[init_decade] = 0
    dec_index[counter] = init_decade
    init_decade += 10
    counter += 1
    
#Initialize predicted decades
for d in predicted_decades:
    for d2 in predicted_decades:
        predicted_decades[d][d2] = 0

#Load all decades and words combinations
counter = 0
for movie in movies_training:
    counter += 1
    print counter
    movie_summary = clean_str(movie['summary'])#.replace('[^\w\s]','').lower()
    movie_decade = movie['year']
    decades_count[movie_decade] += 1
    for word in movie_summary.split():
        for decade in dictionary:
            if word not in dictionary[decade]:
                dictionary[decade][word] = 0
            else:
                if (movie_decade == decade):
                        dictionary[decade][word] += 1

#Calculate P(X|Y)                                           
for decade in dictionary:
    for word in dictionary[decade]:
        temp = float(dictionary[decade][word])/decades_count[decade]
        if temp == 0:    
            dictionary[decade][word] = math.log(0.0001)
        else:
            dictionary[decade][word] = math.log(temp)

#Calculate P(Y)
for decade in decades_count:
    decades_count[decade] = float(decades_count[decade])/total_movies

#Test classifier
correct = 0
incorrect = 0
counter = 0
for movie in movies_test:
    counter += 1
    print counter
    final_prob = {}
    movie_summary = movie['summary'].replace('[^\w\s]','').lower()
    movie_decade = movie['year']
    for decade in dictionary:
        
        final_prob[decade] = math.log(decades_count[decade])
        for word in movie_summary.split():
            if word not in dictionary[decade]:
                final_prob[decade] += math.log(0.0001)
            else:
                final_prob[decade] += dictionary[decade][word]
    
    predicted = keywithmaxval(final_prob)
    if predicted == movie_decade:
        correct += 1
    else:
        incorrect += 1
    
    predicted_decades[predicted][movie_decade] += 1

#Initialize confusion matrix
matrix = np.zeros((len(dec_list),len(dec_list)))

#Load confusion matrix
for i in range(len(dec_list)):
    for j in range(len(dec_list)):
        matrix[i][j] = predicted_decades[dec_index[i]][dec_index[j]]

#Load visualization
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_aspect('equal')
ax.set_xticklabels(np.arange(INITIAL_DECADE, FINAL_DECADE + 10, 10))
ax.set_yticklabels(np.arange(INITIAL_DECADE, FINAL_DECADE + 10, 10))
ax.set_xticks(np.arange(matrix.shape[1]) + 0.5, minor=False)
ax.set_yticks(np.arange(matrix.shape[0]) - 0.5, minor=False)
plt.title('Confusion Matrix')
plt.xlabel('Real Decade')
plt.ylabel('Predicted Decade')
plt.imshow(matrix, interpolation='nearest', cmap='jet')
plt.colorbar()
plt.show() 
plt.savefig(FIGURES+"Confusion Matrix")    