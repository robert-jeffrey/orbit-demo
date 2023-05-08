"""_conic_artists.py

"""

# third party imports
import numpy as np
import matplotlib.patches as mpatches

# local imports
from toolkit.vector import Vector2D
from toolkit import rotate_2d


def conic_line_of_apsides(conic):
    """End points for line of apsides."""
    _rp, _ra = conic.periapsis(), conic.apoapsis()
    if conic.e > 1:
        _x = np.asarray([-_ra, -_rp])
        
    else:
        _x = np.asarray([_rp, -_ra])

    _y = np.asarray([0, 0])
    return rotate_2d(_x, _y, -conic.angle0)
    
def conic_polar_locus(conic):
    r, theta = conic.locus(polar=True)
    return theta, r



class ConicArtist:
    """A line representing a conic section."""
    def __init__(self, ax, conic, **kwargs):
        """Initialiser."""
        self.locus, = ax.plot(*conic_polar_locus(conic), **kwargs)
        
    def update(self, new_conic):
        self.locus.set_data(*conic_polar_locus(new_conic))
        return self.locus, 
        
