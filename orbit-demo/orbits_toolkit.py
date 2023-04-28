"""orbits_toolkit.py

Functions to convert between orbital elements and orbital state.

"""

import numpy as np

from conics import conic_radius
from toolkit import angle_sub, angle_add



def orbital_elements_from_state(position_radius, position_angle, 
                                flight_speed, flight_angle, gm):
    """Calculate object's orbital elements from position & velocity."""
    # precompute trig
    _c, _s = np.cos(flight_angle), np.sin(flight_angle)
    
    # normalised speed parameter = (v / vcirc)**2
    _vsq = flight_speed * flight_speed * position_radius / gm
    
    # size and shape
    l = position_radius * _vsq * _c * _c
    e = np.sqrt(1 - 2 * _vsq * (1 - 0.5 * _vsq) * _c * _c)
    
    # orientation - true anomaly
    _ex = _vsq * _c * _c - 1
    _ey = _vsq * _s * _c
    true_anomaly = np.arctan2(_ey, _ex)
    
    # orientation - argument of periapsis
    periapsis_angle = angle_sub(position_angle, true_anomaly)

    # orbital elements
    return l, e, periapsis_angle, true_anomaly


def orbital_state_from_elements(l, e, periapsis_angle, true_anomaly, gm):
    """Calculate object's position & velocity from orbital elements."""
    # precompute trig
    _c, _s = np.cos(true_anomaly), np.sin(true_anomaly)
    
    # orbital angle
    position_angle = angle_add(periapsis_angle, true_anomaly)
    
    # orbital distance
    position_radius = conic_radius(true_anomaly, e, l)
    
    # flight speed
    _vsq = 2 * (1 + e * _c) - (1 - e * e)
    flight_speed = np.sqrt(_vsq * gm / l)

    # flight path angle
    _vr = e * _s
    _vt = 1 + e * _c
    flight_angle = np.arctan2(_vr, _vt)
    
    # orbital state
    return position_radius, position_angle, flight_speed, flight_angle
