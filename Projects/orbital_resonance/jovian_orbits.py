"""
This script curve-fits and plots angular separation between Jupiter and its moon Ganymede.
It then attempts to check the [4:2:1] tidal lock ratio between Ganymede, Europa and Io.

Amplitudes came from: 
    https://en.wikipedia.org/wiki/Moons_of_Jupiter

The basic technique came from code snippets in Stack Overflow:
    https://stackoverflow.com/questions/16716302/how-do-i-fit-a-sine-curve-to-my-data-with-pylab-and-numpy

Copyright [2020] [Nezumi Workbench]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy as np
from scipy.optimize import curve_fit
import pylab as plt
from pprint import pprint

days = np.array([0, 2, 4, 6, 8, 26])
q = np.arange(0,29,0.1)

ganymede = np.array([148.6, 164.0, -210.6, -92.0, 237.4, -232.5])  # angular separation data

europa = np.array([-67.7, 115.1, -147.2, 151.8, -118.0, -107.5])   # angular separation data
europa_orbit_ratio = 671034 / 1070412 # not enough data to find max - how much smaller than ganymede

io = np.array([0.0, 76.3, 92.6, 57.4, 0.0, -84.4])  # angular separation data
io_orbit_ratio =  421700 / 671034 # not enough data to find max - how much smaller than europa

N = 6 # number of data points

guess_freq = 1
guess_amplitude = 3*np.std(ganymede)/(2**0.5)
guess_phase = 0
guess_offset = 0

p0=[guess_freq, guess_amplitude,
    guess_phase, guess_offset]

# create a sinewave
def my_sine(x, freq, amplitude, phase, offset):
    return np.sin(x * freq + phase) * amplitude + offset

fit = curve_fit(my_sine, days, ganymede, p0=p0)

# recreate the fitted curve using the optimized parameters
pprint(fit[0])
pprint(fit[1])

ganymede_msg = 'Ganymede orbit ' + "{:1.2f}".format(2 * 3.14159 / fit[0][0]) + ' days'
europa_msg = 'Europa orbit ' + "{:1.2f}".format(2 * 3.14159 / fit[0][0]/2) + ' days'
io_msg = 'Io orbit ' + "{:1.2f}".format(2 * 3.14159 / fit[0][0]/4) + ' days'

ganymede_fit = my_sine(q, *fit[0])

fit[0][0] *= 2  # double the freq of ganymede
fit[0][1] *= europa_orbit_ratio  # smaller than ganymede
fit[0][2] += 3.14159  # 180 degrees out of phase from ganymede
europa_fit = my_sine(q, *fit[0])

fit[0][0] *= 2  # double the freq of europa
fit[0][1] *= europa_orbit_ratio  # smaller than europa
fit[0][2] += 3.14159  # 180 degrees out of phase from europa
io_fit = my_sine(q, *fit[0])

plt.plot(days, ganymede, 'o', color = 'b')
plt.plot(days, europa, 'o', color = 'g')
plt.plot(days, io, 'o', color = 'r')
plt.plot(q, ganymede_fit, label=ganymede_msg, color = 'b')
plt.plot(q, europa_fit, label=europa_msg, color = 'g')
plt.plot(q, io_fit, label=io_msg, color = 'r')
plt.xlabel('Days since intital observation')
plt.ylabel('Distance from Jupiter (arc-seconds)')
plt.title('Orbits of Jupiter\'s Moons')
plt.legend()
plt.show()
