__author__ = 'aub3'

from config import *
from code.utils import *
 
#Load data from files
train_data = loadfile(TRAIN_DATA, -1) #should be -1
test_data = loadfile(TRIP_DATA_1, 100000) #should be 100000

#Indicate values to extract (value to predict goes last)
values = [5, 9, 10, 11, 12, 13, 8]

#Extract only the necesary values and True to transform to float
train_data = special_format_set(values, train_data)
test_data = special_format_set(values, test_data)

#Lists that hold only the values needed to calculate metrics
k_results = []
real_values = []

#For every data in the test data, we calculate the nearest neighbor's label and save it
#we also save the real value to then compare
result_location = len(test_data[0])-1
for data in test_data:
   k_results.append(float(nearest_neighbors(1, data, train_data)))
   real_values.append(data[result_location])

#Prints metrics of RMSE, Correlation Coefficient, and MAE    
print_metrics(k_results, real_values)