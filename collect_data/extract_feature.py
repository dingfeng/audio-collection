# -*- coding: UTF-8 -*-
# filename: extract_feature date: 2018/11/4 15:55  
# author: FD 
from python_speech_features import mfcc
import soundfile as sf
import os
import numpy as np


def get_feature(dir, filename):
    filepath = os.path.join(dir, filename)
    data, fs = sf.read(filepath, dtype='float32')
    mfcc_feature = mfcc(data, samplerate=fs, winlen=0.002, winstep=0.001)
    filename = filename[0:-4]
    tag = filename[0:filename.index('_')]
    return (tag, filename, mfcc_feature)


if __name__ == '__main__':
    root_dir = 'label_data_dingfeng_test'
    dir_filenames = os.listdir(root_dir)
    tags = []
    filenames = []
    mfcc_features = []
    for index, item in enumerate(dir_filenames):
        print('index {} '.format(index))
        tag, filename, mfcc_feature = get_feature(root_dir, item)
        tags.append(tag)
        filenames.append(filename)
        mfcc_features.append(mfcc_feature)

    feature_dir = 'features'
    feature_file = os.path.join(feature_dir, '1.npz')
    np.savez(feature_file, tags=np.asarray(tags), filenames=np.asarray(filenames),
             mfcc_features=np.asarray(mfcc_features))
