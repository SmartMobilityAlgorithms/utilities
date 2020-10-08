""" Provides some utilities for specific problems/algorithms like heuristic functions """

import math
import heapq
import random
import itertools
from collections import deque
import numpy as np

from .common import *


########################################################################
########################################################################
############################# A STAR ###################################
########################################################################
########################################################################

"""Calculates the straight line distance between two points on earth
(specified in decimal degrees). This is of course an approximation, but 
acceptable one if the two points are close to each other

Parameters
----------
lon1: longitude of the first point
lat1: latitude of the second point
lon2: longitude of the second point
lat2: latitude of the second point

Returns
-------
distance: the straight line distance calculated by pythagoras theorem

"""
def straight_line(lon1, lat1, lon2, lat2):
    return math.sqrt((lon2 - lon1)**2 + (lat2-lat1)**2)



"""Calculates the great circle distance between two points  on the earth
(specified in decimal degrees). This is useful when finding distance between 
two points that are far-away. 

Parameters
----------
lon1: longitude of the first point
lat1: latitude of the second point
lon2: longitude of the second point
lat2: latitude of the second point

Returns
-------
distance: the distance of the great circle arc between two points
          calculated by harversine method
"""

def haversine_distance(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

"""Used in A-star algorithm; it takes the source and destination node
and calculate the summation of straight line distance between each node
to origin and each node to the destination.

The value of the summation is not the actual distance but up to the some actual scale as 
we use matplotlib coordinates (x,y)

Parameters
----------
G: NetworkX graph returned from osmnx methods
origin: The id of the origin node in the graph 
destination: The id of the destination node in the graph
measuring_dist: The method used in measuring distance between nodes; staright line distance,
                harversine distance

Returns
-------
distanceGoal, distanceOrigin: dictionaries that associate the proper distance with node id

"""

def astar_heuristic(G, origin, destination, measuring_dist = straight_line):
    distanceGoal = dict()
    distanceOrigin = dict()

    originX = G.nodes[origin]['x']
    originY = G.nodes[origin]['y']

    destX = G.nodes[destination]['x']
    destY = G.nodes[destination]['y']

    for node in G:
        pointX = G.nodes[node]['x']
        pointY = G.nodes[node]['y']

        originDist = measuring_dist(originX, originY, pointX, pointY)
        destDist = measuring_dist(pointX, pointY, destX, destY)

        distanceGoal[node] = originDist
        distanceOrigin[node] = destDist

    return distanceGoal, distanceOrigin



##########################################################################################################
##########################################################################################################


########################################################################
########################################################################
############################# Simulated Annealing ######################
########################################################################
########################################################################



"""Schedule exponential function for cooling in simulated annealing

Parameters
----------
k: starting temperature of the function
lam: the rate of temperature decreasing
limit: number of iterations after which the function produces zero value

Returns
-------
function: it is lambda function that take the current number of iteration
"""

def exp_schedule(k=20, lam=0.005, limit=100):
    function = lambda t: (k * np.exp(-lam * t) if t < limit else 0)
    return function



##########################################################################################################
##########################################################################################################

########################################################################
########################################################################
############################# Genetic Algorithm ########################
########################################################################
########################################################################

"""Mutation policy for routes. It fails a random node in the route and
stitch the resulting gap and that is it. Sometimes this process fail, so
we iterate until it succeed.

Parameters
----------
G: NetworkX graph returned from osmnx methods
route: The route to be mutated

Returns
-------
path: mutated version from the route
"""
def mutate(G, route):
    source = route[0]
    destination = route[len(route) - 1]
    failed = random.choice(route)

    path = shortest_path_with_failed_nodes(G, route, source, destination, [failed])

    # This method could fail because of a lot of factors relating to the graph structure
    # Check the documentation fo the shortest_path_with_failed_nodes to lear more
    while path == math.inf:
        failed = random.choice(route)
        path = shortest_path_with_failed_nodes(G, route, source, destination, [failed])
    
    return path

"""Crossover between two routes. This is more or less 1-point crossover, but choosing the crossover
node isn't random because sometimes it is not possible to crossover two routes. We choose the crossover
node by searching both routes to find a node that is common between them and split at that node. This route
may not be there, in that case we just return the first route without doing anything.

Parameters
----------
route_1: The first route
route_2: The second route

Returns
-------
The result of doing crossover between route_1 and route_2
"""

def cross_over(route_1, route_2):
    intersection = [*itertools.filterfalse(lambda element : element in [origin.osmid, destination.osmid] , list(set(route_1) & set(route_2)))]
    if len(intersection) == 0: return route_1 # if there is not common node, just return the first route

    cross_over_point = random.choice(intersection)
    first_point = route_1.index(cross_over_point)
    second_point = route_2.index(cross_over_point)

    if probability(0.5):
        return route_1[:first_point] + route_2[second_point:]
    else:
        return route_2[:second_point] + route_1[first_point:]
    