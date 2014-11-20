import numpy,math,datetime,logging
from sklearn import linear_model
from distance import get_distance
import math
import time
import numpy as np



# logging.basicConfig(filename='logs/utils.log',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#*****************************************************
#Class used to hold values of distances and corresponding
#values of neighbors.
#*****************************************************
class K_DISTANCE:
     def __init__(self, distance, k):
        self.distance = distance  
        self.k = k
        
#*****************************************************
#Scales a value based on max and min
#*****************************************************      
def scale_val(val, max_val, min_val):
    return (val-min_val)/(max_val-min_val)

#*****************************************************
#Scales a dataset based on the max and min values of
#each attribute
#*****************************************************
def scale_set(dataset, max_vals, min_vals):
    for data in dataset:
        length = len(data)
        for i in range(length):
            if (i < length-1):
                data[i] = scale_val(data[i], max_vals[i], min_vals[i])
    return dataset
    
#*****************************************************
#Calculates the euclidean distance between 2 arrays of
#same length
#*****************************************************
def euclidean_distance(a, b, omit_last):
    total = 0
    length = len(a)
    if(omit_last):
        length = length -1
    for i in range(length):
        temp = a[i] - b[i]
        temp = temp*temp
        total += temp
    return math.sqrt(total)
    
#*****************************************************
#Calculates the RMSE of y_produced and y_expected
#values
#*****************************************************
def RMSE(y_produced,y_expected):
    final_error = 0
    for i in range(len(y_produced)):
        error = y_produced[i] - y_expected[i]
        error = error*error
        final_error += error
    return math.sqrt(final_error/len(y_produced))

#*****************************************************
#Calculates the MAR of y_produced and y_expected
#values
#*****************************************************  
def MAE(y_produced,y_expected):
    final_error = 0
    for i in range(len(y_produced)):
        error = y_produced[i] - y_expected[i]
        error = math.fabs(error)
        final_error += error
    return final_error/len(y_produced)

#*****************************************************
#Prints the necesary metrics
#*****************************************************  
def print_metrics(y_produced, y_expected):
    print "Root Mean Square Error: ", RMSE(y_produced, y_expected)
    print "Pearson Correlation Coefficient: ", np.corrcoef(y_produced, y_expected)[0][1]
    print "Mean Absolute Error: ", MAE(y_produced, y_expected)
    return None

#***************************
#Calculate median of a list
#***************************
def median(lst):
    return numpy.median(numpy.array(lst))

#*****************************************************
#Calculates the nk neares neighbots a the test variable
#in the train data
#*****************************************************   
def nearest_neighbors(nk, test, train):
   
    temp_list = []
    for data in train:
        temp_distance = euclidean_distance(test, data, True)
        k = K_DISTANCE(temp_distance, data[len(data)-1]) 
        if(len(temp_list) < nk):
         temp_list.append(k)
         temp_list.sort(key=lambda x: x.distance)
            
        elif(temp_distance < temp_list[len(temp_list)-1].distance):
            temp_list[len(temp_list)-1] = k
            temp_list.sort()
    
    median_list = []
    for element in temp_list:
        median_list.append(element.k)       
    return median(median_list)

#*****************************************************
#Returns a set only with the values that will be used
#*****************************************************   
def format_set(values, dataset, float_them):
    final_set = []
    for data in dataset:
        if(float_them == False):
            final_set.append([data[i] for i in values])
        else:
            final_set.append([float(data[i]) for i in values])
    return final_set
    
#*****************************************************
#Returns a set only with the values that will be used
#formatting the pickuptime as well
#*****************************************************      
def special_format_set(values, dataset):
    final_set = []
    
    for data in dataset:
        temp = []
        for i in values:
            if(i != 5):
                temp.append(float(data[i]))
            else:
                trip_time = time.strptime(data[i], "%Y-%m-%d %H:%M:%S")
                trip_time = trip_time.tm_hour
                temp.append(trip_time)
        final_set.append(temp)
    return final_set


#*****************************************************
#Loads the contents of a cvs file into al list
#***************************************************** 
def loadfile(file_name, limit):
    flag = True         #Flag to ignore the first line of the file
    train_data = []   #List containing onyly the important attributes of the example_data from taxis:
                                # [0] pickup_datetime 
                                # [1] dropoff_datetime
                                # [2] trip_time
                                # [3] pickup_longitude
                                # [4] pickup_latitude
                                # [5] dropoff_longitude
                                # [6] dropoff_latitude
                                # [7] trip distance (taximeter in miles)
                                # [8] coordinate_distance
        
    distances = []      #Array containing only the coordinates distance
    error_count  = 0
        
    #Go through each line in the TRAINING_DATA CSV
    counter = 0
    for line in file(file_name):
            counter+= 1
            if((limit != -1) and counter > limit):
                    break
            if flag == False:
                line = line.strip().split(',')      #Transform the line into a list
                plong,plat,dlong,dlat=line[-4:]     #Recover the laitutde and longitude variables
                try:
                    plong = float(plong)                
                    plat = float(plat)
                    dlong = float(dlong)
                    dlat = float(dlat)
                except:
                    None
                try:
                    dist = get_distance(plat,plong,dlat,dlong)
                    if(dist != 0.0 and math.fabs(dlat) > 1.0 and math.fabs(dlong) > 1.0):
                        distances.append(dist)
                        #Add the calculated distance to the line array in the last position
                        line.append(dist)

                        train_data.append([line[i] for i in range(len(line))])
                except:
                    error_count += 1
    
            flag = False
    
    return train_data