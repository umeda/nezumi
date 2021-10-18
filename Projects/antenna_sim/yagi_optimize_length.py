'''
Copyright 2021 Nezumi Workbench

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
import matplotlib.collections as collections

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Simulate a 3-element Yagi antenna')
    parser.add_argument('--freq', default=146.52, help='Driven element resonant frequency in MHz')
    parser.add_argument('--elespacing', default="[0.25,0.25]", help='Element Spacing from back to front in wavelengths')
    parser.add_argument('--elefactor', default="[1.04,1.00,0.96]", help='Element length factor from back to front')    
    args = parser.parse_args()

    # loop here!
    lens = []
    fwd_gains = []

    min_swr_lens = []    
    min_swr_freqs = []
    min_freqs_data = {'x': min_swr_lens, 'freqs': min_swr_freqs}

    max_swr_lens = []    
    max_swr_freqs = []
    max_freqs_data = {'x': max_swr_lens, 'freqs': max_swr_freqs}

    min_vswr_lens = []
    min_vswrs = []
    min_vswrs_data = {'x': min_vswr_lens, 'swrs': min_vswrs}

    lengths = loads(args.elefactor)
    for len_factor in range(0, 100, 1):  # was 4
        ref_len = 0.985
        drv_ele_lam = str(EngNumber(0.25 * ref_len))
        # Reflector is half a wavelength.
        # len_list = [reflector_len,  
        #             reflector_len * (1.0 - len_factor / 1000), 
        #             reflector_len * (1.0 - len_factor / 1000) ** 2]
        # Driven element is half a wavelength.
        len_list = [ref_len * (1.0 + len_factor / 1000),  
                    ref_len, 
                    ref_len * (1.0 - len_factor / 1000)]
        pprint(len_list)
        perf_params = yagi3(freq=float(args.freq), 
                         element_spacing=loads(args.elespacing),
                         element_factor=len_list, show_plots=False)
        pprint(perf_params)
        lens.append(len_factor / 1000)
        fwd_gains.append(perf_params['fwd_gain'])
        if perf_params['min_swr_freq'] != 0.0:
            min_freqs_data['x'].append(len_factor / 1000)
            min_freqs_data['freqs'].append(perf_params['min_swr_freq'])
        if perf_params['max_swr_freq'] != 0.0:
            max_freqs_data['x'].append(len_factor / 1000)
            max_freqs_data['freqs'].append(perf_params['max_swr_freq'])
        if perf_params['min_swr'] != 999999999.0:
            min_vswrs_data['x'].append(len_factor / 1000)
            min_vswrs_data['swrs'].append(perf_params['min_swr'])
 
    fig, ax = plt.subplots()
    ax.plot(lens, fwd_gains, 'b-')
    ax.set_title(str(float(args.freq)) + " MHz, 3 Element Yagi Simulation\n space factor = "   + str(loads(args.elespacing)[0]) )
    ax.set_xlabel("Element Length Adjustment (fraction)")
    ax.set_ylabel("Antenna Gain")
    ax.tick_params(axis='y', labelcolor='blue')
    ax2 = ax.twinx()
    ax2.plot(min_vswrs_data['x'], min_vswrs_data['swrs'], 'g-')
    ax2.set_ylabel('Lowest SWR')
    ax2.hlines(2.0, 0, min_vswrs_data['x'][-1],colors='red', linestyles='dashed')
    ax2.text(0, 2, '   max SWR', ha='left', va='bottom')
    ax2.tick_params(axis='y', labelcolor='green')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(lens, fwd_gains, 'b-')
    ax.set_title("3 Element Yagi Simulation\ndesign freq = " + str(float(args.freq)) + " MHz, space factor = "   + str(loads(args.elespacing)[0]) )
    ax.set_xlabel("Element Length Adjustment (fraction)")
    ax.set_ylabel("Antenna Gain")
    ax.tick_params(axis='y', labelcolor='blue')
    ax2 = ax.twinx()
    ax2.plot(min_freqs_data['x'], min_freqs_data['freqs'], 'g-')
    ax2.plot(max_freqs_data['x'], max_freqs_data['freqs'], 'g-')
    ax2.set_ylabel('Frequency with SWR < 2 (MHz)')
    ax2.hlines([144,148], 0, min_vswrs_data['x'][-1],colors='red', linestyles='dashed')
    ax2.text(0, 144, '   lower band edge', ha='left', va='bottom')
    ax2.text(0, 148, '   upper band edge', ha='left', va='top')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.fill_between(max_freqs_data['x'], min_freqs_data['freqs'], max_freqs_data['freqs'], color='green', alpha=0.2)
    plt.show()
    print('pau')
