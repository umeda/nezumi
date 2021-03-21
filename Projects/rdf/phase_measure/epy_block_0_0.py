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
    curr_sig_samples = np.array([])
    curr_ref_samples = np.array([])


    def __init__(self, samp_rate=1.0, freq=500):  # only default arguments here
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
        self.freq = freq

    def work(self, input_items, output_items):
        print('sample rate = ' + str(self.samp_rate))
        print('freq        = ' + str(self.freq))
        print('Input Items[0]: ' + str(input_items[0]))
        print('Input Items[1]: ' + str(input_items[1]))

        # input as a tuple???
        print(str(type(self.curr_sig_samples)))
        print(str(type(input_items[0])))
        self.curr_sig_samples = np.concatenate((self.curr_sig_samples, input_items[0]))
        self.curr_sig_samples = np.concatenate((self.curr_ref_samples, input_items[1]))

        print('number of inputs: ' + str(len(input_items[0])))
        print('number of samples: ' + str(len(self.curr_sig_samples)))
        print(str(self.curr_sig_samples))
        # todo: check logic
        if len(self.curr_sig_samples) >=  self.samp_rate/self.freq:
            max = [0,0]
            min = [0,0]
            max[0] = np.argmax(self.curr_sig_samples)
            max[1] = np.argmax(self.curr_ref_samples)
            min[0] = np.argmin(self.curr_sig_samples)
            min[1] = np.argmin(self.curr_ref_samples)
                # check for length
                # try putting a delay here...
            if max[0] and max[1]: 
                angle = (max[0] - max[1]) * 180 / 10
                print('MAX ' + str(max[0]) + ' ' + str(max[1]) + ' ' + str(angle))
                output_items[0][:] = np.array([angle])
                print(output_items[0][:])
            elif min[0] and min[1]: 
                angle = (min[0] - min[1]) * 180 / 10
                print('MIN ' + str(min[0]) + ' ' + str(min[1]) + ' ' + str(angle))
                output_items[0][:] = np.array([angle])
                print(output_items[0][:])
            else:
                # needs xor
                print('needs more work')
            self.curr_sig_samples = np.array([])
            self.curr_ref_samples = np.array([])
        else:
            print('too short')
            return 0


        # print(str(type(input_items[0])))
        # self.total_samples += len(input_items[0])
        # self.total_samples += 1
        # print('current samples: ' + str(len(input_items[0])))
        # print('total samples  : ' + str(self.total_samples))
        #output_items[0][:] = input_items[0] * self.example_param
        # output_items[0][:] = self.total_samples
        return len(output_items[0])
