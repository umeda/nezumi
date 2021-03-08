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
    
    def __init__(self, example_param=1.0):  # only default arguments here
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
        self.example_param = example_param

    def work(self, input_items, output_items):
        print('Input Items[0]: ' + str(input_items[0]))
        # print('Input Items[1]: ' + str(input_items[1]))
        print('max           : ' + str(np.argmax(input_items[0])))
        print('min           : ' + str(np.argmin(input_items[0])))
        print(str(type(input_items[0])))
        # self.total_samples += len(input_items[0])
        self.total_samples += 1
        print('current samples: ' + str(len(input_items[0])))
        print('total samples  : ' + str(self.total_samples))
        #output_items[0][:] = input_items[0] * self.example_param
        output_items[0][:] = self.total_samples
        return len(output_items[0])
