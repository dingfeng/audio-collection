# -*- coding: UTF-8 -*-
# filename: cut_data date: 2018/11/6 18:37  
# author: FD 
from common.common import *
import os


def main():
    source_dirs = ['semi_key_record_1_test']
    for source_dir in source_dirs:
        cut_data_dir(source_dir)
    return


def cut_data_dir(source_dir):
    data_dir = source_dir + '_smoothed'
    cut_dir = source_dir + "_cut"
    for label_name in os.listdir(data_dir):
        label_dir_path = os.path.join(data_dir, label_name)
        cut_label_dir_path = os.path.join(cut_dir, label_name)
        for filename in os.listdir(label_dir_path):
            data_path = os.path.join(label_dir_path, filename)
            data, fs = read_sound_file(data_path)
            cut_file_name = filename + "_points.txt"
            cut_file_path = os.path.join(cut_label_dir_path, cut_file_name)
            points = eval(read_content_from_file(cut_file_path))
            data = data[int(points[0][0]):int(points[1][0]), :]
            dest_filepath = os.path.join(cut_label_dir_path, filename)
            write_to_sound_file(dest_filepath, data, fs)
    return


if __name__ == '__main__':
    main()
