# -*- coding: UTF-8 -*-
# filename: svm date: 2018/11/4 16:29  
# author: FD
import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt

feature_dir = '../collect_data/features'
filename = 'dingfeng.npz'
tags = None  # data tag list
filenames = None  # filename list
mfcc_features = None  # data feature list
data_len = None

test_tags = None
test_filenames = None
test_mfcc_features = None
test_data_len = None

key = 'j'


def init():
    global tags
    global filenames
    global mfcc_features
    global data_len
    global test_tags
    global test_filenames
    global test_mfcc_features
    global test_data_len
    filepath = os.path.join(feature_dir, filename)
    data = np.load(filepath)
    tags = data['tags']
    filenames = data['filenames']
    mfcc_features = data['mfcc_features']
    data_len = len(mfcc_features)
    train_end_len = int(data_len * 0.8)
    test_data_len = data_len - train_end_len
    test_tags = tags[train_end_len:]
    test_filenames = filenames[train_end_len:]
    test_mfcc_features = mfcc_features[train_end_len:]
    tags = tags[:train_end_len]
    filenames = filenames[:train_end_len]
    mfcc_features = mfcc_features[:train_end_len]
    data_len = train_end_len
    return


def test_generate_point():
    global test_data_len
    global test_tags
    global test_mfcc_features
    global key
    while True:
        index = np.random.randint(test_data_len)
        tag = test_tags[index]
        mfcc_feature = test_mfcc_features[index]
        output = 0.0
        if tag == key:
            output = 1.0
        yield mfcc_feature.astype(np.float32), np.array(output).astype(np.float32)


def generate_point():
    global data_len
    global tags
    global mfcc_features
    while True:
        index = np.random.randint(data_len)
        tag = tags[index]
        mfcc_feature = mfcc_features[index]
        output = 0.0
        if tag == 'b':
            output = 1.0
        yield mfcc_feature.astype(np.float32), np.array(output).astype(np.float32)


def SVM():
    global key
    batchsize = 100
    # 构建数据输入
    gen = generate_point
    data = tf.data.Dataset.from_generator(gen, (tf.float32, tf.float32))
    data = data.batch(batchsize).prefetch(2)
    data = data.make_one_shot_iterator()
    next_x, next_y = data.get_next()

    # 构建SVM
    w = tf.Variable(tf.random_uniform([1, 26]))
    b = tf.Variable(tf.random_uniform((1,)))
    logit = tf.matmul(w, next_x, transpose_b=True) + b
    logit = tf.tanh(logit)
    prediction = tf.tanh(tf.matmul(w, next_x, transpose_b=True) + b)
    loss = tf.losses.hinge_loss(next_y, logit) + tf.norm(w, 2)
    opt = tf.train.RMSPropOptimizer(1e-2).minimize(loss)

    xs = []
    ys = []
    data_count = 0
    for item in test_generate_point():
        xs += [item[0]]
        ys += [item[1]]
        data_count += 1
        if (data_count >= batchsize):
            break
    xs = np.stack(xs, 0).astype(np.float32)
    step_count = 0
    gpu_options = tf.GPUOptions(allow_growth=True)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        sess.run(tf.global_variables_initializer())
        while True:
            sess.run(opt)
            # random get 100 data
            prd = sess.run(prediction, {next_x: xs})
            prd = np.squeeze(prd)
            true_count = 0
            for p_index, p_item in enumerate(prd):
                true_tag = ys[p_index]
                if (true_tag == key and p_item >= 0.5) or (true_tag != key and p_item < 0.5):
                    true_count += 1
            step_count += 1
            predict_rate = true_count / batchsize
            print('step_count = {} predict_rate = {}'.format(step_count, predict_rate))


if __name__ == '__main__':
    init()
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['PYDEVD_USE_FRAME_EVAL'] = 'NO'
    os.environ['PYTHONUNBUFFERED'] = '1'
    SVM()
