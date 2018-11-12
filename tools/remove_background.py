# -*- coding: UTF-8 -*-
# filename: remove_background date: 2018/11/8 13:31  
# author: FD 
from common.common import *
import scipy.fftpack as fftp
import numpy as np

data1, fs1 = read_sound_file('default_model/1.wav')
y1 = data1[:, 0]
data2, fs2 = read_sound_file('default_model/2.wav')
y2 = data2[:, 0]
min_len = min(len(y1), len(y2))
y1 = y1[:min_len]
y2 = y2[:min_len]
yf1 = fftp.fft(y1, len(y1))
yf2 = fftp.fft(y2, len(y2))
yf3 = (yf2 - yf1)
newY = fftp.ifft(yf3, len(yf3))
newY=newY.astype(np.float32)
newY=newY.reshape((len(newY),1))
write_to_sound_file('aa.wav',newY,fs1)
