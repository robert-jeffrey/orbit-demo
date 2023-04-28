"""artists.py


"""

# third party imports
import numpy as np
import matplotlib.patches as mpatches

# local imports
from vector import Vector2D
from toolkit import rotate_2d


def vector_endpoints(vector, pos, scale=1):
    """Return tail and head of vector starting at pos."""
    # tail of vector arrow
    tail = pos

    # head of vector arrow
    head = tail + vector * scale
    
    return tail, head

def plot_vector(ax, vector, pos, scale=1, **kwargs):
    """Plot a vector arrow on an Axes."""
    _tail, _head = vector_endpoints(vector, pos, scale)
    
    # the arrow patch object
    _arrow = mpatches.FancyArrowPatch(tuple(_tail), tuple(_head), **kwargs)
    
    return ax.add_patch(_arrow)


def conic_line_of_apsides(conic):
    """End points for line of apsides."""
    _rp, _ra = conic.periapsis(), conic.apoapsis()
    if conic.e > 1:
        _x = np.asarray([-_ra, -_rp])
        
    else:
        _x = np.asarray([_rp, -_ra])

    _y = np.asarray([0, 0])
    return rotate_2d(_x, _y, -conic.angle0)
    

class ConicArtist:
    """A line representing a conic section."""
    def __init__(self, ax, conic, **kwargs):
        """Initialiser."""
        self.locus, = ax.plot(*conic.locus(), **kwargs)
#        self.line_of_apsides, = ax.plot(*conic_line_of_apsides(conic), c='k')
        
    def update(self, new_conic):
        self.locus.set_data(*new_conic.locus())
#        self.line_of_apsides.set_data(*conic_line_of_apsides(new_conic))
        return self.locus, 
        

class VectorArrowArtist:
    """An arrow representing a vector."""
    def __init__(self, ax, vect, pos, scale=1, arrowprops={}):
        """Initialiser."""
        self.scale = scale
        self.arrow = plot_vector(ax, vect, pos, self.scale, **arrowprops)
        
    def update(self, new_vect, new_pos):
        _tail, _head = vector_endpoints(new_vect, new_pos, scale=self.scale)
        self.arrow.set_positions(tuple(_tail), tuple(_head))        
        return self.arrow,         
    
class OrbitalStateArtist(VectorArrowArtist):
    """An arrow representing orbital state velocity vector."""
    def __init__(self, ax, state, scale=1, arrowprops={}):
        """Initialiser."""
        super().__init__(ax, state.velocity, state.position, scale, arrowprops)
        
    def update(self, new_state):
        super().update(new_state.velocity, new_state.position)

# class ImpulseArtist:
#     """An arrow representing the difference between two states."""
#     def __init__(self, ax, state0, state1, scale, arrowprops={}):
#         """Initialiser."""
#         self.scale = scale
        
#         _, _tail = vector_endpoints(state0.velocity, state0.position, self.scale)
#         _, _head = vector_endpoints(state1.velocity, state1.position, self.scale)
        
#         self.arrow = plot_vector(ax, _tail, _head, scale=1, **arrowprops)
        
#     def update(self, new_state0, new_state1):
#         _, _tail = vector_endpoints(new_state0.velocity, new_state0.position, self.scale)
#         _, _head = vector_endpoints(new_state1.velocity, new_state1.position, self.scale)
#         self.arrow.set_positions(tuple(_tail), tuple(_head))        

class ImpulseArtist:
    """An arrow representing the difference between two states."""
    def __init__(self, ax, state, impulse, scale, arrowprops={}):
        """Initialiser."""
        self.scale = scale

        # find the tip of the state vector
        _, _tail = vector_endpoints(state.velocity, state.position, self.scale)
        
        # plot the arrow
        self.arrow = plot_vector(ax, impulse, _tail, scale=self.scale, **arrowprops)
        
    def update(self, new_state, new_impulse):
        _, _tail = vector_endpoints(new_state.velocity, new_state.position, self.scale)
        _, _head = vector_endpoints(new_impulse, _tail, self.scale)
        self.arrow.set_positions(tuple(_tail), tuple(_head))        