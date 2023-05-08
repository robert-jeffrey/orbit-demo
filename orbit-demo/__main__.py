import matplotlib.pyplot as plt
from visualisation import OrbitImpulseUI

FIG_TITLE = 'OrbitDemo'
FIGSIZE = [16, 8]
PAGE_TITLE = 'Visualising Orbits'

COPYRIGHT_NOTICE = '\u00A9 robert-jeffrey'

INIT_SPEED, INIT_ANGLE = 1., 0.
SCALE = 1

def main():    
    with plt.style.context('fivethirtyeight'):
        fig = plt.figure(PAGE_TITLE, FIGSIZE)

        fig.suptitle(
            FIG_TITLE,
            x=0.1, y=0.95,
            ha='left',
            fontsize='xx-large',
            fontweight='bold',
        )

        fig.text(
            0.99, 0.01, COPYRIGHT_NOTICE,
            ha='right', va='bottom',
            fontsize='xx-small',
        )

        ui = OrbitImpulseUI(fig, INIT_SPEED, INIT_ANGLE, SCALE)
        plt.show()


main()
