"""
This script calculates time RC time constnats.

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

from math import e
from engineering_notation import EngNumber

resistance = 10e3
capacitance = 0.01e-6
initial_voltage = 1
tau = resistance * capacitance

print('')
print(f'Resistance  = {EngNumber(resistance)}\u03A9')
print(f'Capacitance = {EngNumber(capacitance)}F')
print(f'Tau (RC)    = {EngNumber(tau)}S')
print(f'Initial voltage = {initial_voltage}V')
print('')

print('Capacitor Dischage')
print('TC\ttime\tvoltage')
for t in range(0, 6):
    voltage = e ** (-(t * tau)/tau)
    print(f'{t}\t{str(EngNumber(t * tau))}S\t{str(EngNumber(voltage, precision=1))}V')

print('')
print('pau, 終, done.')
