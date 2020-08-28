""" Provides some utilities to ease the usage of ipyleaflet with osmnx """

import ipyleaflet as lf
import osmnx as ox


def draw_map(G, zoom = 16):
    """ draws ipyleaflet map with location as center of the map """
    center_osmid = ox.stats.extended_stats(G,ecc=True)['center'][0]
    G_gdfs = ox.graph_to_gdfs(G)
    nodes_frame = G_gdfs[0]
    ways_frame = G_gdfs[1]
    center_node = nodes_frame.loc[node_center]
    location = (center_node['y'], center_node['x'])
    m = lf.Map(center = location, zoom = zoom)
    for _, row in ways_frame.iterrows():
        lines = Polyline(
        locations = [list(elem)[::-1] for elem in [*row['geometry'].coords]],
        color = "black",
        fill = False,
        weight = 1
    )
    m.add_layer(lines)
    return m