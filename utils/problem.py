""" Provides some utilities for specific problems/algorithms like heuristic functions """

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
A Queue in which the minimum (or maximum) element (as determined by f and order) is returned first.
If order is 'min', the item with minimum f(x) isreturned first; if order is 'max', then it is the item with maximum f(x).
Also supports dict-like lookup.
"""

class PriorityQueue:
    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')