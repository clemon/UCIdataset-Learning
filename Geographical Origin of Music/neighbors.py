import numpy as np
import random
import math
import pdb
import sys

# have collection of all train data in format
# given new point to classify:
    # find closest k dataPoints (use euclidian distance formula)
    # average the closest k dataPoints' latlng coordinates
    # $$$profit$$$

k = 10           # k value (number of neighbors to find)
numf = 116      # number of features in each dataPoint in the corpus

# gather the data from the corpus
musicData = []
with open('default_plus_chromatic_features_1059_tracks.txt') as file:
    for line in file:
        musicData.append(eval(line))
# shuffle the data
random.shuffle(musicData)

# split into train and test sets
trainSet = musicData[:700]
testSet = musicData[700:]

results = []
#pdb.set_trace()
for testPoint in testSet:
    knear = [(-69,-69,sys.float_info.max)]*k    # [(lat1,lng1,dist1), ... , (latk,lngk,distk)]

    for trainPoint in trainSet:
        
        distSum = 0.0
        for feature in range(numf):
            distSum += (testPoint[feature] - trainPoint[feature])**2

        knear.sort(key=lambda x: x[2], reverse=False)
        if distSum < knear[k-1][2]:
            knear[k-1] = (trainPoint[numf], trainPoint[numf+1], distSum)
        knear.sort(key=lambda x: x[2], reverse=False)

    #pdb.set_trace()
    # calc avg lat and lng
    latsum = 0.0
    lngsum = 0.0
    for point in knear:
        latsum += point[0]
        lngsum += point[1]        

    results.append((latsum/k, lngsum/k))
#pdb.set_trace()

# calculate the mean squared error
distSum = 0.0
for i, result in enumerate(results):
    # calc dist between prediction and actual coordinates
    # take MSE on the difference    
    distSum += math.sqrt((result[0]-testSet[i][numf])**2+(result[1]-testSet[i][numf+1])**2)

print "average distance error: {}".format(distSum/len(results))





