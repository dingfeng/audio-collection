# -*- coding: UTF-8 -*-
# filename: common date: 2018/11/6 15:20  
# author: FD 
import sounddevice as  sd
import soundfile as sf
import os

def read_sound_file(filepath):
    data, fs = sf.read(filepath, dtype='float32')
    return data, fs


def write_to_sound_file(filepath, data, fs):
    with sf.SoundFile(filepath, mode='x', samplerate=fs,
                      channels=data.shape[1]) as file:
        file.write(data)
        file.close()


def create_if_no(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def write_content_to_file(content,filepath):
    with open(filepath, "w") as fo:
        fo.write(content)

def read_content_from_file(filepath):
    with open(filepath,'r') as fo:
        return fo.read()