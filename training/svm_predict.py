# -*- coding: UTF-8 -*-
# filename: svm_predict date: 2018/11/4 22:19  
# author: FD 
import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt

keys = [chr(i) for i in range(97, 123)]
feature_dir = '../collect_data/features'
filename = 'dingfeng.npz'
tags = None  # data tag list
filenames = None  # filename list
mfcc_features = None  # data feature list
data_len = None


def init():
    global tags
    global filenames
    global mfcc_features
    global data_len
    filepath = os.path.join(feature_dir, filename)
    data = np.load(filepath)
    tags = data['tags']
    filenames = data['filenames']
    mfcc_features = data['mfcc_features'].astype(np.float32)
    data_len = len(mfcc_features)
    return


def SVM_Predict():
    with tf.Session() as sess:
        new_saver = tf.train.import_meta_graph('svm_param/svm_k.ckpt.meta')
        new_saver.restore(sess, tf.train.latest_checkpoint('./svm_param'))
        predictions = []
        mfcc_feature = mfcc_features[5]
        mfcc_feature = np.asarray(mfcc_feature).reshape((1,26))
        for key in keys:
            key_collection = tf.get_collection(key)
            w = key_collection[0]
            b = key_collection[1]
            # print('w {}'.format(w.eval()))
            # print('b {}'.format(b.eval()))
            next_x = mfcc_feature#tf.Variable(tf.zeros((1, 26)))
            prediction = tf.tanh(tf.matmul(w, next_x, transpose_b=True) + b)
            prd = sess.run(prediction)
            prd = np.squeeze(prd)
            print("key {} prd = {}".format(key, prd))
    return


if __name__ == '__main__':
    init()
    SVM_Predict()
