import matplotlib.pyplot as plt
from visualisation import OrbitImpulseUI


INIT_SPEED, INIT_ANGLE = 1., 0.
SCALE = 1

def main():    
    with plt.style.context('fivethirtyeight'):
        fig = plt.figure('Visualising Orbits')
        ui = OrbitImpulseUI(fig, INIT_SPEED, INIT_ANGLE, SCALE)
        plt.show()


main()
