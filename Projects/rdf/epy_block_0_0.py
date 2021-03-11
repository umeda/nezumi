"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    total_samples = 0
    
    def __init__(self, samp_rate=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Phase Measurement',   # will show up in GRC
            in_sig=[np.uint8, np.uint8],
            out_sig=[np.float32]
        )
        # np types int32  
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.samp_rate = samp_rate

    def work(self, input_items, output_items):
        print('Input Items[0]: ' + str(input_items[0]))
        print('Input Items[1]: ' + str(input_items[1]))
        max = [0,0]
        min = [0,0]
        max[0] = np.argmax(input_items[0])
        max[1] = np.argmax(input_items[1])
        min[0] = np.argmin(input_items[0])
        min[1] = np.argmin(input_items[1])
            # check for length
            # try putting a delay here...
        if max[0] and max[1]: 
            angle = (max[0] - max[1]) * 180 / 10
            print('MAX ' + str(max[0]) + ' ' + str(max[1]) + ' ' + str(angle))
            output_items[0][:] = angle
            print(output_items[0][:])
        elif min[0] and min[1]: 
            angle = (min[0] - min[1]) * 180 / 10
            print('MIN ' + str(min[0]) + ' ' + str(min[1]) + ' ' + str(angle))
            output_items[0][:] = angle
            print(output_items[0][:])
        else:
            # needs xor
            print('needs more work')

        # print(str(type(input_items[0])))
        # self.total_samples += len(input_items[0])
        # self.total_samples += 1
        # print('current samples: ' + str(len(input_items[0])))
        # print('total samples  : ' + str(self.total_samples))
        #output_items[0][:] = input_items[0] * self.example_param
        # output_items[0][:] = self.total_samples
        return len(output_items[0])
