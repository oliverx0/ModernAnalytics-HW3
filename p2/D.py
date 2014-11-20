__author__ = 'aub3'

from config import *
from code.utils import *


#Load data from files
train_data = loadfile(TRAIN_DATA, 1000) #should be -1
test_data = loadfile(TRIP_DATA_1, 4000) #should be 10000

#Indicate values to extract (value to predict goes last)
values = [5, 9, 10, 11, 12, 13, 8]

#Extract only the necesary values and True to transform to float
train_data = special_format_set(values, train_data)
test_data = special_format_set(values, test_data)

#Max and min value of each attribute
max_vals = []
min_vals = []

temp_train = np.array(train_data).T
temp_test = np.array(test_data).T

for data in temp_train:
    max_vals.append(np.amax(data))
    min_vals.append(np.amin(data))
    
train_data_scaled = scale_set(train_data, max_vals, min_vals)    
test_data_scaled =  scale_set(test_data, max_vals, min_vals) 

#Lists that hold only the values needed to calculate metrics
k_results = []
real_values = []

#For every data in the test data, we calculate the nearest neighbor's label and save it
#we also save the real value to then compare
result_location = len(test_data[0])-1
for data in test_data_scaled:
   k_results.append(float(nearest_neighbors(1, data, train_data_scaled)))
   real_values.append(data[result_location])

#Prints metrics of RMSE, Correlation Coefficient, and MAE    
print_metrics(k_results, real_values)