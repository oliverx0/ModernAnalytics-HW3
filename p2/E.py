import math
from config import *
from code.utils import *

WORD = "radio"

#Load all the movies from the file 
movies = load_balanced_movies(MOVIES_DATA, False)
total_movies = len(movies)

print total_movies
#Dictionary that contains the decade and the counts of movies per decade
decade_counts = {}

#Dictionary that contains the count of words "WORD" in movies per decade P(Y)
word_counts = {}

#P(WORD > 0 )
P_WORD = 0

#Load the decades in the dictionary (INITIAL_DECADE and FINAL_DECADE in config.py)
init_decade = INITIAL_DECADE
while(init_decade <= FINAL_DECADE):
    decade_counts[init_decade] = 0
    word_counts[init_decade] = 0
    init_decade += 10

#Update the dictionary with movies count
for m in movies:
    decade = m['year']
    decade_counts[decade] += 1
    if(findWholeWord(WORD, str(m['summary'])) == True):
        word_counts[decade] += 1
        P_WORD += 1

P_WORD = float(P_WORD)/float(total_movies)

#Update the dictionary with the probabilities
for d in decade_counts:
    decade_counts[d] = float(decade_counts[d])/float(total_movies)
    word_counts[d] = float(word_counts[d])/float(total_movies)
    decade_counts[d] = (word_counts[d]*decade_counts[d])/P_WORD #Bayes theorem

# draw_PMF(decade_counts, "Figure_E")