""" 
common stuff for gluing things together and hiding unnecessary complexity  
"""

import random
from collections import deque

from .omx import *

"""
Generate random simple path between source and destination node
over a osmnx graph.

We can use networkx.all_simple_paths iterator function which would serve the
same purpose, but if you went to the its implementation you will see that they use stack
of all the edges of the graph which would REALLY hurt our performance when you use big graph
over a complete city or something like that.

Our method is very simple randomized graph search, and the randomization is about randomly selecting
the node to expand in each step, and only keeping the frontier in our memory. It is obviously has time
complexity O(n+m) and space complexity O(n).

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
                        continue
                    frontier.append(child)
        nums -= 1


"""
Return true with probability p.
"""
def probability(p):
    return p > random.uniform(0.0, 1.0)