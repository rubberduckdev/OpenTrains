import os
import gtfs.models
import analysis.models
import numpy as np
from scipy import spatial
import shelve
import matplotlib.pyplot as plt
import simplekml
import config
import itertools


def get_XY_pos(relativeNullPoint, p):
    """ Calculates X and Y distances in meters.
    """
    deltaLatitude = p.latitude - relativeNullPoint.latitude
    deltaLongitude = p.longitude - relativeNullPoint.longitude
    latitudeCircumference = 40075160 * cos(relativeNullPoint.latitude * pi / 180)
    resultX = deltaLongitude * latitudeCircumference / 360
    resultY = deltaLatitude * 40008000 / 360
    return resultX, resultY


def meter_distance_to_coord_distance(meter_distance):
    # the following (non-exact) calculation yields a conversion from meter distances 
    # to lat-lon distance which should be accurate enough for Israel
        #tel_aviv = [32.071589, 34.778227]
        #rehovot = [31.896010, 34.811525]
        #meter_distance = 19676
        #delta_coords = [tel_aviv[0]-rehovot[0], tel_aviv[1]-rehovot[1]]
        #delta_coords_norm = (delta_coords[0]**2 + delta_coords[1]**2)**0.5
        #meters_over_coords = meter_distance/delta_coords_norm # equals 110101    
    meters_over_coords = 110101.0
    return meter_distance/meters_over_coords

def query_coords(point_tree, query_coords, query_accuracies):
    if isinstance( query_accuracies, ( int, long, float ) ):
        res = point_tree.query_ball_point(query_coords, query_accuracies)
    else:
        res = [point_tree.query_ball_point(query_coords[i], query_accuracies[i]) for i in xrange(len(query_accuracies))]
    return res
