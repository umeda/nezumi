# fun with mumpy
import numpy as np
from pprint import pprint
arr = np.full((20), 0.0)
pprint(arr)
for i in range(1,21):
    arr[0] = i
    arr = np.roll(arr,-1)
    pprint(arr)
