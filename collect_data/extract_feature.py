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
    T=1.0/fs
    mfcc_feature_0 = mfcc(data[:,0], samplerate=fs, winlen=len(data)*T, winstep=len(data)*T,nfft=len(data))
    mfcc_feature_1 = mfcc(data[:,1], samplerate=fs, winlen=len(data)*T, winstep=len(data)*T,nfft=len(data))
    mfcc_feature=np.hstack((np.squeeze(mfcc_feature_0,0),np.squeeze(mfcc_feature_1,0)))
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
    feature_file = os.path.join(feature_dir, 'dingfeng.npz')
    np.savez(feature_file, tags=np.asarray(tags), filenames=np.asarray(filenames),
             mfcc_features=np.asarray(mfcc_features))
