"""toolkit.py

Miscellaneous tools

"""

import numpy as np
from numpy import pi as PI

TWO_PI = 2. * PI

def cartesian_from_polar2d(radius, azimuth):
    """Cartesian (x, y) coordinates from radius & azimuth."""
    return radius * np.cos(azimuth), radius * np.sin(azimuth)


def angle_add(angle, other):
    return (angle + other) % TWO_PI
    
def angle_sub(angle, other):
    return ((angle % TWO_PI) - (other % TWO_PI)) % TWO_PI



def rotate_2d(x, y, angle):
    """Counterclockwise rotation of Cartesian coordinates."""
    _c, _s = np.cos(angle), np.sin(angle)
    return (
        ( x * _c + y * _s),
        (-x * _s + y * _c)
    )