""" Provides some utilities to ease the usage of ipyleaflet with osmnx """

import pandas, numpy
import ipyleaflet as lf
import folium as fl
import osmnx as ox
import networkx as nx


def draw_map(G, highlight = None , zoom = 16):
    """ draws ipyleaflet map with location as center of the map """
    
    if len(G) >= 1000:
        print(f"The graph has {len(G)} which is a lot, we will use basic faster folium instead")
        m = ox.plot_graph_folium(G = G)
        return m
        
    center_osmid = ox.stats.extended_stats(G,ecc=True)['center'][0]
    G_gdfs = ox.graph_to_gdfs(G)
    nodes_frame = G_gdfs[0]
    ways_frame = G_gdfs[1]
    center_node = nodes_frame.loc[center_osmid]
    location = (center_node['y'], center_node['x'])
    m = lf.Map(center = location, zoom = zoom)

    for _, row in ways_frame.iterrows():
        lines = lf.Polyline(
            locations = [list(elem)[::-1] for elem in [*row['geometry'].coords]],
            color = "black",
            fill = False,
            weight = 1
        )
        m.add_layer(lines)

    # if we want to mark some specific nodes
    if highlight:
        for node_osmid in highlight:
            node = nodes_frame.loc[node_osmid]
            node_xy = (node['y'], node['x'])
            marker = lf.Marker(location = node_xy, draggable = False)
            m.add_layer(marker)

    return m

def draw_route(G, route, zoom = 16):
    """ draws ipyleaflet map with antpath as route"""
    
    if len(G) >= 1000:
        print(f"The graph has {len(G)} which is a lot, we will use basic faster folium instead")
        m = ox.plot_route_folium(G = G, route = route)
        return m

    center_osmid = ox.stats.extended_stats(G,ecc=True)['center'][0]
    G_gdfs = ox.graph_to_gdfs(G)
    nodes_frame = G_gdfs[0]
    ways_frame = G_gdfs[1]
    center_node = nodes_frame.loc[center_osmid]
    location = (center_node['y'], center_node['x'])
    m = lf.Map(center = location, zoom = zoom)

    start_node = nodes_frame.loc[route[0]]
    end_node = nodes_frame.loc[route[len(route)-1]]

    start_xy = (start_node['y'], start_node['x'])
    end_xy = (end_node['y'], end_node['x'])
    marker = lf.Marker(location = start_xy, draggable = False)
    m.add_layer(marker)
    marker = lf.Marker(location = end_xy, draggable = False)
    m.add_layer(marker)

    for u, v in zip(route[0:], route[1:]):
        try:
            x, y = (ways_frame.query(f'u == {u} and v == {v}').to_dict('list')['geometry'])[0].coords.xy
        except:
            x, y = (ways_frame.query(f'u == {v} and v == {u}').to_dict('list')['geometry'])[0].coords.xy
        points = map(list, [*zip([*y],[*x])])
        ant_path = lf.AntPath(
            locations = [*points], 
            dash_array=[1, 10],
            delay=1000,
            color='red',
            pulse_color='black'
        )
        m.add_layer(ant_path)

    return m
    