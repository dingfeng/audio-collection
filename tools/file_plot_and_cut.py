# -*- coding: UTF-8 -*-
# filename: file_plot_and_cu date: 2018/10/31 21:52  
# author: FD 

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import  threading
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()

class CutThreading(threading.Thread):
    def __init__(self, data,dest_file,fs):
        threading.Thread.__init__(self)
        self._dest_file = dest_file
        self._data=data
        self._fs=fs
    def run(self):
        import soundfile as sf
        try:
            start = int(input('input start index:'))
            end = int(input("input end index:"))
            data = self._data[start:end, :]
            with sf.SoundFile(self._dest_file, mode='x', samplerate=self._fs,
                              channels=2, subtype=args.subtype) as file:
                file.write(data)
        except KeyboardInterrupt:
            parser.exit('\nInterrupted by user')
        except Exception as e:
            parser.exit(type(e).__name__ + ': ' + str(e))
        return

def cut_sound_file(source_file,dest_file):
    import soundfile as sf
    data, fs = sf.read(source_file, dtype='float32')
    cut_thread = CutThreading(data,dest_file,fs)
    cut_thread.start()
    plt.figure()
    plt.title(source_file)
    plt.plot(data[:, 0], label='channel 1')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    cut_dirs=['default_model']#['j_c_smoothed','j_u_smoothed','k_c_smoothed','l_c_smoothed']
    cut_root='.'
    dest_root_dir='./cut';
    for cut_dir in cut_dirs:
        cut_dir_path=os.path.join(cut_root,cut_dir)
        dest_dir_path=os.path.join(dest_root_dir,cut_dir)
        if(not os.path.isdir(dest_dir_path)):
            os.mkdir(dest_dir_path)
        for filename in os.listdir(cut_dir_path):
            if(filename.endswith("wav")):
                #sound file to cut
                source_file_path=os.path.join(cut_dir_path,filename)
                dest_file_path=os.path.join(dest_dir_path,filename)
                print("source: {}".format(source_file_path))
                print("dest: {}".format(dest_file_path))
                if(os.path.isfile(dest_file_path)):
                    continue
                cut_sound_file(source_file_path,dest_file_path)

