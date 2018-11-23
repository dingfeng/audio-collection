# -*- coding: UTF-8 -*-
# filename: common date: 2018/11/12 14:28  
# author: FD
import queue
import sys
import numpy as np
import threading
import scipy.fftpack as fftp
import time


class Audio_Manager(threading.Thread):
    def __init__(self, running=False, samplerate=16000, channels=1, device_info=None, status_manager=None):
        threading.Thread.__init__(self)
        self._running = running
        self._samplerate = samplerate
        self._channels = channels
        self._queue = queue.Queue()
        self._device_info = device_info
        self._status_manager = status_manager
        return

    def get_window_energy(self):
        return self._queue.get()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self._queue.put(np.squeeze(indata.copy()).tolist())

    def run(self):
        import sounddevice as sd
        self._device_info = sd.query_devices(self._device_info, 'input')
        samplerate = self._samplerate or self._device_info['default_samplerate']
        channels = self._channels or self._device_info['max_input_channels']
        with sd.InputStream(samplerate=samplerate, device=self._device_info['name'],
                            channels=channels, callback=self.callback, blocksize=800, latency='low'):
            # scheduler.run(False)
            before_window = []
            continous = False
            while True:
                window = self.get_window_energy()
                total_window = window + before_window
                win_f = fftp.fft(total_window, len(total_window))
                energy = (abs(win_f[5]) ** 2 + abs(win_f[6]) ** 2)
                total_energy = np.sum(np.square(abs(win_f)))
                touch_energy_rate = energy / total_energy
                # print('total_energy {} energy {}'.format(total_energy,energy))
                # if touch_energy_rate > 0.15 and energy < 1000:
                if energy > 100 and energy < 1000:
                    continous = True
                    self._status_manager.touch_update()
                else:
                    if continous:
                        continous = False
                        # print('*' * 60)
                before_window = window


class Status_Manager():
    min_touch_key_time = 0.03
    max_touch_key_time = 2.0
    min_key_touch_time = 0.5

    def __init__(self, trigger):
        # print(Status_Manager.min_touch_key_time)
        self._status = 0
        # self._keyboard_controller = Controller()
        self._last_touch_time = 0
        self._last_key_time = 0
        self._lock = threading.Lock()
        # self._keyboard = Controller()
        self._trigger = trigger
        return

    def press_update(self):
        current_key_time = time.time()
        result = 0
        with self._lock:
            time_diff = current_key_time - self._last_touch_time
            # print('press time diff {}'.format(time_diff))
            if self._status == 1 and time_diff > Status_Manager.min_touch_key_time and time_diff < Status_Manager.max_touch_key_time:
                # key_str = str(key)[1:-1]
                # if len(key_str) == 1:
                #     large_key = chr(ord(key_str) - 32)
                #     self._trigger(large_key)
                #     # self._keyboard.press(large_key)
                #     # self._keyboard.release(large_key)
                result = 1
            self._status = 0
            self._last_key_time = current_key_time
        return result

    def touch_update(self):
        current_touch_time = time.time()
        with self._lock:
            time_diff = current_touch_time - self._last_key_time
            # print('touch time_diff {}'.format(time_diff))
            if self._status == 0 and time_diff > Status_Manager.min_key_touch_time:
                self._status = 1
            self._last_touch_time = current_touch_time
        return


def trigger(key):
    pass


status_manager = None


def build_and_run():
    global status_manager
    status_manager = Status_Manager(trigger)
    audio_manager = Audio_Manager(status_manager=status_manager)
    audio_manager.start()
    return
