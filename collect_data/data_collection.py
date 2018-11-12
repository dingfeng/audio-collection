# -*- coding: UTF-8 -*-
# filename: test date: 2018/11/1 16:38  
# author: FD 
from pynput.keyboard import Listener
import logging
import  os
import time
import argparse
import tempfile
import queue
import sys
import threading
import uuid

file_prefix=str(uuid.uuid1())
log_dir = './data'
logging.basicConfig(filename=(log_dir + "/"+file_prefix+"_keylogger.txt"), format="%(message)s",
                    level=logging.INFO)
key_count=0
start_time=None
def press(key):
    global key_count
    global start_time
    if(key_count < 5 and str(key)=='Key.enter'):
        key_count=1+key_count
        if(key_count==5):
            start_time=time.time()
            logging.info("start {} start".format(start_time,))
        return
    if(start_time is not None):
        logging.info('press {} {}'.format(time.time()-start_time,str(key)))



class Listener_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        with Listener(on_press=press) as listener:
            listener.join()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=2, help='number of input channels')
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy  # Make sure NumPy is loaded before it is used in the callback
    assert numpy  # avoid "imported but unused" message (W0611)
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    if args.filename is None:
        args.filename = log_dir+"/"+file_prefix+"_data.wav"
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    # Make sure the file is opened before recording anything:
    with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype) as file:
        with sd.InputStream(samplerate=args.samplerate, device=device_info['name'],
                            channels=args.channels, callback=callback):
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            Listener_Thread().start()
            while True:
                file.write(q.get())


except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(args.filename))
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
