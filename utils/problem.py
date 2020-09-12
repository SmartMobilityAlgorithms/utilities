""" Provides some utilities for specific problems/algorithms like heuristic functions """

import math
import heapq
import random
from collections import deque

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
Generate random simple path between source and destination node
over a osmnx graph.

We can use networkx.all_simple_paths iterator function which would serve the
same purpose,but if you went to the its implementation you will see that they use stack
of all the edges of the graph which would really hurt our performance when you use big graph
over a complete city or something.

Our method is randomized graph search, and the randomization is about randomly selecting
the node to expand in each step, and only keeping the frontier in our memory.

It is an iterator function so we don't overload our memory if you wanted a lot of paths.
"""

def randomized_search(G, source, destination, nums_of_paths = 1):
    origin = Node(graph = G, osmid = source)
    destination = Node(graph = G, osmid = destination)
    nums = nums_of_paths
    
    while nums > 0:
        route = [] # the route to be yielded
        frontier = deque([origin])
        explored = set()
        found = False
        while frontier and not found:
            node = random.choice(frontier)   # here is the randomization part
            frontier.remove(node)
            explored.add(node)

            for child in node.expand():
                if child not in explored and child not in frontier:
                    if child == destination:
                        route = child.path()
                        yield route
                        found = True
                    frontier.append(child)
        nums -= 1
