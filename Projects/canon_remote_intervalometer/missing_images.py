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

from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = ArgumentParser(description = 'check a series of intervalometer photos to look for missing images.')
    parser.add_argument('--dir', default='~/Desktop/stellar_time_lapse_220101/images', help='Directory containing jpg images')
    args = parser.parse_args()


    import os
    from pathlib import Path

    dir = '~/Desktop/stellar_time_lapse_220103/images'
    
    files = Path(args.dir).iterdir()

    paths = sorted(Path(args.dir).iterdir(), key=os.path.getmtime)

    tl_images = []

    for fn in Path(args.dir).iterdir():
        print(fn)
        print(fn.name)
        print(os.path.getmtime(fn))
        tl_images.append([fn.name, os.path.getmtime(fn)]) 
        tl_images.sort()   

    # tl_images.remove[-1]  # hack to remove kdenlive file
    tl_deltas = []
    oldtime = 0
    for image in tl_images:
        if oldtime:

            currtime = image[1]
            print(currtime)
            tl_deltas.append([image[0], currtime - oldtime])
            oldtime = currtime
        else:
            tl_deltas.append([image[0], 0])
            oldtime = image[1]

    deltas_by_time = np.array(tl_deltas)
    deltas = np.transpose(deltas_by_time)
    print(deltas[1])
    # plt.imshow(deltas[1])
    # plt.show
    y_str = np.array(deltas[1])
    y_vals = y_str.astype(np.float64)


    x_vals = np.arange(len(deltas[1]))
    # plt.xkcd()
    plt.ylim(0,240)
    plt.yticks([0, 60, 120, 180, 240])
    plt.plot(x_vals, y_vals, 'x') 
    # plt.plot(ref_vals, y_vals, 'or') 
    plt.show()

    # fig, ax = plt.subplots()
    # ax.plot(x_vals, y_vals, 'b-')
    # ax.set_yscale(ax.scale)
    # ax.show()


    plt.plot(deltas[1])
    plt.show()
    print('pau')

