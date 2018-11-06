# -*- coding: UTF-8 -*-
# filename: extract_feature date: 2018/11/6 18:54  
# author: FD 
import numpy as np
from common.common import *
from python_speech_features import mfcc


def main():
    dirs = ['semi_key_record_1', 'semi_key_record_1_test']
    for dir in dirs:
        extract_feature_dir(dir)


def extract_feature_dir(dir):
    dest_dir = ''.join([dir, '_feature'])
    create_if_no(dest_dir)
    source_dir = ''.join([dir, '_cut'])
    for label_name in os.listdir(source_dir):
        source_label_path = os.path.join(source_dir, label_name)
        dest_label_path = os.path.join(dest_dir, label_name)
        create_if_no(dest_label_path)
        for label_filename in os.listdir(source_label_path):
            if label_filename.endswith('wav'):
                source_filepath = os.path.join(source_label_path, label_filename)
                data, fs = read_sound_file(source_filepath)
                mfcc_data = get_mfcc_data(data, fs)
                dest_file_path = os.path.join(dest_label_path, ''.join([label_filename, '.npz']))
                np.savez(dest_file_path, mfcc_data=mfcc_data)


def get_mfcc_data(data, fs):
    new_data = []
    for i in range(data.shape[1]):
        one_channel_mfcc = mfcc(data[:, i], samplerate=fs, winlen=0.010, winstep=0.005, highfreq=200)
        one_channel_mfcc = normalize(one_channel_mfcc)
        new_data += [one_channel_mfcc]
    new_data = np.asarray(new_data).transpose(1, 2, 0)
    return new_data


def normalize(data):
    size = 98
    x = np.arange(size)
    new_data = []
    for i in range(data.shape[1]):
        y = data[:, i]
        y_len = len(y)
        y = np.interp(x * y_len / size, np.arange(y_len), y)
        y = np.interp(y, (y.min(), y.max()), (-1, +1))
        new_data += [y]
    new_data = np.asarray(new_data).transpose()
    return new_data


if __name__ == '__main__':
    main()
    # a = np.array([1, 2, -1])
    # b = np.interp(a, (a.min(), a.max()), (-1, +1))
    # print(b)
    # data=np.vstack([np.arange(40) for _ in range(26)])
    # data=data.transpose().reshape((40,2,13)).transpose((2,0,1))
    # print(data.shape)
    # mfcc_data_lens = [91, 88, 111, 93, 90, 101, 99, 100, 102, 97, 108, 84, 92, 98, 99, 88, 104, 103, 96, 108, 100, 96,
    #                   102, 101, 109, 107, 104, 138, 120, 105, 99, 104, 102, 104, 98, 87, 95, 106, 111, 103, 102, 86, 93,
    #                   101, 93, 99, 87, 104, 108, 98, 82, 82, 75, 67, 63, 81, 106, 68, 77, 81, 90, 92, 92, 96, 105, 100,
    #                   98, 102, 120, 102] + [81, 88, 80, 82, 130, 99, 84, 93, 91, 90, 72, 89, 74, 89, 77, 79, 81, 85, 95,
    #                                         104, 100, 103, 102, 102, 101, 107,
    #                                         131, 100, 102, 100, 97, 100, 98, 98, 88, 98, 94, 112, 105, 107, 95, 99, 96,
    #                                         82, 97, 101, 99, 98, 102, 101, 76, 115,
    #                                         99, 112, 104, 93, 105, 110, 102, 98, 108, 106, 110, 104, 104, 100, 104, 94,
    #                                         110, 127]
    # print(np.mean(mfcc_data_lens))
