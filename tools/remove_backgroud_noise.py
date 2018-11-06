# -*- coding: UTF-8 -*-
# filename: remove_backgroud_noise date: 2018/11/5 20:10  
# author: FD
import numpy as np
import soundfile as sf

data1, fs1 = sf.read('default_model/1.wav', dtype='float32')
data2, fs2 = sf.read('default_model/2.wav', dtype='float32')

minLen=min(len(data2[:,0]),len(data1[:,0]))
X1=np.fft.fft(data1[:minLen,0])
X2=np.fft.fft(data2[:minLen,0])
X3=X2-X1
data3=np.abs(np.fft.ifft(X3))
with sf.SoundFile('true.wav', mode='x', samplerate=44100,
                  channels=1) as file:
    file.write(np.asarray(data3))