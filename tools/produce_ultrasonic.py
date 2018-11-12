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
# parser.add_argument('-f', '--filename', default="./default_model/1.wav", help='audio file to be played back')
parser.add_argument('-f', '--filename', default="../sound_wave/ultrasonic.wav",
                    help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()


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
    plt.plot(xf, yf)
    # plt.show()
    # with sf.SoundFile('sdfsdf3.wav', mode='x', samplerate=44100,
    #                   channels=2, subtype=args.subtype) as file:
    #     file.write(np.asarray([y1, y2]).T)
    #     file.close()
    # plt.figure()

    yf[:] = 0
    yf[20200] = 41000
    newY = fftp.ifft(yf, len(y1)).astype(np.float32)
    newY = newY.astype(np.float32).tolist()
    resultY = []
    for i in range(60):
        resultY += newY
    resultY = np.asarray(resultY).reshape((len(resultY), 1))
    # newY=newY.reshape((len(newY),1))
    write_to_sound_file('ultrasonic2.wav', resultY, fs)
    # newY.astype(np.float32)
    # plt.plot(xf, newY, xf, y1 + 0.05)

    yf = fftp.fft(newY, len(newY))
    plt.plot(xf, yf)
    plt.show()


except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
