"""_vector_artists.py

Artist classes for vectors and orbital states
"""

# third party imports
import numpy as np
import matplotlib.patches as mpatches

# local imports
from toolkit.vector import Vector2D


def vector_endpoints(vector, pos, scale=1):
    """Return tail and head of vector starting at pos."""
    # tail of vector arrow
    tail = pos

    # head of vector arrow
    head = tail + vector * scale
    
    return tail, head

def vector2d_polar(v):
    r, t = v.polar()
    return t, r

def plot_vector(ax, vector, pos, scale=1, **kwargs):
    """Plot a vector arrow on an Axes."""
    _tail, _head = vector_endpoints(vector, pos, scale)
    
    # the arrow patch object
    _arrow = mpatches.FancyArrowPatch(
        vector2d_polar(_tail),
        vector2d_polar(_head),
        **kwargs
    )
    return ax.add_patch(_arrow)


class VectorArrowArtist:
    """An arrow representing a vector."""
    def __init__(self, ax, vect, pos, scale=1, arrowprops={}):
        """Initialiser."""
        self.scale = scale
        self.arrow = plot_vector(ax, vect, pos, self.scale, **arrowprops)
        
    def update(self, new_vect, new_pos):
        _tail, _head = vector_endpoints(new_vect, new_pos, scale=self.scale)
        self.arrow.set_positions(vector2d_polar(_tail), vector2d_polar(_head))
        return self.arrow,

class OrbitalStateArtist(VectorArrowArtist):
    """An arrow representing orbital state velocity vector."""
    def __init__(self, ax, state, scale=1, arrowprops={}):
        """Initialiser."""
        super().__init__(ax, state.velocity, state.position, scale, arrowprops)
        
    def update(self, new_state):
        return super().update(new_state.velocity, new_state.position)

class ImpulseArtist:
    """An arrow representing the difference between two states."""
    def __init__(self, ax, state, impulse, scale, arrowprops={}):
        """Initialiser."""
        self.scale = scale

        # find the tip of the state vector
        _, _tail = vector_endpoints(state.velocity, state.position, self.scale)
        
        # plot the arrow
        self.arrow = plot_vector(
            ax, impulse, _tail, scale=self.scale,
            **arrowprops
        )
        
    def update(self, new_state, new_impulse):
        _, _tail = vector_endpoints(
            new_state.velocity,
            new_state.position,
            self.scale
        )
        _, _head = vector_endpoints(new_impulse, _tail, self.scale)
        self.arrow.set_positions(
            vector2d_polar(_tail),
            vector2d_polar(_head)
        )        
        return self.arrow, 
