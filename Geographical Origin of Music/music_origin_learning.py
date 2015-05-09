import numpy as np
import matplotlib.pyplot as plt
import math
import pdb
import random

k = 6
numf = 116

musicData = []
with open('default_plus_chromatic_features_1059_tracks.txt') as file:
    for line in file:
        musicData.append(eval(line))

random.shuffle(musicData)

# each track has [numf features, lat, lng]
trainData = musicData[:700]
testData = musicData[700:]

# get mean of each feature
featureStats = []   # (mean, IQR, q75, q25)
for feature in range(numf):
    currFeature = []
    meanSum = 0.0
    for point in trainData:
        currFeature.append(point[feature])
        meanSum += point[feature]
        
    q75, q25 = np.percentile(currFeature, [75 ,25])
    iqr = q75 - q25
    featureStats.append((meanSum/len(trainData), iqr, q75, q25))

# initialize centroids (one per continent) to random values (q25 - q75)
newCentroids = [[] for _ in range(k)]
centroids = [[0]*(numf+2)]*k
for centroid in range(k):
    for feature in range(numf): 
        newCentroids[centroid].append(random.uniform(featureStats[feature][3],\
                                                  featureStats[feature][2]))
    
newCentroids[0].extend([55.071348, -105.253907])    #Burgers and obesity
newCentroids[1].extend([-8.924247, -55.722657])    #tacos
newCentroids[2].extend([54.702192, 15.320313])     #cold
newCentroids[3].extend([-8.413157, 34.387194])     #giraffes
newCentroids[4].extend([34.598423, 100.703125])    #noodles
newCentroids[5].extend([-24.571523, 133.687319])    #'Roos and Foster

# lets try to trim the data a little bit so its more uniform across the world
clusters = [[] for _ in range(k)]
for dataPoint in trainData:
    distances = [0.0]*k      # list of distances to centroids len=6 
    for i in range (k):
        # calc euclidian distance 
        distances[i] += math.sqrt((newCentroids[i][numf] - dataPoint[numf])**2 + (newCentroids[i][numf+1] - dataPoint[numf+1])**2)
            
    closest = distances.index(min(distances))      # grab the closest centroid from the list
    clusters[closest].append(dataPoint)            # put the dataPoint in the appropriate cluster
    
print "num NA: {}".format(len(clusters[0])) 
print "num SA: {}".format(len(clusters[1])) 
print "num EU: {}".format(len(clusters[2])) 
print "num AF: {}".format(len(clusters[3])) 
print "num AS: {}".format(len(clusters[4])) 
print "num AU: {}".format(len(clusters[5])) 

# so now we have somewhat constant results for matching the continental centroids based on latlng alone.
# rather than initializing the centroid features (0-67) with avg values over all train data, I should 
# take the avg values over all data in the 'continental cluster'
for i, cluster in enumerate(clusters):
    for feature in range(numf):
        currFeature = []
        meanSum = 0.0
        for dataPoint in cluster:
            currFeature.append(dataPoint[feature])
            meanSum += dataPoint[feature]
        
        newCentroids[i][feature] = meanSum / len(cluster)

while centroids[0] != newCentroids[0]:
    centroids = newCentroids
    newCentroids = [[0]*(numf+2)]*k
    
    clusters = [[] for _ in range(k)]
    
    # foreach datapoint
        # foreach feature
            # foreach centroid

    for dataPoint in trainData:
        distances = [0.0]*k      # list of distances to centroids len=6 
        for feature in range(numf):
            for i in range (k):
                # calc euclidian distance 
                distances[i] += (dataPoint[feature] - centroids[i][feature])**2
                
        closest = distances.index(min(distances))      # grab the closest centroid from the list
        clusters[closest].append(dataPoint)            # put the dataPoint in the appropriate cluster

    # foreach cluster
        # foreach point
    
    # calculate new means for centroids given new dataPoints
    newMeans = np.array([[0.0]*(numf+2)]*k)   # 6xnumf+2 matrix
    for i, cluster in enumerate(clusters):
        for point in cluster:
            newMeans[i] += point
        if len(cluster) > 0:
            newMeans[i] /= len(cluster)
            
    # populate newCentroids with the means
    for i in range(k):
        newCentroids[i] = newMeans[i].tolist()
        
## plot the data
#lat = []
#lng = []
#color = []
#for i, cluster in enumerate(clusters):
#    for dataPoint in cluster:
#        lat.append(dataPoint[numf])
#        lng.append(dataPoint[numf+1])
#        color.append(i)
#
#pdb.set_trace()
#plt.scatter(lat, lng, c=color, alpha=.5, s=100)
#plt.show()

for i, cluster in enumerate(clusters):
    for dataPoint in cluster:
        if i==1:
            print "{}, {}".format(dataPoint[numf], dataPoint[numf+1])

        
# print coordinates
print "-----centroids-----"
for centroid in newCentroids:
    print "{}, {}".format(centroid[numf], centroid[numf+1])
    
clusters = [[] for _ in range(k)]
# test the classifier on the testData
for dataPoint in testData:
    # calc which centroid is closest
    distances = [0.0]*k
    for feature in range(numf):
        for i in range(k):
            distances[i] += math.sqrt((dataPoint[feature] - newCentroids[i][feature])**2)
    closest = distances.index(min(distances))
    clusters[closest].append(dataPoint)
        
# measure the distance from actual coordinates
totalErrorDistance = 0.0
for i, cluster in enumerate(clusters):
    for dataPoint in cluster:
        #print "guess: {},{} actual: {},{}".format(newCentroids[i][numf], newCentroids[i][numf+1], dataPoint[numf], dataPoint[numf+1])
        totalErrorDistance += math.sqrt((newCentroids[i][numf] - dataPoint[numf])**2 + (newCentroids[i][numf+1] - dataPoint[numf+1])**2)
# calculate avg error
print "avg error dist: {}".format(totalErrorDistance/len(testData))


     