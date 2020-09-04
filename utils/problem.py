""" Provides some utilities for specific problems/algorithms like heuristic functions """

"""
Used in A-star algorithm; it takes the source and destination node
and calculate the summation of straight line distance between each node
and to origin and each node to the destination.

The value of the summation is not the actual distance but up to the actual scale as 
we use matplotlib coordinates (x,y)
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