"""Create plots of signals generated by chirp() and sweep_poly()."""
from scipy.signal import butter, lfilter

import soundfile as sf
import numpy as np


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


data, fs = sf.read('../collect_data/data/j.wav', dtype='float32')

y1 = butter_bandpass_filter(data[:, 0], 2000, 5000, fs)
y2 = butter_bandpass_filter(data[:, 1], 2000, 5000, fs)
with sf.SoundFile('aabbbb.wav', mode='x', samplerate=44100,
                  channels=2) as file:
    file.write(np.asarray([y1, y2]).T)