"""
This script calculates 5% resistor values for a voltage divider.

vin ------+
          |
          r1
          |
          +----- vout
          |
          r2
          |
gnd ------+

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
from math import log10
from engineering_notation import EngNumber

five_pct_vals = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]

vin = float(input("Enter input voltage: "))
vout = float(input("Enter output voltage: "))
iin = float(input("Enter current in mA: "))
print('')
rtotal = vin / iin * 1000

r2raw = rtotal * (vout / vin)
r1raw = rtotal - r2raw

r1pwr = log10(r1raw)
r2pwr = log10(r2raw)

r1digits = str(r1raw)[0:2]
r2digits = str(r2raw)[0:2]

r1select = {'val': 0,
            'error': 999,
            'pwr': log10(r1raw),
            'raw': r1raw,
            'digits': str(r1raw)[0:2]}
r2select = {'val': 0,
            'error': 999,
            'pwr': log10(r2raw),
            'raw': r2raw,
            'digits': str(r2raw)[0:2]}

for five_pct_val in five_pct_vals:
    err = abs((int(r1select['digits'])-five_pct_val)/int(r1select['digits']))
    if err < r1select['error']:
        r1select['val'] = five_pct_val
        r1select['error'] = err
    err = abs((int(r2select['digits'])-five_pct_val)/int(r2select['digits']))
    if err < r2select['error']:
        r2select['val'] = five_pct_val
        r2select['error'] = err

r1val = float(r1select['digits']) * 10 ** int((r1select['pwr']-1))
r2val = float(r2select['digits']) * 10 ** int((r2select['pwr']-1))

r1str = str(EngNumber(r1val)) + '\u03A9'
r2str = str(EngNumber(r2val)) + '\u03A9'
print('r1 value => ' + r1str)
print('r2 value => ' + r2str)
print('voltage  => {:.1f} volts'.format(vin * r2val / (r1val + r2val)))
print('current  => {:.1f} milliamps'.format(vin / (r1val + r2val) * 1000))
imp = str(EngNumber(1/((1 / r2val) + (1 / r2val)))) + '\u03A9'
print('r source => ' + imp)
print('r1 power => {:.1f} milliwatts'.format(1000 * r1val * (vin / (r1val + r2val)) ** 2))
print('r2 power => {:.1f} milliwatts'.format(1000 * r2val * (vin / (r1val + r2val)) ** 2))
print('')
print('pau, 終, done.')
