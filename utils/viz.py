""" Provides some utilities to ease the usage of ipyleaflet with osmnx """

import pandas, numpy
import ipyleaflet as lf
import folium as fl
import osmnx as ox


try:
    import google.colab
    IN_COLAB = True
except:
    IN_COLAB = False


draw_map = None
draw_route = None



def draw_map_folium(G, highlight = None, zoom = 16):
    center_osmid = ox.stats.extended_stats(G,ecc=True)['center'][0]
    G_gdfs = ox.graph_to_gdfs(G)
    nodes_frame = G_gdfs[0]
    ways_frame = G_gdfs[1]
    center_node = nodes_frame.loc[center_osmid]
    loc = [center_node['y'], center_node['x']]
    m = fl.Map(location = loc, zoom_start = zoom)

    for _, row in ways_frame.iterrows():
        line = [elem[::-1] for elem in [*row['geometry'].coords]]
        lines = [[u, v] for u, v in zip(line[0:], line[1:])]
        polyline = fl.PolyLine(locations = lines, color = 'black', weight=2)
        m.add_child(polyline)

    if highlight:
        kw = dict(fill_color='red', radius=5)
        for node_osmid in highlight:
            node = nodes_frame.loc[node_osmid]
            node_xy = [node['y'], node['x']]
            marker = fl.CircleMarker(node_xy, **kw)
            m.add_child(marker)
    return m



def draw_map_leaflet(G, highlight = None , zoom = 16):
    """ draws ipyleaflet map with location as center of the map """
    center_osmid = ox.stats.extended_stats(G,ecc=True)['center'][0]
    G_gdfs = ox.graph_to_gdfs(G)
    nodes_frame = G_gdfs[0]
    ways_frame = G_gdfs[1]
    center_node = nodes_frame.loc[center_osmid]
    location = (center_node['y'], center_node['x'])
    m = lf.Map(center = location, zoom = red)

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

def draw_route_leaflet(G, route, zoom = 16):
    center_osmid = ox.stats.extended_stats(G,ecc=True)['center'][0]
    G_gdfs = ox.graph_to_gdfs(G)
    nodes_frame = G_gdfs[0]
    ways_frame = G_gdfs[1]
    center_node = nodes_frame.loc[center_osmid]
    location = (center_node['y'], center_node['x'])
    m = lf.Map(center = location, zoom = 16)

    start_node = nodes_frame.loc[route[0]]
    end_node = nodes_frame.loc[route[len(route)-1]]

    start_xy = (start_node['y'], start_node['x'])
    end_xy = (end_node['y'], end_node['x'])
    marker = lf.Marker(location = start_xy, draggable = False)
    m.add_layer(marker)
    marker = lf.Marker(location = end_xy, draggable = False)
    m.add_layer(marker)

    for u, v in zip(route[0:], route[1:]):
        x, y = (ways_frame.query(f'u == {u} and v == {v}').to_dict('list')['geometry'])[0].coords.xy
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
    


