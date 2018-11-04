# -*- coding: UTF-8 -*-
# filename: svm_demo date: 2018/11/3 14:52  
# author: FD 
import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt


def generate_point():
    while True:
        input = (np.random.rand(2) - 0.5) * 100
        output = input[1] > input[0]
        yield input, output.astype(np.float32)


def SVM():
    batchsize = 100
    # 构建数据输入
    gen = generate_point
    data = tf.data.Dataset.from_generator(gen, (tf.float32, tf.float32))
    data = data.batch(batchsize).prefetch(2)
    data = data.make_one_shot_iterator()
    next_x, next_y = data.get_next()

    # 构建SVM
    w = tf.Variable(tf.random_uniform([1, 2]))
    b = tf.Variable(tf.random_uniform((1,)))
    logit = tf.matmul(w, next_x, transpose_b=True) + b
    logit = tf.tanh(logit)
    prediction = tf.tanh(tf.matmul(w, next_x, transpose_b=True) + b)
    loss = tf.losses.hinge_loss(next_y, logit) + tf.norm(w, 2)
    opt = tf.train.RMSPropOptimizer(1e-2).minimize(loss)

    xy = []
    for i in range(batchsize):
        xy += [next(gen())[0]]
    xy = np.stack(xy, 0)
    i = 0
    gpu_options = tf.GPUOptions(allow_growth=True)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        sess.run(tf.global_variables_initializer())
        while True:
            sess.run(opt)
            prd = sess.run(prediction, {next_x:xy})
            for p, l in zip(xy, np.squeeze(prd)):
                if l > 0:
                    plt.scatter(p[0], p[1], c='red')
                else:
                    plt.scatter(p[0], p[1], c='green')
            plt.show()
            i += 1


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['PYDEVD_USE_FRAME_EVAL']='NO'
    SVM()
