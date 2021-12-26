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
from yagi_sim import yagix
import matplotlib.collections as collections

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Simulate a 3-element Yagi antenna')
    parser.add_argument('--freq', default=146.52, help='Driven element resonant frequency in MHz')
    parser.add_argument('--elespacing', default="[0.25,0.25]", help='Element Spacing from back to front in wavelengths')
    parser.add_argument('--elefactor', default="[1.04,1.00,0.96]", help='Element length factor from back to front')    
    args = parser.parse_args()

    print(yagix(freq=146.52, element_lengths=[1053.0,899.0,892.0], element_spacing=[208.0,327.0], units='mm', plot_range=[130,170], show_plots=True))
    print(yagix(freq=146.52, element_lengths=[994.0,956.0,917.0],  element_spacing=[478.0,478.0], units='mm', plot_range=[130,170], show_plots=True))

    print('pau')
