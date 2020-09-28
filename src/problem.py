""" Provides some utilities for specific problems/algorithms like heuristic functions """

import math
import heapq
import random
from collections import deque

import numpy as np


"""
Used in A-star algorithm; it takes the source and destination node
and calculate the summation of straight line distance between each node
and to origin and each node to the destination.

The value of the summation is not the actual distance but up to the actual scale as 
we use matplotlib coordinates (x,y)

return dictionary
"""

def astar_heuristic(G, origin, destination):
    distanceGoal = dict()
    distanceOrigin = dict()

    originX = G.nodes[origin]['x']
    originY = G.nodes[origin]['y']

    destX = G.nodes[destination]['x']
    destY = G.nodes[destination]['y']

    for node in G:
        pointX = G.nodes[node]['x']
        pointY = G.nodes[node]['y']

        originDest = math.sqrt((pointX-originX)**2 + (pointY-originY)**2)
        destDist = math.sqrt((pointX-destX)**2 + (pointY-destY)**2)
        
        distanceGoal[node] = originDest
        distanceOrigin[node] = destDist

    return distanceGoal, distanceOrigin


"""
Calculates the great circle distance between two points  on the earth
(specified in decimal degrees). This is useful when finding distance between 
two points that are far-away. 

return distance
"""

def haversine_distance (lon1, lat1, lon2, lat2):

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


"""
Used in A-star algorithm; it takes the source and destination node
and determines the great-circle distance between two points on a sphere
This is calculated for each node and to origin and each node to the destination.

return dictionary
"""

def astar_heuristic_haversine(G, origin, destination):
    distanceGoal = dict()
    distanceOrigin = dict()

    originX = G.nodes[origin]['x']
    originY = G.nodes[origin]['y']

    destX = G.nodes[destination]['x']
    destY = G.nodes[destination]['y']

    for node in G:
        pointX = G.nodes[node]['x']
        pointY = G.nodes[node]['y']

        originDest = haversine_distance(originX, originY, pointX, pointY)
        destDist = haversine_distance(pointX, pointY, destX, destY)

        distanceGoal[node] = originDest
        distanceOrigin[node] = destDist

    return distanceGoal, distanceOrigin


"""
One possible schedule function for simulated annealing
"""

def exp_schedule(k=20, lam=0.005, limit=100):
    return lambda t: (k * np.exp(-lam * t) if t < limit else 0)