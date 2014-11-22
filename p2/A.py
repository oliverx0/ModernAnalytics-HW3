import math
from config import *
from code.utils import *

#Load all the movies from the file 
movies = load_all_movies(MOVIES_DATA, False)
total_movies = len(movies)

#Dictionary that contains the decade and the counts of movies per decade
decade_counts = {}

#Load the decades in the dictionary (INITIAL_DECADE and FINAL_DECADE in config.py)
init_decade = INITIAL_DECADE
while(init_decade <= FINAL_DECADE):
    decade_counts[init_decade] = 0
    init_decade += 10

#Update the dictionary with movies count
for m in movies:
    decade = math.trunc(float(m['year'])/10)*10
    decade_counts[decade] += 1

print decade_counts

#Update the dictionary with the probabilities
for d in decade_counts:
    decade_counts[d] = float(decade_counts[d])/float(total_movies)
  
draw_PMF(decade_counts)



