# -*- coding: utf-8 -*-
import math
import re
from config import *
from code.utils import *

K = {1: 47.79259259259259, 2: 64.64814814814814, 3: 75.3851851851852, 4: 82.49629629629631, 5: 88.83333333333333, 6: 93.57777777777778, 7: 96.4925925925926, 8: 98.77037037037037, 9:100}

def draw_CMC(data,filename,xlabel,ylabel):
    print('length of data : ',len(data))
    x,y = [],[]
    for i in data:
        x.append((i))
        y.append((data[i]))
    plt.plot(x, y,color='b')
    plt.xlabel(xlabel)
    plt.title("CMC Curve for Naive Bayes Classifier")
    plt.ylabel(ylabel)
    plt.savefig(FIGURES+filename)
    
draw_CMC(K, "CMC_Curve", "K value", "Accuracy")