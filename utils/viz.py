""" Provides some utilities to ease the usage of ipyleaflet with osmnx """

from ipyleaflet import Map

def draw_map(location, zoom = 16):
    """ draws ipyleaflet map with location as center of the map """
    m = Map(center = location, zoom = zoom)
    return m