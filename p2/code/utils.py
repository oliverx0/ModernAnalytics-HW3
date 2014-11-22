import numpy,math,datetime,logging
from sklearn import linear_model
import math
import time
import numpy as np
import gzip
import re
import matplotlib.pyplot as plt
from config import *


#*******************************************
#Checks is word is in a string
#******************************************
def findWholeWord(word, total):
    return word in total
    
#*******************************************
#Draw a PMF from a dictionary
#********************************************
def draw_PMF(dictionary, filename):
    #Y = list of probabilities, X = list of decades
    x = [d for d in dictionary]
    x.sort()
    y = [dictionary[d] for d in x]
    plt.bar(x,y, width = 10)
    plt.show()
    plt.savefig(FIGURES+filename, dpi=120)

#********************************************
#Function to load movies from the file
#********************************************#
def load_all_movies(filename, debug):
    """
    Load and parse 'plot.list.gz'. Yields each consecutive movie as a dictionary:
        {"title": "The movie's title",
         "year": The decade of the movie, like 1950 or 1980,
         "identifier": Full key of IMDB's text string,
         "summary": "The movie's plot summary"
        }
    You can download `plot.list.gz` from http://www.imdb.com/interfaces
    """
    counter = 0
    movie_list = [] 

    assert "plot.list.gz" in filename # Or whatever you called it
    current_movie = None
    movie_regexp = re.compile("MV: ((.*?) \(([0-9]+).*\)(.*))")
    skipped = 0
    
    for line in gzip.GzipFile(filename, 'r'): #open(filename):
        if counter > DEBUG_MAX_COUNT and debug == True:
            return movie_list

        if line.startswith("MV"):
            if current_movie:
                # Fix up description and send it on
                current_movie['summary'] = "\n".join(current_movie['summary'] )
                # yield current_movie
            current_movie = None
            try:
                identifier, title, year, episode = movie_regexp.match(line).groups()
                if int(year) < 1930 or int(year) > 2014:
                    # Something went wrong here
                    raise ValueError(identifier)
                current_movie = {"title": title,
                                 "year": 10*int(int(year)/10),
                                 'identifier': identifier,
                                 'episode': episode,
                                 "summary": []}
            except:
                skipped += 1
                
                
        if line.startswith("PL: ") and current_movie:
            # Add to the current movie's description
            current_movie['summary'].append(line.replace("PL: ",""))
            movie_list.append(current_movie)
            counter += 1
    print "Skipped",skipped
    return movie_list

