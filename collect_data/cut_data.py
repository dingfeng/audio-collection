# -*- coding: UTF-8 -*-
# filename: cut_data date: 2018/11/2 10:06  
# author: FD 
import numpy as np
import os
import soundfile as sf
import matplotlib.pyplot as plt
import tempfile
import sys
import threading


def plot_vertical_line(x):
    plt.plot([x, x], [-1, 1], color='r')


def get_data_points_by_time(time, fs):
    return int(time * fs)


# read log file
dir = 'data'
prefix='a'
label_data_dir = 'label_data_accurate_tagged'
if (not os.path.isdir(label_data_dir)):
    os.mkdir(label_data_dir)
logfile = os.path.join(dir, prefix+'.txt')
log = np.genfromtxt(logfile, dtype=[('col1', 'S120'), ('col2', float), ('col3', 'S120')])
start_time = None
press_times = []
release_times = []
keys = []
for tuple in log:
    if (tuple[0] == b'start'):
        start_time = float(tuple[1])
    elif (tuple[0] == b'press'):
        press_times.append(float(tuple[1]))
        keys.append(str(tuple[2])[3:-2])
    elif (tuple[0] == b'release'):
        release_times.append(float(tuple[1]))

# read wav file
datafile = os.path.join(dir, prefix+'.wav')
data, fs = sf.read(datafile, dtype='float32')
downsample = 10
sound_start = 0
time_len = 60  # second
data_start_index = sound_start * 44100
data_end_index = (sound_start + time_len) * 44100
one_channel_data = data[data_start_index:data_end_index, 0][::downsample]
T = 1 / fs * downsample
x = np.arange(len(one_channel_data)) * T + sound_start
press_times = np.asarray(press_times)
fixed_offset = 0
start_offset = 0
try:
    while True:
        plt.title('data wave line figure')
        plt.plot(x, one_channel_data, label='channel 1')
        ginputs = plt.ginput(5)
        if (len(ginputs) > 0):
            start_offset = ginputs[0][0]
        press_times_tmp = press_times + start_offset + fixed_offset
        press_times_tmp = press_times_tmp[np.where(press_times_tmp >= sound_start)]
        press_times_tmp = press_times_tmp[np.where(press_times_tmp < sound_start + time_len)]
        for item in press_times_tmp:
            plot_vertical_line(item)
        fixed_offset = float(input("input fixed_offset : "))
        print("start_offset = {} fixed_offset = {} total_offset = {}".format(start_offset, fixed_offset,
                                                                             start_offset + fixed_offset))
        plt.legend()
        plt.show()
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))

total_offset =  start_offset + fixed_offset
print("total_offset = {}".format(total_offset))
press_times_tmp = press_times + total_offset
one_key_max_time = 0.2  # 200 ms
max_data_points = get_data_points_by_time(one_key_max_time, fs)
press_times_tmp = (press_times_tmp * fs).astype(np.int64)

data_len = len(data)


def cut(press_times_piece, keys_piece):
    global data
    global data_len
    for index, item in enumerate(press_times_piece):
        line_count = len(press_times_piece)
        start_index = item
        end_index = sys.maxsize
        if (index + 1 < line_count):
            end_index = press_times_piece[index + 1]
        end_index = min(end_index, start_index + max_data_points, data_len)
        one_key_sound = data[start_index:end_index, :]
        filename = tempfile.mktemp(prefix=''.join([str(keys_piece[index]), '_']),
                                   suffix='.wav', dir=label_data_dir)
        with sf.SoundFile(filename, mode='x', samplerate=fs,
                          channels=data.shape[1]) as file:
            file.write(one_key_sound)


# cut task
task_count = 1
press_times_tmp_len = len(press_times_tmp)
step = int(press_times_tmp_len / task_count)
for i in range(task_count):
    task_start = int(i * step)
    task_end = int((i + 1) * step)
    press_times_piece = press_times_tmp[task_start:task_end]
    keys_piece = keys[task_start:task_end]
    threading.Thread(target=cut, args=(press_times_piece,keys_piece)).start()
