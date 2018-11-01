# -*- coding: UTF-8 -*-
# filename: file_mfcc date: 2018/11/1 10:31  
# author: FD
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import soundfile as sf
import matplotlib.pyplot as plt
data, fs = sf.read('./cut/j_c_smoothed/1.wav', dtype='float32')
plt.subplot(221)
plt.plot(data)
plt.title('./cut/j_c_smoothed/1.wav')
mfcc_feat = mfcc(data,samplerate=fs,winlen=0.005,winstep=0.002)
plt.subplot(222)
plt.plot(mfcc_feat)
plt.title('./cut/j_c_smoothed/1.wav')

data, fs = sf.read('./cut/j_u_smoothed/1.wav', dtype='float32')
plt.subplot(223)
plt.plot(data)
plt.title('./cut/j_u_smoothed/1.wav')
mfcc_feat = mfcc(data,samplerate=fs,winlen=0.005,winstep=0.002)
plt.subplot(224)
plt.plot(mfcc_feat)
plt.title('./cut/j_u_smoothed/1.wav')

plt.show()