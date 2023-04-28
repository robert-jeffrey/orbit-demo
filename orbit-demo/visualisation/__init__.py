"""visualisation.py."""

# third party imports
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider, Button
from numpy import deg2rad

# local imports
from orbits import OrbitalState
from orbits import conic_from_state
from impulses import add_impulse_vector, calculate_impulse
from toolkit.conics import conic_semimajor_axis
from toolkit.vector import Vector2D
from .artists import ConicArtist, OrbitalStateArtist, ImpulseArtist


def get_conic_scale(conic):
    """Determine characteristic length scale for conic."""
    e, l = conic.e, conic.l
    a = conic_semimajor_axis(e, l)
    return 2 * (a if e < 1 else abs(a) * e)
     
def set_xylims(ax, lim, ratio=1):
    """Set square axes limits for ax."""
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim*ratio, lim*ratio)


class OrbitImpulseUI:
    def __init__(self, fig, initial_speed, initial_angle, speed_scale):
        """Initialiser."""
        self.figure = fig
        self.figure.subplots_adjust(bottom=0.25)
        
        # calculate initial state
        _initial_state = OrbitalState.from_state_components(
            1, 0, initial_speed, initial_angle
        )
        _initial_conic = conic_from_state(_initial_state, gm=1)
        
        # add main display axes
        self.ax = fig.add_subplot()
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        
        # set axis scale
        _scale = 1.3 * get_conic_scale(_initial_conic)
        set_xylims(self.ax, 1.1 * _scale, ratio=0.5)
        
        # initialise artists
        _old_orbit = ConicArtist(self.ax, _initial_conic, c='C0', zorder=2)
        
        _old_orbit_state = OrbitalStateArtist(
            self.ax, _initial_state, speed_scale,                              
            arrowprops={'mutation_scale':15, 'zorder':4, 'facecolor':'C0'}
        )

        _new_orbit = ConicArtist(self.ax, _initial_conic, c='C2', zorder=1)
        
        _new_orbit_state = OrbitalStateArtist(
            self.ax, _initial_state, speed_scale,                              
            arrowprops={'mutation_scale':15, 'zorder':3, 'facecolor':'C2'}
        )

        _impulse = ImpulseArtist(
            self.ax, _initial_state, Vector2D(0, 0), speed_scale, 
            arrowprops={'mutation_scale':15, 'zorder':5, 'facecolor':'C1'}
        )
        
        self.artists = {
            'old_orbit' : _old_orbit,
            'old_orbit_state' : _old_orbit_state,
            'new_orbit' : _new_orbit,
            'new_orbit_state' : _new_orbit_state,
            'impulse' : _impulse,
        }
        
        # static artists:
        _static_artists = [
            mpatches.Circle((0, 0), (0.10), ec='none', fc='C0', zorder=10),
            mpatches.Circle((1, 0), (0.05), ec='none', fc='C0', zorder=10),
        ]
        for _artist in _static_artists:
            self.ax.add_artist(_artist)
        
        # add slider to control the speed
        _speed_slider = Slider(
            ax=self.figure.add_axes([0.10, 0.150, 0.3, 0.03]),
            label=r'Speed / $v_{circ}$',
            valmin=0.1,
            valmax=2.0,
            valinit=initial_speed,
        )

        # add slider to control the angle
        _angle_slider = Slider(
            ax=self.figure.add_axes([0.10, 0.075, 0.3, 0.03]),
            label='Angle',
            valmin=-89,
            valmax=+89,
            valinit=initial_angle,
            valfmt='%.0f\u00B0'
        )

        # add sliders to control the impulse speed & angle
        _impulse_speed_slider = Slider(
            ax=self.figure.add_axes([0.60, 0.150, 0.3, 0.03]),
            label=r'Impulse / $v_{circ}$',
            valmin=0,
            valmax=1.,
            valinit=0,
            facecolor='C1',
        )

        _impulse_angle_slider = Slider(
            ax=self.figure.add_axes([0.60, 0.075, 0.3, 0.03]),
            label='Impulse Angle',
            valmin=-180,
            valmax=+180,
            valinit=0,
            valfmt='%.0f\u00B0',
            facecolor='C1',
        )
        
        # create a `matplotlib.widgets.Button` to reset sliders to initial
        # values
        _reset_button = Button(
            ax=self.figure.add_axes([0.8, 0.025, 0.1, 0.04]), 
            label='Reset', 
            hovercolor='0.975'
        )
        
        self.sliders = {
            'speed_slider' : _speed_slider,
            'angle_slider' : _angle_slider,
            'impulse_speed_slider' : _impulse_speed_slider,
            'impulse_angle_slider' : _impulse_angle_slider,
        }
        
        self.widgets = {
            **self.sliders, 
            'reset_button' : _reset_button,
        }
        
        # register callbacks
        _sliders = (
            'speed_slider', 'angle_slider',
            'impulse_speed_slider', 'impulse_angle_slider'
        )
        for _, slider in self.sliders.items():
            slider.on_changed(self.update)
            
        self.widgets['reset_button'].on_clicked(self.reset)
        
    def reset(self, event):
        for _, slider in self.sliders.items():
            slider.reset()
#        self.widgets['speed_slider'].reset()
#        self.widgets['angle_slider'].reset()
        
    def update(self, val):
        # new values
        _speed = self.widgets['speed_slider'].val
        _angle = self.widgets['angle_slider'].val
        _angle = deg2rad(_angle)
        
        _impulse_speed = self.widgets['impulse_speed_slider'].val
        _impulse_angle = self.widgets['impulse_angle_slider'].val
        _impulse_angle = deg2rad(_impulse_angle)
        
        # calculate updated old orbit
        _old_state = OrbitalState.from_state_components(1, 0, _speed, _angle)
        _old_conic = conic_from_state(_old_state, gm=1)

        # calculate updated new orbit
        _impulse = calculate_impulse(_old_state, _impulse_speed, _impulse_angle)
        _new_state = add_impulse_vector(_old_state, _impulse)
        _new_conic = conic_from_state(_new_state, gm=1)
        
        # update orbit artists
        self.artists['old_orbit'].update(_old_conic)
        self.artists['new_orbit'].update(_new_conic)
        
        # update orbit state artists
        self.artists['old_orbit_state'].update(_old_state)
        self.artists['new_orbit_state'].update(_new_state)
        
        # update impulse artist 
        #TODO: clean up? reduce duplication of end point calculation?
        self.artists['impulse'].update(_old_state, _impulse)
        
        # update axis scale
        _scale = 1.3 * max(get_conic_scale(c) for c in (_old_conic, _new_conic))
        set_xylims(self.ax, 1.1 * _scale, ratio=0.5)
        
        # redraw the figure
        self.figure.canvas.draw_idle()
    
    
    
    
if __name__=="__main__":
    INIT_SPEED, INIT_ANGLE = 1., 0.
    SCALE = 1
    
    with plt.style.context('fivethirtyeight'):
        fig = plt.figure('Visualising Orbits')
        ui = OrbitImpulseUI(fig, INIT_SPEED, INIT_ANGLE, SCALE)
        plt.show()
        
