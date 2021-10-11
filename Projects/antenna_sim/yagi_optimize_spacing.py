
import numpy as np
from numpy.lib.function_base import blackman
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse
from PyNEC import *
import numpy as np
from pprint import pprint
from antenna_util import *
from context_clean import *
import math
from engineering_notation import EngNumber
from pprint import pprint
from json import loads
from yagi_3_element import yagi3

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Simulate a 3-element Yagi antenna')
    parser.add_argument('--freq', default=146.52, help='Driven element resonant frequency in MHz')
    parser.add_argument('--elespacing', default="[0.25,0.25]", help='Element Spacing from back to front in wavelengths')
    parser.add_argument('--elefactor', default="[1.04,1.00,0.96]", help='Element length factor from back to front')    
    args = parser.parse_args()

    # loop here!
    spaces = []
    fwd_gains = []

    spacing = loads(args.elespacing)
    for space_factor in range(50, 150, 5):
        space_list = [x * space_factor / 100 for x in spacing] # ugh - a list comprenension
        pprint(space_list)
        fwd_gain = yagi3(freq=float(args.freq), 
                         element_spacing=space_list,
                         element_factor=loads(args.elefactor))
        print(fwd_gain)
        spaces.append(space_list[0])
        fwd_gains.append(fwd_gain)
    print('space   fwd gain')
    for i in range(0, len(spaces)):
          print(f'{spaces[i]}    {EngNumber(fwd_gains[i])}')
    plt.plot(spaces, fwd_gains, 'b.')
    plt.xlabel("Element Spacing (wavelengths)")
    plt.ylabel("Antenna Gain")
    plt.title('3 Element Yagi Simulation')
    plt.show()
    print('pau')

    spaces_back = []
    spaces_front = []
    fwd_gains = []
    max_fwd_gain = 0
    max_back = 0
    max_front = 0
    for space_factor_back in range(2, 200, 20):
        two_d_spaces = []
        two_d_fwd_gains = []
        for space_factor_front in range(2, 200, 20):
            space_list = [spacing[0] * space_factor_back / 100, spacing[1] * space_factor_front /100] # ugh - a list comprenension
            pprint(space_list)
            fwd_gain = yagi3(freq=float(args.freq), 
                             element_spacing=space_list,
                             element_factor=loads(args.elefactor))
            print(fwd_gain)
            spaces_back.append(space_list[0])
            spaces_front.append(space_list[1])
            fwd_gains.append(fwd_gain)
            two_d_spaces.append(space_list[1])
            two_d_fwd_gains.append(fwd_gain)
            if max_fwd_gain < fwd_gain:
                max_fwd_gain = fwd_gain
                max_back = space_list[0]
                max_front = space_list[1]
        # plt.plot(two_d_spaces, two_d_fwd_gains, 'b.')
        # plt.xlabel("Element Spacing (wavelengths)")
        # plt.ylabel("Antenna Gain")
        # plt.title('3 Element Yagi with Reflector Spacing  = ' + str(spacing[0] * space_factor_back / 100))
        # plt.show()
        # print('pau')
        
        

        
    print(f'maximium gain of {max_fwd_gain} at {max_back} and {max_front}')

    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Plot the surface.
    
    surf = ax.plot_trisurf(spaces_back, spaces_front, np.array(fwd_gains), cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
    ax.set_title('Effects of Element Spacing on Yagi Performance')
    ax.set_xlabel('Reflector Spacing')
    ax.set_ylabel('Director Spacing')
    ax.set_zlabel('Gain')
    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    # ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    # rotate the axes and update
    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)


    plt.show()

    print('pau')