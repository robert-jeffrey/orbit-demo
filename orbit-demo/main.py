import matplotlib.pyplot as plt
from visualisation import OrbitImpulseUI

FIG_TITLE = 'OrbitDemo'
FIGSIZE = [16, 8]
PAGE_TITLE = 'Visualising Orbits'

AUTHOR = 'robert-jeffrey'
YEAR = '2023'

INIT_SPEED, INIT_ANGLE = 1., 0.
SCALE = 1

def copyright_notice(author, year):
    return f"\u00A9 {author} {year}"

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
            0.99, 0.01, copyright_notice(AUTHOR, YEAR),
            ha='right', va='bottom',
            fontsize='xx-small',
        )

        ui = OrbitImpulseUI(fig, INIT_SPEED, INIT_ANGLE, SCALE)
        plt.show()

if __name__=="__main__":
    main()
