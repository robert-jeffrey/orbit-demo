
from orbits import OrbitalState
from vector import Vector2D
from toolkit import rotate_2d


def add_impulse_vector(state, delta_v):
    """Create new OrbitalSate by applying a (vector) delta-v."""
    _position = Vector2D(*state.position)
    _velocity = state.velocity + delta_v
    return OrbitalState(_position, _velocity)

def calculate_impulse(state, magnitude, angle):
    """Calculate an impulse vector from its components relative to velocity."""
    # calculate impulse vector relative to velocity
    _delta_v = Vector2D.from_polar(magnitude, angle)
    
    # rotate into x-y frame
    # note sign - rotating the vector, not the coordinates
    return Vector2D(*rotate_2d(*_delta_v, -state.flight_heading))    

def add_impulse(state, magnitude, angle):
    """Create new OrbitalState from size and direction of impulse."""
    
    delta_v = calculate_delta_v(state, magnitude, angle)
    
    # apply impulse
    return add_impulse_vector(state, delta_v)