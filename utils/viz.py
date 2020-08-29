""" Provides some utilities to ease the usage of ipyleaflet with osmnx """

import pandas, numpy
import ipyleaflet as lf
import osmnx as ox


def draw_map(G, highlight = None , zoom = 16):
    """ draws ipyleaflet map with location as center of the map """
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

    if highlight:
        for node_osmid in highlight:
            node = nodes_frame.loc[node_osmid]
            node_xy = (node['y'], node['x'])
            marker = lf.Marker(location = node_xy, draggable = False)
            m.add_layer(marker)

    return m