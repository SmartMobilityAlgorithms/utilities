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
Given an iterable with nodes ids and the networkx graph
The function calculated the weight of the route
"""

def cost(G, route):
    weight = 0
    for u, v in zip(route, route[1:]):
        try: 
            weight += G[u][v][0]['length']
        except:
            # this is for handling bi-directional search
            # because some streets are one-way otherwise
            # it won't affect anything else
            weight += G[v][u][0]['length'] 
    return weight


"""
Given an itertable with nodes id and the networkx graph
The function will calculate the weight of the route as
if it is as tour, so after arriving at the last node
we will add the weight of the edge connecting the last node
with the first one

the expected route here is tuple

It was made to deal with simple graphs
"""
def cost_tour(G, route):
    weight = 0
    route = list(route)
    for u, v in zip(route, route[1:]+[route[0]]):
        weight += G[u][v]['weight']
    return weight
