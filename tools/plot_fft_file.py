# -*- coding: UTF-8 -*-
# filename: plot_fft_file date: 2018/10/31 13:01  
# author: FD 
import argparse
import scipy.fftpack as fftp
import numpy as np
import matplotlib.pyplot as plt


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f', '--filename', default="G:/2018-11-10_14-00.wav", help='audio file to be played back')
# parser.add_argument('-f', '--filename', default="../sound_wave/ultrasonic.wav",
#                     help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()


def smooth(y1):
    yf = fftp.fft(y1, len(y1))
    xf = np.arange(len(y1)) / len(y1) * 44100
    freq_to_index_f = lambda x: int(x * len(y1) / 44100)
    remove_min_freq = 68
    remove_max_freq = 87
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 119
    remove_max_freq = 121
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 96
    remove_max_freq = 102
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 48
    remove_max_freq = 50
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 54
    remove_max_freq = 56
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 43
    remove_max_freq = 45
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 171
    remove_max_freq = 173
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    # remove_min_freq = 601
    # remove_max_freq = 603
    # yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    # yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    # remove_min_freq = 192
    # remove_max_freq = 195
    # yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    # yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    # remove_min_freq = 126
    # remove_max_freq = 127.5
    # yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    # yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    # remove_min_freq = 126
    # remove_max_freq = 127.5
    # yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    # yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    # remove_min_freq = 540
    # remove_max_freq = 560
    # yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    # yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    # remove_min_freq = 526
    # remove_max_freq = 527.5
    # yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    # yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    # remove_min_freq = 562
    # remove_max_freq = 564
    # yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    # yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 300
    remove_max_freq = 20000
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    remove_min_freq = 150
    remove_max_freq = 151
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    newY = fftp.ifft(yf, len(y1))
    return newY


try:
    import soundfile as sf
    from common.common import *

    data, fs = sf.read(args.filename, dtype='float32')
    shape = data.shape
    y1 = data#[:,0]  # [:, 0]

    # y1 = smooth(y1).astype(np.float32)
    # y2 = data[:, 1]
    # y2 = smooth(y2).astype(np.float32)
    xf = np.arange(len(y1)) / len(y1) * fs
    yf = fftp.fft(y1, len(y1))
    yf=np.abs(yf)
    for i in range(20):
        yf[np.argmax(yf)]=0
    plt.plot(xf, yf)
    # plt.show()
    # with sf.SoundFile('sdfsdf3.wav', mode='x', samplerate=44100,
    #                   channels=2, subtype=args.subtype) as file:
    #     file.write(np.asarray([y1, y2]).T)
    #     file.close()
    # plt.figure()

    # yf[:] = 0
    # yf[20100] = 40000
    # newY = fftp.ifft(yf, len(y1)).astype(np.float32)
    # newY = newY.astype(np.float32).tolist()
    # resultY = []
    # for i in range(60):
    #     resultY += newY
    # resultY = np.asarray(resultY).reshape((len(resultY), 1))
    # newY=newY.reshape((len(newY),1))
    # write_to_sound_file('ultrasonic1.wav', resultY, fs)
    # newY.astype(np.float32)
    # plt.plot(xf, newY, xf, y1 + 0.05)

    # yf = fftp.fft(newY, len(newY))
    # plt.plot(xf, yf)
    plt.show()


except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
