""" Provides some utilities for specific problems/algorithms like heuristic functions """

import math
import heapq

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

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)