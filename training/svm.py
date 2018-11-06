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

keys = [chr(i) for i in range(97, 123)]

param_dir = 'svm_param'


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
    orders = list(range(len(tags)))
    np.random.shuffle(orders)
    tags = tags[orders]
    filenames = filenames[orders]
    mfcc_features = mfcc_features[orders]
    data_len = len(mfcc_features)
    train_end_len = int(data_len)
    test_data_len = train_end_len
    test_tags = tags
    test_filenames = filenames
    test_mfcc_features = mfcc_features

    return


def test_generate_point(key):
    global test_data_len
    global test_tags
    global test_mfcc_features
    global z
    while True:
        index = np.random.randint(test_data_len)
        tag = test_tags[index]
        mfcc_feature = test_mfcc_features[index]
        output = 0.0
        if tag == key:
            output = 1.0
        z = tag
        yield mfcc_feature.astype(np.float32), np.array(output).astype(np.float32)


def generate_point(key):
    global data_len
    global tags
    global mfcc_features
    while True:
        index = np.random.randint(data_len)
        tag = tags[index]
        mfcc_feature = mfcc_features[index]
        output = 0.0
        if tag == key:
            output = 1.0
        yield mfcc_feature.astype(np.float32), np.array(output).astype(np.float32)


def SVM():
    batchsize = 5000
    train_max_step_count = 100
    # 构建数据输入
    opts = []
    predictions = []
    for key in keys:
        gen = generate_point
        data = tf.data.Dataset.from_generator(gen, (tf.float32, tf.float32), args=(key))
        data = data.batch(batchsize).prefetch(1)
        data = data.make_one_shot_iterator()
        next_x, next_y = data.get_next()
        # 构建SVM
        w = tf.Variable(tf.random_uniform([1, 26]))
        b = tf.Variable(tf.random_uniform((1,)))
        logit = tf.tanh(tf.matmul(w, next_x, transpose_b=True) + b)
        prediction = tf.tanh(tf.matmul(w, next_x, transpose_b=True) + b)
        loss = tf.losses.hinge_loss(next_y, logit) + tf.norm(w, 2)
        opt = tf.train.RMSPropOptimizer(1e-2).minimize(loss)
        tf.add_to_collection(key, w)
        tf.add_to_collection(key, b)
        opts.append(opt)
        predictions.append(prediction)

    gpu_options = tf.GPUOptions(allow_growth=True)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        sess.run(tf.global_variables_initializer())
        for index, opt in enumerate(opts):
            key = keys[index]
            prediction = predictions[index]
            xs = []
            ys = []
            data_count = 0
            for item in test_generate_point(key):
                xs += [item[0]]
                ys += [item[1]]
                data_count += 1
                if (data_count >= 5000):
                    break
            xs = np.stack(xs, 0).astype(np.float32)
            for i in range(train_max_step_count):
                sess.run(opt)
                prd = sess.run(prediction, {next_x: xs})
                prd = np.squeeze(prd)
                true_count = 0
                true_true_count = 0
                total_true_count = 0.0001
                for p_index, p_item in enumerate(prd):
                    true_tag = ys[p_index]
                    if (true_tag >= 0.5 and p_item >= 0.5) or (true_tag < 0.5 and p_item < 0.5):
                        true_count += 1
                    if (true_tag >= 0.5 and p_item >= 0.5):
                        true_true_count += 1
                    if (true_tag >= 0.5):
                        total_true_count += 1
                predict_rate = true_count / batchsize
                tp = true_true_count / total_true_count
            print('key = {} predict_rate = {} tp {}'.format(key, predict_rate,tp))

        saver = tf.train.Saver()
        save_path = saver.save(sess, param_dir + '/svm_k.ckpt')
        print("save_path = {}".format(save_path))

        # with tf.Session() as sess:
        #     new_saver = tf.train.import_meta_graph(param_dir+'/svm_k.ckpt.meta')
        #     new_saver.restore(sess, tf.train.latest_checkpoint('./'+param_dir))
        #     v = tf.get_variable("w")
        #     print(v.name)
        #     print(v.eval())


if __name__ == '__main__':
    init()
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['PYDEVD_USE_FRAME_EVAL'] = 'NO'
    os.environ['PYTHONUNBUFFERED'] = '1'
    SVM()
