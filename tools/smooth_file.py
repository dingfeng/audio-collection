# -*- coding: UTF-8 -*-
# filename: smooth_file date: 2018/11/5 16:52  
# author: FD 
import numpy as np
from scipy.signal.waveforms import chirp, sweep_poly
import matplotlib.pyplot as plt
import soundfile as sf

import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import soundfile as sf
data, fs = sf.read('smoothed_high2.wav', dtype='float32')

plt.specgram(data[:,0],NFFT=500,Fs=fs,noverlap=400)
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.show()