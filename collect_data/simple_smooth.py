# -*- coding: UTF-8 -*-
# filename: simple_smooth date: 2018/11/5 19:01  
# author: FD 
from scipy.signal import butter, lfilter
import soundfile as sf
import numpy as np
import os


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


def smooth(source, dest):
    data, fs = sf.read(source, dtype='float32')
    y1 = butter_bandpass_filter(data[:, 0], 2000, 3000, fs)
    y2 = butter_bandpass_filter(data[:, 1], 2000, 3000, fs)
    with sf.SoundFile(dest, mode='x', samplerate=44100,
                      channels=2) as file:
        file.write(np.asarray([y1, y2]).T)


if __name__ == '__main__':
    dir='data'
    file_list = os.listdir(dir)
    for file in file_list:
        if not file.endswith('.wav'):
            continue
        filename=file[:-4]
        source=os.path.join(dir,file)
        dest=os.path.join(dir,filename+"_smoothed.wav")
        smooth(source,dest)