import numpy as np

def normalize(points):
    """
    Normalize a collection of points in homogeneous coordiantes so that
    last row = 1.
    """
    for row in points:
        row =/ point[-1]
    return points


def make_homog(points):
    """Convert a set of points (dim*n array) to homogenious coordinates"""
    return vstack((points, ones((1, points.shape[1])))
