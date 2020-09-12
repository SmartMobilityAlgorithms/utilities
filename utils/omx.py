""" Provides some utilities to ease the usage of osmnx """

import osmnx
from pandas.core.common import flatten

from .common import *
"""
This is a wrapper around osmnx nodes so we can query a single node
with questions like:
    how did we get here from the origin?
    how far is the node from the origin? For Dijkstra
    what are my children?
"""

class Node:
    # constructor for each node
    def __init__(self ,graph , osmid, distance = 0, parent = None):
        
        # the dictionary of each node as in networkx graph --- still needed for internal usage
        self.node = graph[osmid]
        
        # the distance from the parent node --- edge length
        self.distance = distance
        
        # the parent node
        self.parent = parent
        
        # unique identifier for each node so we don't use the dictionary returned from osmnx
        self.osmid = osmid
        
        # the graph
        self.G = graph
    
    # returning all the nodes adjacent to the node
    def expand(self):
        children = [Node(graph = self.G, osmid = child, distance = self.node[child][0]['length'], parent = self) \
                        for child in self.node]
        return children
    
    # returns the path from that node to the origin as a list and the length of that path
    def path(self):
        node = self
        path = []
        while node:
            path.append(node.osmid)
            node = node.parent
        return path[::-1]
    
    # the following two methods are for dictating how comparison works

    def __eq__(self, other):
        try:
            return self.osmid == other.osmid
        except:
            return self.osmid == other
            
    
    def __hash__(self):
        return hash(self.osmid)



"""
Find the neighbours of a route that has exact source/destination node.

We had to define the meaning of finding neighbours for a route in a graph,
because we needed it in local search algorithms like simulated annealing and
genetic algorithm and tabu search.

Here is how it works; we have a route of length 10 from node A to node Z as follows

    route = [A, B, C, D, E, F, G, H, I, Q, Z]

if we make the node B to fail/contracted so we need to find a new way
to get from A to C

    child = [A, M, N, C, D, E, F, G, H, I, Q, Z]

the new route from A to C is [A, M, N, C] instead of [A, B, C], let's call
that our first child. Our second child when we delete node C from the original
route and see how we can get from B to D instead.

Based on that we have 8 children from a route of 10 nodes; each children is produced
from contracting a node in the route except the source or destination.

It is iterator function so it is lazy evaluated to avoid dealing with routes with big 
number of nodes.
"""

def children_route(G, route):
    
    # now we will iterate over all the nodes except the source and destination
    # node and fail them one node at a time and yield a new route by stitching
    # a route between the node before and after the failing node into our 
    # original route

    for i in range(1, len(route) - 1):
        failing_node = route[i]
        to_be_stitched = shortest_path_with_failed_nodes(G, route[i-1], route[i+1], route[i])
        route[i] = to_be_stitched # route now is a list of lists so we need to flatten it
        route = flatten(route)
        yield route
