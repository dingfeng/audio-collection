# -*- coding: UTF-8 -*-
# filename: smooth date: 2018/11/6 15:03  
# author: FD 

import scipy.fftpack as fftp
import numpy as np
import sounddevice as sd
import soundfile as sf
import os
from common.common import *


def main():
    print("hello world!")
    source_dirs = ['semi_key_record_1', 'semi_key_record_1_test']
    for source_dir in source_dirs:
        smooth_dir(source_dir)


def smooth_dir(source_dir):
    dest_dir =  source_dir+"_smoothed"
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
    for dir_name in os.listdir(source_dir):
        source_dir_path = os.path.join(source_dir, dir_name)
        dest_dir_path = os.path.join(dest_dir, dir_name)
        if not os.path.isdir(dest_dir_path):
            os.mkdir(dest_dir_path)
        for filename in os.listdir(source_dir_path):
            source_filepath = os.path.join(source_dir_path, filename)
            dest_filepath = os.path.join(dest_dir_path, filename)
            # read sound file in the source filepath
            smooth(source_filepath, dest_filepath)


def smooth(source, dest):
    data, fs = read_sound_file(source)
    y1 = data[:, 0]
    y1 = smooth_data(y1).astype(np.float32)
    y2 = data[:, 1]
    y2 = smooth_data(y2).astype(np.float32)
    data = np.asarray([y1, y2]).T
    write_to_sound_file(dest, data, fs)


def smooth_data(y1):
    yf = fftp.fft(y1, len(y1))
    # xf = np.arange(len(y1)) / len(y1) * 44100
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


if __name__ == '__main__':
    main()
