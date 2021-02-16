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

from cmath import phase
from math import pi

z1 = (50 + 10j)
z2 = (75 - 50j)

z_parallel = (z1 * z2)/(z1 + z2)
print(f'parallel impedance: {z_parallel}')
print(f'real: {z_parallel.real}')
print(f'imaginary:  {z_parallel.imag}')
print(f'phase: {phase(z_parallel)*180/pi} degrees')


print('')
print('pau, 終, done.')
