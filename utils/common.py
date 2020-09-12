""" 
common stuff for gluing things together and hiding unnecessary complexity  
"""

import random
from collections import deque

from .omx import Node


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
Return true with probability p.
"""
def probability(p):
    return p > random.uniform(0.0, 1.0)