"""orbits.py

"""

import numpy as np
import matplotlib.pyplot as plt

from orbits_toolkit import orbital_elements_from_state
from orbits_toolkit import orbital_state_from_elements
from vector import Vector2D
from conics import ConicSection
from toolkit import angle_add, angle_sub

from numpy import pi as PI

def flight_heading(position_angle, flight_angle):
    """The direction of travel."""
    # zenith angle is angle between velocity and straight up
    _zenith = angle_sub(0.5 * PI, flight_angle)
    
    return angle_add(position_angle, _zenith)

class OrbitalElements:
    """Classical orbital elements."""
    def __init__(self, 
                 semilatus_rectum, eccentricity, 
                 periapsis_angle, true_anomaly):
        """Initialiser."""
        self.semilatus_rectum = semilatus_rectum
        self.eccentricity     = eccentricity
        self.periapsis_angle  = periapsis_angle
        self.true_anomaly     = true_anomaly
                
    def __repr__(self):
        return f"OrbitalElements({', '.join(map(repr, self._elements))})"

    def __iter__(self):
        return iter(self._elements)
    
    @property
    def _elements(self):
        return (
            self.semilatus_rectum, 
            self.eccentricity, 
            self.periapsis_angle, 
            self.true_anomaly
        )

    @classmethod
    def from_state(cls, state, gm):
        """Create OrbitalElements from an OrbitalState."""
        _components = (
            state.position_radius,
            state.position_angle,
            state.flight_speed,
            state.flight_angle
        )
        
        _elements = orbital_elements_from_state(*_components, gm)

        return cls(*_elements)

    
class OrbitalState:
    def __init__(self, position, velocity):
        """Initialiser."""
        # vectors
        self.position = position
        self.velocity = velocity

        # convenience accessors
        # position
        self.position_radius = abs(self.position)
        self.position_angle  = self.position.angle()

        # velocity speed
        self.flight_speed = abs(self.velocity)
        
        # velocity direction
        self.flight_heading = self.velocity.angle()
        self.zenith_angle = angle_sub(
            self.flight_heading, self.position_angle
        )
        self.flight_angle = angle_sub(0.5 * PI, self.zenith_angle)
        
        
    def __repr__(self):
        return f"OrbitalState({self.position!r}, {self.velocity!r})"
    
    
    @classmethod
    def from_state_components(cls, 
                              position_radius, position_angle, 
                              flight_speed, flight_angle):
        """Create OrbitalState from size & direction of position & velocity."""
        # position vector
        position = Vector2D.from_polar(position_radius, position_angle)
        
        # velocity vector
        _flight_heading = flight_heading(position_angle, flight_angle)
        velocity = Vector2D.from_polar(flight_speed, _flight_heading)
        
        return cls(position, velocity)
        
    @classmethod
    def from_elements(cls, elements, gm):
        """Create OrbitalState from OrbitalElements."""
        # extract orbital elements
        _elements = list(elements)

        # calculate components
        _components = orbital_state_from_elements(*_elements, gm)

        return cls.from_state_components(*_components)

def conic_from_elements(elements):
    """Calculate conic section from a complete set of orbital elements."""
    return ConicSection(
        elements.eccentricity, 
        elements.semilatus_rectum, 
        elements.periapsis_angle,
    )

def conic_from_state(state, gm):
    """Calculate conic section from orbital state."""
    # convert to orbital elements
    _elements = OrbitalElements.from_state(state, gm)

    # extract the conic section
    return conic_from_elements(_elements)


def trajectory_from_state(state, gm, *args, **kwargs):
    """Calculate the 2D trajectory from the orbital state."""
    _conic = conic_from_state(state, gm)
    return _conic.locus(*args, **kwargs)

