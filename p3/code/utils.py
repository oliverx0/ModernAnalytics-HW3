import numpy,math,datetime,logging
from sklearn import linear_model
import math
import time
import numpy as np
import gzip
import re
import matplotlib.pyplot as plt
import random
from config import *


#*******************************************
#Returns the key in a dictionary with the 
#maximum value
#******************************************
def keywithmaxval(d):
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

def replacement(match):
    return match.group(1).lower();

#*******************************************
#Cleans a summary
#******************************************    
def clean_str(string):
    string = re.sub(r"('s)", "", string)                #father's becomes father
    string = re.sub(r'([A-Z])', replacement, string)    #Oliver becomes oliver
    string = re.sub(r'([-_])', " ", string)             #friend-zone becomes friend zone
    string = re.sub(r'([^a-zA-Z ])', " ", string)       #yes!! becomes yes
    string = re.sub(r'([\s]+)', " ", string)            #let    me   go becomes let me go
    return string

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
    plt.figure()
    x = [d for d in dictionary]
    x.sort()
    y = [dictionary[d] for d in x]
    plt.bar(x,y, width = 10)
    # plt.show()
    plt.savefig(FIGURES+filename)
    
#*******************************************
#Draw a PMF from a dictionary
#********************************************
def draw_PMF2(dictionary, filename, predicted, real, X, Y):
    #Y = list of probabilities, X = list of decades
    plt.figure()
    x = [d for d in dictionary]
    x.sort()
    y = [dictionary[d] for d in x]
    colors = []
    for d in x:
        if d == real:
            colors.append('r')
        elif d == predicted:
            colors.append('g')
        else:
            colors.append('b')
    plt.bar(x,y, width = 10, color=colors)
    plt.xlabel(X, fontsize=18)
    plt.ylabel(Y, fontsize=16)
    # plt.show()
    plt.savefig(FIGURES+filename)
    
#*******************************************
#Draw a CMC Curve
#********************************************
def draw_CMC(dictionary,filename,xlabel,ylabel):
    
    plt.figure()
    x = [d for d in dictionary]
    x.sort()
    y = [dictionary[d] for d in x]
    plt.plot(x, y,color='b')
    plt.xlabel(xlabel)
    plt.title("CMC Curve for Naive Bayes Classifier")
    plt.ylabel(ylabel)
    plt.savefig(FIGURES+filename)
    
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
                movie_list.append(current_movie)
                counter +=1 
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

    print "Skipped",skipped
    return movie_list

#********************************************
#Function to load balanced movie set
#********************************************#
def load_balanced_movies(filename, debug):
    
    print "ENTRA LOAD"
    """
    Load and parse 'plot.list.gz' for 6000 first movies in each decade. Yields each consecutive movie as a dictionary in a list:
        {"title": "The movie's title",
         "year": The decade of the movie, like 1950 or 1980,
         "identifier": Full key of IMDB's text string,
         "summary": "The movie's plot summary"
        }
    You can download `plot.list.gz` from http://www.imdb.com/interfaces

    Returns list of dictionaries of all movies, is 54,000 samples long
    """
    movie_list = [] 
    movie_list_balanced = []
    decade_sample = {}
    decade_count = {}
    decade_counter = 0
    counter = 0

    init_decade = INITIAL_DECADE
    while(init_decade <= FINAL_DECADE):
        decade_sample[init_decade] = []
        decade_count[init_decade] = 0
        init_decade += 10    
        decade_counter += 1

    assert "plot.list.gz" in filename # Or whatever you called it
    current_movie = None
    movie_regexp = re.compile("MV: ((.*?) \(([0-9]+).*\)(.*))")
    skipped = 0

    for line in gzip.GzipFile(filename, 'r'): #open(filename):
        #if counter > DEBUG_MAX_COUNT and debug == True:
        #    return movie_list_balanced
        if counter >= decade_counter:
            break
        if line.startswith("MV"):
            if current_movie:
                # Fix up description and send it on
                decade = current_movie['year']
                current_movie['summary'] = "\n".join(current_movie['summary']) 
                if((debug == False and (decade_count[decade] < BALANCED_COUNT)) or (debug == True and (decade_count[decade] < DEBUG_MAX_COUNT))):
                    decade_sample[decade].append(current_movie)
                    decade_count[decade] += 1
                    if((debug == False and decade_count[decade] == BALANCED_COUNT) or (debug == True and decade_count[decade] == DEBUG_MAX_COUNT)):
                        counter += 1
                        movie_list_balanced += decade_sample[decade]

                #movie_list.append(current_movie)    
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
    
    
    print "Skipped",skipped    
    print "DECADE COUNT: ", decade_count
    return movie_list_balanced

    #for m in movie_list:
    #    decade = m['year']
    #    decade_sample[decade].append(m)

    #for d in decade_sample:
    #    #decade_sample[d] = decade_sample[d][0:6000]
    #    movie_list_balanced += decade_sample[d]

#********************************************
#Function to load all movies in tthe name_list
#********************************************#
def load_movies_by_name(filename, names_list):
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
    max_count = len(names_list)

    assert "plot.list.gz" in filename # Or whatever you called it
    current_movie = None
    movie_regexp = re.compile("MV: ((.*?) \(([0-9]+).*\)(.*))")
    skipped = 0
    
    for line in gzip.GzipFile(filename, 'r'): #open(filename):
        if counter >= max_count:
            return movie_list

        if line.startswith("MV"):
            if current_movie:
                # Fix up description and send it on
                current_movie['summary'] = "\n".join(current_movie['summary'] )
                for name in names_list:
                    if(name == current_movie['title']):
                        movie_list.append(current_movie)
                        names_list.remove(name)
                        counter +=1 
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

    print "Skipped",skipped
    print "Not found: ", names_list
    return movie_list
    

    

