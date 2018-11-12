# -*- coding: UTF-8 -*-
# filename: averaging_smooth date: 2018/11/7 12:43  
# author: FD 
from common.common import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fftp
def smooth(y1):
    yf = fftp.fft(y1, len(y1))
    xf = np.arange(len(y1)) / len(y1) * 44100
    freq_to_index_f = lambda x: int(x * len(y1) / 44100)
    remove_min_freq = 100
    remove_max_freq = 150
    yf[freq_to_index_f(remove_min_freq):freq_to_index_f(remove_max_freq)] = 0
    yf[freq_to_index_f(44100 - remove_max_freq):freq_to_index_f(44100 - remove_min_freq)] = 0
    newY = fftp.ifft(yf, len(y1))
    newY=newY.astype(np.float32)
    return newY

def average_moving(y):
    win_size = 500
    for i in range(len(y) - win_size + 1):
        y[i] = np.mean(y[i:i + win_size])
    return y


filepath = 'default_model/1.wav'

# for i in range(2):
data, fs = read_sound_file(filepath = 'default_model/2.wav')
# plt.subplot(10,1,i+1)
plt.plot(smooth(data[:,0]))


# for i in range(10):
#     data, fs = read_sound_file(filepath.format('i',i+1))
#     plt.subplot(10,2,10+i+1)
#     plt.plot(average_moving(data[:,0]))

plt.show()