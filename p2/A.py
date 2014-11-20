__author__ = 'aub3'

from config import *
from code.utils import *

import matplotlib.pyplot as plt


def get_passengersX(X, dataset):
    final_data = []
    for data in dataset:
        if(data[2] == float(X)):
            final_data.append(data)
    return final_data


def create_bins(bin_num, dataset, max_vals, min_vals):
    bin_range = []
    bin_range.append((max_vals[0] - min_vals[0])/bin_num) #lon
    bin_range.append((max_vals[1] - min_vals[1])/bin_num) #lat
    for data in dataset:
        if(bin_range[0] != 0.0):
            data[0] = int((data[0]-min_vals[0])/bin_range[0])
        else:
            data[0] = 0
        
        if(bin_range[1] != 0.0):
            data[1] = int((data[1]-min_vals[1])/bin_range[1])
        else:
            data[1] = 0
            
        data[2] = int(data[2])
        
    return dataset

p_count_vals = [1,3]

for i in p_count_vals:
    #Load data from files
    if(i == 3):
        train_data = loadfile(TRAIN_DATA, -1) 
    else:
        train_data = loadfile(TRAIN_DATA, 100000) #More data points cause certain problems
    
    #Indicate values to extract (value to predict goes last)
    values = [12, 13, 7]
    
    #Extract only the necesary values and True to transform to float
    train_data = format_set(values, train_data, True)
    
    #Maintain only those values where passenger count = 3
    train_data = get_passengersX(i, train_data)
    
    #Max and min value of each attribute
    max_vals = []
    min_vals = []
    
    temp_train = np.array(train_data).T
    
    for data in temp_train:
        max_vals.append(np.amax(data))
        min_vals.append(np.amin(data))
        
    train_data_scaled = create_bins(1400, train_data, max_vals, min_vals)
    
    plt.figure(i)
    xs = [train_data_scaled[i][0] for i in range(len(train_data_scaled))] #Longitude
    ys = [train_data_scaled[i][1] for i in range(len(train_data_scaled))] #Latitude
    
    plt.scatter(xs, ys) 
    plt.legend()
    plt.show()
    plt.savefig(FIGURES+"/result_p_{0}.jpg".format(PASSENGER_COUNT), dpi=120)