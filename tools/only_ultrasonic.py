# -*- coding: UTF-8 -*-
# filename: plot_buffer_worth_file date: 2018/10/31 20:56
# author: FD
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft,ifft
import scipy.signal as signal
import os

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f','--filename',  default="../collect_data/data/j.wav", help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()


def butter_highpass_filter(data, cut, fs, order, zero_phase=False):
    from scipy.signal import butter, lfilter, filtfilt
    nyq = 0.5 * fs
    cut = cut / nyq
    b, a = butter(order, cut, btype='high')
    y = (filtfilt if zero_phase else lfilter)(b, a, data)
    return y



def smooth_and_write_to_file(source,dest):
    try:
        import soundfile as sf
        data, fs = sf.read(source, dtype='float32')
        fs = 44100
        high_freq=18000
        order=5
        y1 = butter_highpass_filter(data[:, 0], high_freq, fs, order)
        y2 = butter_highpass_filter(data[:, 1], high_freq, fs, order)
        with sf.SoundFile(dest, mode='x', samplerate=44100,
                          channels=2, subtype=args.subtype) as file:
            file.write(np.asarray([y1, y2]).T)
    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


if __name__ == '__main__':
    # dir_names=['j_c','j_u','k_c','l_c']
    # root='.'
    # for dir_name in dir_names:
    #     dir_path=''.join([root,'/',dir_name])
    #     dest_dir_path=''.join([dir_path,'_smoothed'])
    #     if(not os.path.isdir(dest_dir_path)):
    #         os.mkdir(dest_dir_path,0o0755)u
    #     indir_files=os.listdir(dir_path)
    #     for file in indir_files:
    #         if(file.endswith('wav')):
    #             #wav file wathdirjjj
    #             source_file_path=''.join([dir_path,'/',file])
    #             dest_file_path=''.join([dest_dir_path,'/',file])
    #             if(os.path.exists(dest_file_path)):
    #                 os.remove(dest_file_path)
    #             smooth_and_write_to_file(source_file_path,dest_file_path)
    smooth_and_write_to_file("default_model/3.wav", 'smoothed_high2.wav')


