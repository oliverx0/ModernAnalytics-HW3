import math
import re
from config import *
from code.utils import *


def find_min_prob(word, diction):
    min_prob = 99999999
    for decade in diction:
        if diction[decade][word] < min_prob:
            min_prob = diction[decade][word] 
    return min_prob

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
informative_words = {}
importance_dictionary = {}

#Initialize dictionary
init_decade = INITIAL_DECADE
while(init_decade <= FINAL_DECADE):
    dictionary[init_decade] = {}
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
    decades_count[movie_decade] += 1
    movie_bag = []
    for word in movie_summary.split():
        for decade in dictionary:
            if word not in dictionary[decade]:
                dictionary[decade][word] = 0
            else:
                if (movie_decade == decade):
                        if word not in movie_bag:
                            dictionary[decade][word] += 1
                            movie_bag.append(word)

for decade in dictionary:
    for word in dictionary[decade]:
        temp = float(dictionary[decade][word])/decades_count[decade]
        if temp == 0:    
            dictionary[decade][word] = 0.00001
        else:
            dictionary[decade][word] = temp

for decade in dictionary:
    for word in dictionary[decade]:
        prob = dictionary[decade][word]
        min_prob = 999999
        for decade2 in dictionary:
            if(dictionary[decade2][word] < min_prob):
                min_prob = dictionary[decade2][word]
                
        importance_dictionary[decade][word] = float(prob)/min_prob
        

for decade in decades_count:
    for i in range(10):
        word = keywithmaxval(importance_dictionary[decade])
        informative_words[decade].append(word)
        del importance_dictionary[decade][word]
        

print informative_words
            
    
                
                

    
        

