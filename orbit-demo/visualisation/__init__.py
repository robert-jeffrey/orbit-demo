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

# axes positions
MAIN_AXES = [0.05, 0.15, 0.5, 0.7]
SPEED_SLIDER = [0.60, 0.3, 0.15, 0.03]
ANGLE_SLIDER = [0.80, 0.3, 0.15, 0.03]
IMPULSE_SPEED_SLIDER = [0.60, 0.15, 0.15, 0.03]
IMPULSE_ANGLE_SLIDER = [0.80, 0.15, 0.15, 0.03]
RESET_BUTTON = [0.85, 0.1, 0.1, 0.04]
#MAIN_AXES = [0.125, 0.25, 0.775, 0.63]
#SPEED_SLIDER = [0.10, 0.150, 0.3, 0.03]
#ANGLE_SLIDER = [0.10, 0.075, 0.3, 0.03]
#IMPULSE_SPEED_SLIDER = [0.60, 0.150, 0.3, 0.03]
#IMPULSE_ANGLE_SLIDER = [0.60, 0.075, 0.3, 0.03]
#RESET_BUTTON = [0.8, 0.025, 0.1, 0.04]

# label positions
VELOCITY_LABEL = [0.60, 0.375]
IMPULSE_LABEL = [0.60, 0.225]

def get_conic_scale(conic):
    """Determine characteristic length scale for conic."""
    e, l = conic.e, conic.l
    a = conic_semimajor_axis(e, l)
    return 2 * (a if e < 1 else abs(a) * e)
     
def set_xylims(ax, lim, ratio=1):
    """Set square axes limits for ax."""
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim*ratio, lim*ratio)


def format_slider_label(slider, xy, va, ha):
    label = slider.label
    label.set_position(xy)
    label.set_verticalalignment(va)
    label.set_horizontalalignment(ha)
    return label

def format_slider(slider):
    """Formats the slider label and text value."""
    label = slider.label
    label.set_position((0.0, 1.02))
    label.set_verticalalignment('bottom')
    label.set_horizontalalignment('left')

    valtext = slider.valtext
    valtext.set_position((1.0, 1.02))
    valtext.set_verticalalignment('bottom')
    valtext.set_horizontalalignment('right')

    return label, valtext


class OrbitImpulseUI:
    def __init__(self, fig, initial_speed, initial_angle, speed_scale):
        """Initialiser."""
        self.figure = fig
        
        # calculate initial state
        _initial_state = OrbitalState.from_state_components(
            1, 0, initial_speed, initial_angle
        )
        _initial_conic = conic_from_state(_initial_state, gm=1)
        
        # add main display axes
        self.ax = fig.add_axes(MAIN_AXES, projection='polar')
        self.ax.grid(True)

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
            mpatches.Circle((0, 0), (0.10), ec='none', fc='C0', zorder=10,
                            transform=self.ax.transData._b),
            mpatches.Circle((1, 0), (0.05), ec='none', fc='C0', zorder=10,
                            transform=self.ax.transData._b),
        ]
        for _artist in _static_artists:
            self.ax.add_artist(_artist)

        # static labels
        self.figure.text(
            *VELOCITY_LABEL, 'Velocity',
            ha='left', va='bottom',
            fontweight='bold',
        )
        self.figure.text(
            *IMPULSE_LABEL, 'Impulse',
            ha='left', va='bottom',
            fontweight='bold',
        )

        
        # add slider to control the speed
        _speed_slider = Slider(
            ax=self.figure.add_axes(SPEED_SLIDER),
            label=r'Speed / $v_\mathdefault{circ}$',
            valmin=0.1,
            valmax=2.0,
            valinit=initial_speed,
            valstep=0.01,
            valfmt='%.2f',
            facecolor='C0',
        )

        # add slider to control the angle
        _angle_slider = Slider(
            ax=self.figure.add_axes(ANGLE_SLIDER),
            label='Angle',
            valmin=-89,
            valmax=+89,
            valinit=initial_angle,
            valstep=1.0,
            valfmt='%.0f\u00B0',
            facecolor='C0',
        )

        # add sliders to control the impulse speed & angle
        _impulse_speed_slider = Slider(
            ax=self.figure.add_axes(IMPULSE_SPEED_SLIDER),
            label=r'Magnitude / $v_\mathdefault{circ}$',
            valmin=0,
            valmax=1.,
            valinit=0,
            valstep=0.01,
            valfmt='%.2f',
            facecolor='C1',
        )

        _impulse_angle_slider = Slider(
            ax=self.figure.add_axes(IMPULSE_ANGLE_SLIDER),
            label='Direction',
            valmin=-180,
            valmax=+180,
            valinit=0,
            valstep=1.0,
            valfmt='%.0f\u00B0',
            facecolor='C1',
        )
        
        # create a `matplotlib.widgets.Button` to reset sliders to initial
        # values
        _reset_button = Button(
            ax=self.figure.add_axes(RESET_BUTTON),
            label='Reset',
            hovercolor='0.975',
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

        for _, slider in self.sliders.items():
            format_slider(slider)

        # register callbacks
        for _, slider in self.sliders.items():
            slider.on_changed(self.update)

        self.widgets['reset_button'].on_clicked(self.reset)

        # set axis scale - this has to happen after drawing?
        _scale = 1.3 * get_conic_scale(_initial_conic)
        self.ax.set_rmax(_scale)


    def reset(self, event):
        for _, slider in self.sliders.items():
            slider.reset()
        
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
#        set_xylims(self.ax, 1.1 * _scale, ratio=0.5)
        self.ax.set_rmax(_scale)
        
        # redraw the figure
        self.figure.canvas.draw_idle()
    
    
    
    
if __name__=="__main__":
    INIT_SPEED, INIT_ANGLE = 1., 0.
    SCALE = 1
    
    with plt.style.context('fivethirtyeight'):
        fig = plt.figure('Visualising Orbits')
        ui = OrbitImpulseUI(fig, INIT_SPEED, INIT_ANGLE, SCALE)
        plt.show()
        
