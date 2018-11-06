# -*- coding: UTF-8 -*-
# filename: plot_wav_file date: 2018/10/19 12:33
# author: FD

import argparse
import matplotlib.pyplot as plt
import numpy as np

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f','--filename',  default="./sdfsdf3.wav", help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
args = parser.parse_args()

try:
    import soundfile as sf
    data, fs = sf.read(args.filename, dtype='float32')
    shape = data.shape
    plt.figure()
    plt.title('acoustic line')
    plt.plot(1/44100*np.arange(len(data[:,0])),data[:,0],label='channel 1')
    plt.legend()
    plt.show()
    start=int(input('input start index:'))
    end=int(input("input end index:"))
    data[start:end,:]

except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))