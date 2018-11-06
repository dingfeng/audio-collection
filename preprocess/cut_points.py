# -*- coding: UTF-8 -*-
# filename: sut date: 2018/11/6 15:33  
# author: FD 

import os
from common.common import *
import matplotlib.pyplot as plt


def main():
    source_dirs = ['semi_key_record_1', 'semi_key_record_1_test']
    for source_dir in source_dirs:
        cut_dir(source_dir)


def cut_dir(source_dir):
    dest_dir = source_dir + '_cut'
    create_if_no(dest_dir)
    for label_name in os.listdir(source_dir):
        str = input('begin to cut label name {} y or '' : '.format(label_name))
        if str == 'y' or str == '':
            label_dir_path = os.path.join(source_dir, label_name)
            dest_label_dir_path = os.path.join(dest_dir, label_name)
            create_if_no(dest_label_dir_path)
            for filename in os.listdir(label_dir_path):
                filepath = os.path.join(label_dir_path, filename)
                while True:
                    str = input('begin to cut label name {} filename {} y or '' : '.format(label_name, filename))
                    if str == 'y' or str == '':
                        points = begin_cut_file(filepath)
                        print('file is cut points = {}'.format(points))
                        point_record_file_path = os.path.join(dest_label_dir_path, filename + "_points.txt")
                        write_content_to_file(points.__str__(), point_record_file_path)
                    else:
                        print('label name {} filename {} is cut'.format(label_name, filename))
                        break
        else:
            print('to next label name')


def begin_cut_file(filepath):
    data, fs = read_sound_file(filepath)
    # only show the first channel
    y = data[:, 0]
    fig=plt.figure('cut data filepath = {}'.format(filepath))
    plt.scatter(list(range(len(y))), y)
    points = plt.ginput(5, timeout=-1)
    plt.close(fig)
    return points


if __name__ == '__main__':
    main()