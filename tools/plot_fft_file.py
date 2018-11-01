# -*- coding: UTF-8 -*-
# filename: plot_fft_file date: 2018/10/31 13:01  
# author: FD 
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft,ifft

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f','--filename',  default="../tools/j_c/1.wav", help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()

try:
    import soundfile as sf
    data, fs = sf.read(args.filename, dtype='float32')
    shape = data.shape
    fs = 44100
    y1=data[:, 0]

    # plt.subplot(121)
    # plt.title('source acoustic line')
    # plt.plot(y, label='channel 1')
    # plt.legend()

    yf=fft(y1)
    xf = np.arange(len(y1))/len(y1)*44100

    min_freq=200
    start_index = int(min_freq /44100 * len(y1))
    max_freq=44100-min_freq
    end_index = int(max_freq /44100 * len(y1))
    # yf[:start_index] = 0
    yf[start_index:end_index]=0
    y1= np.abs(ifft(yf))
    data[:, 0]=y1

    y2 = data[:, 1]
    yf = fft(y2)
    xf = np.arange(len(y2)) / len(y2) * 44100
    min_freq = 200
    start_index = int(min_freq / 44100 * len(y2))
    max_freq = 44100 - min_freq
    end_index = int(max_freq / 44100 * len(y2))
    # yf[:start_index] = 0
    yf[start_index:end_index] = 0
    y2 = np.abs(ifft(yf))
    data[:, 1] = y2
    with sf.SoundFile('./smoothed3.wav', mode='x', samplerate=44100,
                      channels=2, subtype=args.subtype) as file:
        file.write(np.asarray([y1,y2]).T)
    # plt.figure()
    # plt.plot(xf[range(int(len(y)/2))], yf[range(int(len(y)/2))], 'g')
    # plt.title('FFT of Mixed wave(normalization)', fontsize=9, color='r')
    # plt.show()
    # plt.subplot(122)
    # plt.title('smoothed acoustic line')
    # plt.plot(y,label='channel 1')
    # plt.legend()
    # plt.show()


except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))