import math
import re
from config import *
from code.utils import *

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
dictionary2 = {}
decades_count = {}
informative_words = {}
importance_dictionary = {}

#Initialize dictionary
init_decade = INITIAL_DECADE
while(init_decade <= FINAL_DECADE):
    dictionary[init_decade] = {}
    dictionary2[init_decade] = {}
    decades_count[init_decade] = 0
    informative_words[init_decade] = []
    importance_dictionary[init_decade] = {}
    init_decade += 10
    
counter = 0
for movie in movies_training:
    counter += 1
    print counter
    movie_summary = clean_str(movie['summary'])#.replace('[^\w\s]','').lower()
    movie_decade = movie['year']
    movie_bag = []
    decades_count[movie_decade] += 1
    for word in movie_summary.split():
        for decade in dictionary:
            if word not in dictionary[decade]:
                dictionary[decade][word] = 0
                dictionary2[decade][word] = 0
            else:
                if (movie_decade == decade):
                    if word not in movie_bag:
                        dictionary[decade][word] += 1
                        dictionary2[decade][word] += 1
                        movie_bag.append(word)

for decade in dictionary:
    for word in dictionary[decade]:
        temp = float(dictionary[decade][word])/decades_count[decade]
        if temp == 0:    
            dictionary[decade][word] = math.log(0.0001)
            dictionary2[decade][word] = 0.00001
        else:
            dictionary[decade][word] = math.log(temp)
            dictionary2[decade][word] = temp

for decade in decades_count:
    decades_count[decade] = float(decades_count[decade])/total_movies
    
for decade in dictionary:
    for word in dictionary2[decade]:
        prob = dictionary2[decade][word]
        min_prob = 999999
        for decade2 in dictionary2:
            if(dictionary2[decade2][word] < min_prob):
                min_prob = dictionary2[decade2][word]
                
        importance_dictionary[decade][word] = float(prob)/min_prob
        
for decade in decades_count:
    for i in range(100):
        word = keywithmaxval(importance_dictionary[decade])
        informative_words[decade].append(word)
        del importance_dictionary[decade][word]
        del dictionary[decade][word]

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

print "Correct: "+str(correct)
print "Incorrect: "+str(incorrect)
print "Accuracy: "+str(float(correct)/total_movies)
            
            
    
                
                

    
        

