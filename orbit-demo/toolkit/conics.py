"""conics.py


"""

import numpy as np

from toolkit import cartesian_from_polar2d
from toolkit import rotate_2d
from toolkit import angle_add, angle_sub

PI = np.pi
TWO_PI = 2 * PI


def conic_radius(angle, e, l=1):
    """Radius of conic section at true anomaly angle."""
    return l / (1 + e * np.cos(angle))

def conic_semimajor_axis(e, l):
    return l / (1 - e * e)

def conic_periapsis(e, l):
    return l / (1 + e)

def conic_apoapsis(e, l):
    return l / (1 - e)


class ConicSection:
    """A simple conic section."""
    def __init__(self, e, l=1, angle0=0):
        self.e, self.l = e, l
        self.angle0 = angle0

    def anomaly(self, angle):
        return angle_sub(angle, self.angle0)
        
    def radius(self, angle):
        return conic_radius(self.anomaly(angle), self.e, self.l)

    def position(self, angle):
        _r = self.radius(angle)
        return cartesian_from_polar2d(_r, angle)
    
    def periapsis(self):
        return conic_periapsis(self.e, self.l)
    
    def apoapsis(self):
        return conic_apoapsis(self.e, self.l)

    def locus(self, num_segment=3000, polar=False):
        """Points on the principal branch of the conic section."""
        # determine range
        _max = (PI if self.e < 1 else np.arccos(-1./self.e))
    
        # compute anomaly points
        _anomaly = np.linspace(-1, 1, num_segment+1) * _max
        if self.e >= 1:
            _anomaly = _anomaly[1:-1]
    
        # compute radii
        r = conic_radius(_anomaly, self.e, self.l)

        if polar:
            return r, angle_sub(_anomaly, -self.angle0)
        else:
            # compute coordinates in apside-centred frame
            _x, _y = cartesian_from_polar2d(r, _anomaly)
    
            # rotate from apside-centred frame to reference frame 
            return rotate_2d(_x, _y, -self.angle0)
    
