# -*- coding: UTF-8 -*-
# filename: plot_sound_realtime date: 2018/10/19 12:33
# author: FD

import argparse


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-f','--filename',  default="../tools/default_model/1.wav", help='audio file to be played back')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='output device (numeric ID or substring)')
args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read(args.filename, dtype='float32')
    sd.play(data, fs, device=args.device)
    status = sd.wait()
    if status:
        parser.exit('Error during playback: ' + str(status))
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))