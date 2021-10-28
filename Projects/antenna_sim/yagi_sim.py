'''
Copyright 2021 Nezumi Workbench

This library function returns performance paramters for a 3 element yagi,
given certain design parameters.

    Design Parameters:

        Number of Elements      
        Frequency
        Element Spacing
        Element Length
        Element Diameter
        Units
        Include Radiation and SWR Plots
        Frequency Range for SWR Plot 

    Performance Parameters:
    
        Gain
        Best SWR
        Min and Max Frequencies for SWR < 2
        Radiation Pattern
        SWR Over Frequency
        Beam Width
        FB Ratio


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import numpy as np
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

def yagix(freq=146.52, element_spacing=[0.4780,0.4780], element_length=[0.9943,0.9560,0.9178], units='m', show_plots=False ):

    #TODO: return element lengths in wavelengths or something like that.
    
    # convert to meters
    if units == 'mm':
        element_spacing = [space / 1000 for space in element_spacing]
        element_length = [element / 1000 for element in element_length]
    elif units == 'feet':
        element_spacing = [space * 12 * 25.4 / 1000 for space in element_spacing]
        element_length = [element * 12 * 25.4 / 1000 for element in element_length]
    elif units == 'in':
        element_spacing = [space * 25.4 / 1000  for space in element_spacing]
        element_length = [element * 25.4 / 1000 for element in element_length]
    elif units == 'lambda':
        element_spacing = [space * 300 / freq for space in element_spacing]
        element_length = [element * 300 / freq for element in element_length]



    # print(type(element_spacing))
    pprint(element_spacing)
    pprint(element_length)
    # creation of a nec context
    context=nec_context()
    # get the associated geometry
    geo = context.get_geometry()

    #Design Parameters
    # freq = 146.520  # Design Frequency in MHz
    wire_diameter_mm = 2  # Element Diameter in mm
    # element_spacing = [0.25, 0.25]  # spacing from reflector in wavelengths- reflector to driven, driven to director 1, director 1 to director 2, etc.
    # element_factor = [1.04, 0.96]  # percentage of driven element length - reflector, director 1, director2, etc

    # Derived Values
    wire_rad = wire_diameter_mm / 2000 
    length_ft = 468.0 / freq # dipole formula from ARRL
    halfwave = length_ft * 12 * 25.4 / 1000  #  driven element length in millimeters.
    drv_len = element_length[1]
    # print(drv_len)
    num_segs = 35 # Number of segments per Element. More segments = increased accuracy and longer processing time.
    excitation_element_num = 1 #  Element to which excitation is applied.

    # Add Elements
    element_tag = 1
    center      = np.array([0, 0, 0])
    half_height = np.array([0  , 0, drv_len/2.0])
    top         = center + half_height
    bottom      = center - half_height
    nr_segments = 35
    geo.wire(element_tag, nr_segments, bottom[0],bottom[1],bottom[2], top[0], top[1], top[2], wire_rad, 1.0, 1.0)
    # geo.wire(tag, num_segs, x1, y1, z1, x2, y2, z2, radius, rtap, rrad)


    #reflector
    ref_len = element_length[0]
    pos = -1 * element_spacing[0]  # negative because it's behind the driven element
    element_tag = 2
    center      = np.array([pos, 0, 0]) # back
    half_height = np.array([0  , 0, ref_len/2.0])
    top         = center + half_height
    bottom      = center - half_height
    nr_segments = 35
    geo.wire(element_tag, nr_segments, bottom[0],bottom[1],bottom[2], top[0], top[1], top[2], wire_rad, 1.0, 1.0)



    #director - iterate through these
    dir_len = element_length[2]
    pos = element_spacing[1]
    element_tag = 3
    center      = np.array([pos, 0, 0])
    half_height = np.array([0  , 0, dir_len/2.0])
    top         = center + half_height
    bottom      = center - half_height
    nr_segments = 35
    geo.wire(element_tag, nr_segments, bottom[0],bottom[1],bottom[2], top[0], top[1], top[2], wire_rad, 1.0, 1.0)

    brass_conductivity = 15600000 # mhos - Need to figure out how to use this.
    # nec.set_wire_conductivity(brass_conductivity)

    context.geometry_complete(0)


    # ground card 
    context.gn_card(-1, 0, 0, 0, 0, 0, 0, 0)  # no ground - floating in free space!

    #add a "ex" card to specify an excitation
    center_seg = int((num_segs + 1) / 2) + 1
    # print(f'Center Segment = {center_seg} of {num_segs}')
    context.ex_card(0, excitation_element_num, center_seg, 0, 0, 0, 0, 0, 0, 0, 0)

    #add a "fr" card to specify the frequency 
    context.fr_card(0, 0, freq, 1) # single frequency to calculate radiation pattern.

    #add a "rp" card to specify radiation pattern sampling parameters and to cause program execution
    '''
    calc_mode	This integer selects the mode of calculation for the radiated field. Some values of (calc_mode) will affect the meaning of the remaining parameters on the card. Options available for calc_mode are:
        O - normal mode. Space-wave fields are computed. An infinite ground plane is included if it has been specified previously on a GN card; otherwise, the antenna is in free space.
        1 - surface wave propagating along ground is added to the normal space wave. This option changes the meaning of some of the other parameters on the RP card as explained below, and the results appear in a special output format. Ground parameters must have been input on a GN card. The following options cause calculation of only the space wave but with special ground conditions. Ground conditions include a two-medium ground (cliff where the media join in a circle or a line), and a radial wire ground screen. Ground parameters and dimensions must be input on a GN or GD card before the RP card is read. The RP card only selects the option for inclusion in the field calculation. (Refer to the GN and GD cards for further explanation.)
        2 - linear cliff with antenna above upper level. Lower medium parameters are as specified for the second medium on the GN card or on the GD card.
        3 - circular cliff centered at origin of coordinate system: with antenna above upper level. Lower medium parameters are as specified for the second medium on the GN card or on the GD card.
        4 - radial wire ground screen centered at origin.
        5 - both radial wire ground screen and linear cliff.
        6 - both radial wire ground screen ant circular cliff.
    n_theta	The number of theta angles.
    n_phi	The number of phi angles.
    output_format	The output format:
    0 major axis, minor axis and total gain printed.
    1 vertical, horizontal ant total gain printed.
    normalization	Controls the type of normalization of the radiation pattern
    0 no normalized gain.
    1 major axis gain normalized.
    2 minor axis gain normalized.
    3 vertical axis gain normalized.
    4 horizontal axis gain normalized.
    5 total gain normalized.
    D	Selects either power gain or directive gain for both standard printing and normalization. If the structure excitation is an incident plane wave, the quantities printed under the heading "gain" will actually be the scattering cross section (a/lambda 2 ) and will not be affected by the value of d. The column heading for the output will still read "power" or "directive gain," however.
    0 power gain.
    1 directive gain.
    A	- Requests calculation of average power gain over the region covered by field points.
    0 no averaging.
    1 average gain computed.
    2 average gain computed, printing of gain at the field points used for averaging is suppressed. If n_theta or NPH is equal to one, average gain will not be computed for any value of A since the area of the region covered by field points vanishes.
    theta0	- Initial theta angle in degrees (initial z coordinate in meters if calc_mode = 1).
    phi0	- Initial phi angle in degrees.
    delta_theta	- Increment for theta in degrees (increment for z in meters if calc_mode = 1).
    delta_phi	- Increment for phi in degrees.
    radial_distance	- Radial distance (R) of field point from the origin in meters. radial_distance is optional. If it is zero, the radiated electric field will have the factor exp(-jkR)/R omitted. If a value of R is specified, it should represent a point in the far-field region since near components of the field cannot be obtained with an RP card. (If calc_mode = 1, then radial_distance represents the cylindrical coordinate phi in meters and is not optional. It must be greater than about one wavelength.)
    gain_norm	- Determines the gain normalization factor if normalization has been requested in the normalization parameter. If gain_norm is zero, the gain will be normalized to its maximum value. If gain_norm is not zero, the gain wi11 be normalized to the value of gain_norm.
    '''

    num_thetas = 91
    num_phis = 91

    NO_GAIN = 0
    MAJOR_GAIN = 1
    MINOR_GAIN = 2
    VERT_GAIN = 3
    HORIZ_GAIN = 4
    TOTAL_GAIN = 5
    norm = TOTAL_GAIN

    POWER_GAIN = 0
    DIREC_GAIN = 1
    pd = POWER_GAIN

    NO_AVG = 0
    AVG_GAIN = 1
    AVG_GAIN_FP = 2
    avg = NO_AVG

    # (0, 0) is looking down from the top
    # (90, 0) is the side view
    theta_0 = 90.0  # from the vertical (z) axis
    phi_0 = 0.0  # from the horizontal (x) axis

    theta_d = 4.0
    phi_d = 4.0

    context.rp_card(0, num_thetas, num_phis, 0, norm, pd, avg, theta_0, phi_0, theta_d, phi_d, 1.0, 0.0)

    #get the radiation_pattern
    rp = context.get_radiation_pattern(0)

    # Gains are in decibels
    gains_db = rp.get_gain()
    gains = 10.0**(gains_db / 10.0)
    thetas = rp.get_theta_angles() * 3.1415 / 180.0
    phis = rp.get_phi_angles() * 3.1415 / 180.0

    fwd_gain = gains[:,0][0]

    if show_plots:
        # Plot stuff
        # import matplotlib.pyplot as plt
        
        ax = plt.subplot(111, polar=True)
        # TODO: np.roll hack needed to make antenna face the right way. Need to figure out why. 
        ax.plot(np.roll(thetas, 23) , gains[:,0], color='r', linewidth=3)
        ax.grid(True)

        # pprint(f'Forward Gain = {fwd_gain}')

        # ax.set_title("3 element yagi - side view", va='bottom')
        ax.set_title(f'3 Element Yagi Radiation Pattern: Side View\nBack Space = {element_spacing[0]}, Front Space = {element_spacing[1]}, Reflector Length = {element_length[0]}, Director Factor = {element_length[2]}')
        plt.savefig("radiation_pattern_%i_MHz.png" % freq)
        plt.show()

    system_impedance = 50  
    start_freq = 140
    stop_freq = 150
    freq_points = 100
    context.fr_card(0, freq_points, start_freq, (stop_freq-start_freq)/freq_points)
    # ifrq_linear_step, count, start_frequency, step_size
    context.xq_card(0) # Execute simulation

    # context.get input parameters could be very useful in debugging
    freqs = []
    vswrs = []
    blah = context.get_input_parameters(0)
    for idx in range(1, freq_points):
        ipt = context.get_input_parameters(idx)
        z = ipt.get_impedance()

        freqs.append(ipt.get_frequency() / 1000000)
        vswrs.append(vswr(z, system_impedance))
            
        # print(f"freq = {EngNumber(ipt.get_frequency(), precision=1)}, SWR = {EngNumber(vswr(z, system_impedance), precision=2)}, z = {EngNumber(system_impedance)}")
    
    if show_plots:
        plt.figure()
        plt.plot(freqs, vswrs)
        plt.title(f'VSWR of a 3 element yagi for a {system_impedance} Ohm system\nBack Space = {element_spacing[0]}, Front Space = {element_spacing[1]}, Reflector Factor = {element_length[0]}, Director Factor = {element_length[2]}')
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("VSWR")
        plt.grid(True)
        filename = "vswr_%i_MHz.png" % freq
        print("Saving plot to file: %s" % filename)
        plt.savefig(filename)
        plt.show()
        # return best swr & freq & fwd gain
        # 
    min_swr_freq = 0.0
    max_swr_freq = 0.0
    min_vswr = 999999999.0
    for idx, swr in enumerate(vswrs):  # must be enumerated if we want the index.
        if swr < 2.0:
            max_swr_freq = freqs[idx]
        if swr < min_vswr:
            min_vswr = swr
    for idx, swr in enumerate(vswrs[::-1]):  # what a strange way to reverse a list!
        if swr < 2.0:
            min_swr_freq = freqs[len(freqs) - idx - 1] # look out for off by 1 error!

    perf_params = {'fwd_gain': fwd_gain,
                   'min_swr_freq': min_swr_freq,
                   'max_swr_freq': max_swr_freq,
                   'min_swr': min_vswr}
    return perf_params
    #return fwd_gain
     
if __name__ == '__main__':

    '''
    driven element length = 0.9560385257985257
    reflector length = 0.9942800668304668
    reflector spacing = 0.47801926289926283
    director length = 0.9177969847665846 
    director spacing = 0.47801926289926283 
    '''

    parser = argparse.ArgumentParser(description = 'Simulate a 3-element Yagi antenna')
    parser.add_argument('--freq', default=146.52, help='Driven element resonant frequency in MHz')
    parser.add_argument('--elelength', default="[0.9943,0.9560,0.9178]", help='Array of element lengths from back to front')
    parser.add_argument('--elespace', default="[0.4780,0.4780]", help='Array of element spacing from back to front')
    parser.add_argument('--units', default='m', choices=['m', 'mm', 'ft', 'in', 'lambda'], help='Units in meters(m), millimeters(mm), feet(ft), inches(in), or wavelengths(lambda)')
    parser.add_argument('--range', default='[140,150]', help='SWR plot range (MHz)')
    parser.add_argument('--showplot', dest='showplot', action='store_true')
    parser.add_argument('--no-showplot', dest='showplot', action='store_false')
    parser.set_defaults(showplot=True)

    args = parser.parse_args()
    pprint(args.showplot)
    perf_params = yagix(freq=float(args.freq), 
          element_spacing=loads(args.elespace),
          element_length=loads(args.elelength),
          show_plots=True)
    print(f'Forward Gain = {perf_params}')
    pprint(args.showplot)
