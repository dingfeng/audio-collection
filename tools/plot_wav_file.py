# -*- coding: UTF-8 -*-
# filename: plot_wav_file date: 2018/10/19 12:33
# author: FD

import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import math

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f', '--filename', default="default_model/1.wav", help='audio file to be played back')
# parser.add_argument('-f','--filename',  default="ultrasonic.wav", help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
args = parser.parse_args()

try:
    import soundfile as sf

    data, fs = sf.read(args.filename, dtype='float32')
    # data=data.reshape((len(data),1))
    # shape = data.shape
    # plt.figure()
    # plt.title('acoustic line')
    # plt.plot(1/44100*np.arange(len(data[:,0])),data[:,0]-data[:,1],label='channel 1')
    # plt.legend()
    # plt.show()
    # start=int(input('input start index:'))
    # end=int(input("input end index:"))
    # data[start:end,:]
    # x = data[fs * 4:6 * fs]
    x=data[:,0]
    f, t, Zxx = signal.stft(x, fs, nperseg=1600,noverlap=800)
    vmax = np.max(x)
    mm = np.abs(Zxx)
    # print(Zxx.shape)
    # for i in range(Zxx.shape[0]):
    #     phase_line = []
    #     freq= i / 2000  *fs
    #     print(freq)
    #     # if freq > 120:
    #     #     break
    #     # if freq > 30:
    #     for j in range(Zxx.shape[1]):
    #         value=Zxx[i,j]
    #         phase_line.append(np.arctan(value.real/value.imag))
    #     plt.figure()
    #     plt.plot(range(len(phase_line)),phase_line,'*',label='{}'.format(round(freq,2)))
    #     plt.legend()
    #     plt.show()


    plt.pcolormesh(t, f, mm, vmin=0, vmax=np.max(x))
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
