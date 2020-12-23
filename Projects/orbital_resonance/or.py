

import numpy as np
from scipy.optimize import curve_fit
import pylab as plt
from pprint import pprint
days = np.array([0, 2, 4, 6, 8, 26])
ganymede = np.array([148.6, 164.0, -210.6, -92.0, 237.4, -232.5])
europa = np.array([])
io = np.array([])

q = np.arange(0,29,0.1)

# N = 1000 # number of data points
# t = np.linspace(0, 4*np.pi, N)
# data = 3.0*np.sin(t+0.001) + 0.5 + np.random.randn(N) # create artificial data with noise

N = 6 # number of data points
t = days
data = ganymede

guess_freq = 1
guess_amplitude = 3*np.std(data)/(2**0.5)
guess_phase = 0
# guess_offset = np.mean(data)
guess_offset = 0

p0=[guess_freq, guess_amplitude,
    guess_phase, guess_offset]

# create the function we want to fit
def my_sin(x, freq, amplitude, phase, offset):
    return np.sin(x * freq + phase) * amplitude + offset

# now do the fit
fit = curve_fit(my_sin, t, data, p0=p0)

# we'll use this to plot our first estimate. This might already be good enough for you
data_first_guess = my_sin(q, *p0)

# recreate the fitted curve using the optimized parameters
pprint(fit[0])
pprint(fit[1])
msg = 'Ganymede orbit ' + str(2 * 3.14159 / fit[0][0]) + ' days'
data_fit = my_sin(q, *fit[0])
plt.plot(t, data, 'o')
plt.plot(q, data_fit, label=msg)
# plt.plot(q, data_first_guess, label='first guess')
plt.legend()
plt.show()
