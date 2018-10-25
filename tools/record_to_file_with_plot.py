# -*- coding: UTF-8 -*-
# filename: record_to_file date: 2018/10/19 13:22
# author: FD
import argparse
import tempfile
import queue
import sys
import threading
# import numpy as np
# import soundfile as sf
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf




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
# parser.add_argument(
#     '-c', '--channels', type=int, default=2, help='number of input channels')
parser.add_argument(
    'channels', type=int, default=[1,2], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    'filename',  nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument('-o', '--output-device', type=int_or_str,
                    help='output device ID or substring')
parser.add_argument('-lt', '--latency', type=float, default=0.5, help='latency in seconds')
parser.add_argument('-dt', '--dtype', help='audio data type')
parser.add_argument('-id', '--input-device', type=int_or_str,
                    help='input device ID or substring')
args = parser.parse_args()
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
fileQueue=queue.Queue()
q = queue.Queue()


class PlotThreading(threading.Thread):
    def __init__(self,file):
        threading.Thread.__init__(self)
        self._file=file
    def run(self):
        while True:
            self._file.write(fileQueue.get())
        pass

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata[::args.downsample, mapping])
    fileQueue.put(indata.copy())

def update_plot(frame):
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines

def direct_callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

try:
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,callback=direct_callback,
                   channels=max(args.channels)):
        print('#' * 80)
        print('press Return to quit')
        print('#' * 80)
        input()
    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(args.channels) > 1:
        ax.legend(['channel {}'.format(c) for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom='off', top='off', labelbottom='off',
                   right='off', left='off', labelleft='off')
    fig.tight_layout(pad=0)

    if args.filename is None:
        args.filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                        suffix='.wav', dir='')
    # Make sure the file is opened before recording anything:

    stream = sd.InputStream(samplerate=args.samplerate, device=args.device,
                   channels=max(args.channels), callback=callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)

    with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                      channels=max(args.channels), subtype=args.subtype) as file:
        with stream:
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            plotThread = PlotThreading(file)
            plotThread.start()
            # plt.show()

# except KeyboardInterrupt:
#     print('\nRecording finished: ' + repr(args.filename))
#     parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))