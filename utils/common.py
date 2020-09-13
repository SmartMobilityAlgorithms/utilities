"""
common stuff for gluing things together and hiding unnecessary complexity 
""" 

import osmnx
import random
from collections import deque
from pandas.core.common import flatten


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

"""
Find the route between `source` and `destination` nodes when the list of nodes
specified in `failed` acts if they are not in the graph.
"""

def shortest_path_with_failed_nodes(G, source, target, failed : list):
    origin = Node(graph = G, osmid = source)
    destination = Node(graph = G, osmid = target)

    # you can't introduce failure in the source and target
    # node, because your problem will lose its meaning
    if origin.osmid in failed or destination.osmid in failed:
        raise Exception("source/destination node can't failed")

    # we need to flag every node whether it is failed or not
    failure_nodes = {node: False for node in G.nodes()}
    failure_nodes.update({node: True for node in failed})

    # the normal implementation of dijkstra
    shortest_dist = {node: math.inf for node in G.nodes()}
    unrelaxed_nodes = [Node(graph = G, osmid = node) for node in G.nodes()]
    seen = set()

    shortest_dist[source] = 0

    while len(unrelaxed_nodes) > 0:
        node = min(unrelaxed_nodes, key = lambda node : shortest_dist[node])

        if node == destination:
            return node.path()

        unrelaxed_nodes.remove(node); seen.add(node.osmid) # relaxing the node

        for child in node.expand():
            # if it is failed node, skip it
            if failure_nodes[child.osmid] or\
                child.osmid in seen: continue

            child_obj = next((node for node in unrelaxed_nodes if node.osmid == child.osmid), None)
            child_obj.distance = child.distance

            distance = shortest_dist[node.osmid] + child.distance
            if distance < shortest_dist[child_obj.osmid]:
                shortest_dist[child_obj.osmid] = distance
                child_obj.parent = node

    # in case the node can't be reached from the origin
    return math.inf

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
