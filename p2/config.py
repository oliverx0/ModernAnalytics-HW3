__author__ = 'aub3'
"""
All constants should go here.
"""

import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

INITIAL_DECADE = 1930
FINAL_DECADE = 2010

MOVIES_DATA = os.path.join(__location__, 'data/plot.list.gz') # small data files (ideally < 5 MB) should be stored in data folder
FIGURES = os.path.join(__location__, 'figures/') # figure folder

DEBUG_MAX_COUNT = 100


