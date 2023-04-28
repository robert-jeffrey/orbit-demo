"""plotting.py


"""

import matplotlib.pyplot as plt


def plot_conic_section(ax, conic, **kwargs):
    """Plot a conic section as a locus of points on an Axes."""
 
    # find the locus
    _x, _y = conic.locus()
    
    # plot it
    return ax.plot(_x, _y, **kwargs)

def plot_vector(ax, vector, pos, scale=1, arrowprops={}):
    """Plot a vector arrow on an Axes."""
    # tail of vector arrow
    tail = pos

    # head of vector arrow
    head = tail + vector * scale
    
    return ax.annotate('', xy=head, xytext=pos, arrowprops=arrowprops)