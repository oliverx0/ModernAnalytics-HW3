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

K_ACC = {}
for k in range(1,len(decades_count)+1):
    
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
        
        predicted = []
        aux = 1
        for dec in decades_count:         
            if aux <= k:
                pred = keywithmaxval(final_prob)
                predicted.append(pred)
                del final_prob[pred]
                aux += 1
            else:
                break
        
        if movie_decade in predicted:
            correct += 1
        else:
            incorrect += 1
            
    ACC = 100*(float(correct)/total_movies)
    K_ACC[k] = ACC

draw_CMC(K_ACC, "CMC_Curve", "K value", "Accuracy")
            
            
    
                
                

    
        

