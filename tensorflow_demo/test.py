# -*- coding: UTF-8 -*-
# filename: test date: 2018/11/4 11:01  
# author: FD 
import tensorflow as tf
import numpy as np

with tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))) as sess:
    print(sess.run(tf.random_uniform(
        (1,2), dtype=tf.float32)))
