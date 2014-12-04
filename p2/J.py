import math
from config import *
from code.utils import *
import scipy.stats

#Movies name
NAMES = ["Finding Nemo", "The Matrix", "Gone with the Wind", "Harry Potter and the Goblet of Fire", "Avatar"]

#Load all the movies from the file 
movies_training = load_balanced_movies(MOVIES_DATA, False)
movies_test = load_movies_by_name(MOVIES_DATA, NAMES)

total_movies = len(movies_training)

#Dictionary
dictionary = {}
decades_count = {}

#Initialize dictionary
init_decade = INITIAL_DECADE
while(init_decade <= FINAL_DECADE):
    dictionary[init_decade] = {}
    decades_count[init_decade] = 0
    init_decade += 10
    
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

for decade in dictionary:
    for word in dictionary[decade]:
        temp = float(dictionary[decade][word])/decades_count[decade]
        if temp == 0:    
            dictionary[decade][word] = math.log(0.0001)
        else:
            dictionary[decade][word] = math.log(temp)

for decade in decades_count:
    decades_count[decade] = float(decades_count[decade])/total_movies

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
   # print final_prob
    draw_PMF2(final_prob, movie['title'], predicted, movie_decade, "Decade", movie['title'])
    
print "Correct: "+str(correct)
print "Incorrect: "+str(incorrect)

