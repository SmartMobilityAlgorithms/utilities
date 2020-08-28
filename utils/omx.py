""" Provides some utilities to ease the usage of osmnx """

import osmnx

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
        
        # the distance from the origin to that node --- sum of edges length
        self.from_origin = self.distance_from_origin()

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
        length = 0
        path = []
        while node:
            length += node.distance
            path.append(node.osmid)
            node = node.parent
        return path[::-1], length
    
    # return the summation of edges length from the origin --- used in dijkstra
    def distance_from_origin(self):
        meters = 0
        node = self
        while node:
            meters += node.distance
            node = node.parent
        return meters
    
    # the following two methods are for supporting
    # list usage and some optimization to get over
    # the networkx dictionary hurdle

    def __eq__(self, other):
        try:
            return self.osmid == other.osmid
        except:
            return self.osmid == other
            
    
    def __hash__(self):
        return hash(self.osmid)