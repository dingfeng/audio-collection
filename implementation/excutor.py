# -*- coding: UTF-8 -*-
# filename: excutor date: 2018/11/10 23:22  
# author: FD
from collections import namedtuple
from multiprocessing import Process, Lock, Value


def listen(lock, status):
    KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                                 'scan_code', 'alt_pressed',
                                                 'time'])
    from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref
    import win32con, win32api, win32gui, atexit

    event_types = {win32con.WM_KEYDOWN: 'key down',
                   win32con.WM_KEYUP: 'key up',
                   0x104: 'key down',  # WM_SYSKEYDOWN, used for Alt key.
                   0x105: 'key up',  # WM_SYSKEYUP, used for Alt key.
                   }

    def low_level_handler(nCode, wParam, lParam):
        event = KeyboardEvent(event_types[wParam], lParam[0], lParam[1],
                              lParam[2] == 32, lParam[3])
        print(event)
        return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    pointer = CMPFUNC(low_level_handler)
    hook_id = windll.user32.SetWindowsHookExA(win32con.WH_KEYBOARD_LL, pointer,
                                              win32api.GetModuleHandle(None), 0)
    atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)

    while True:
        msg = win32gui.GetMessage(None, 0, 0)
        win32gui.TranslateMessage(byref(msg))
        win32gui.DispatchMessage(byref(msg))


audio_manager = None
lock = None
listen_process = None
status = Value('i', 0)


def main():
    import queue
    import sys
    import time
    import numpy as np
    import threading
    import sched
    import scipy.fftpack as fftp
    from pynput.keyboard import Listener
    from pynput.keyboard import Key, Controller
    scheduler = sched.scheduler(time.time, time.sleep)

    def log():
        global audio_manager
        audio_block_queue_size = audio_manager._queue.qsize()
        out_str = 'audio_block_queue_size={}'.format(audio_block_queue_size)
        print(out_str)
        scheduler.enter(5, 0, log)
        pass

    def start():
        global audio_manager
        global status_manager
        status_manager = Status_Manager()
        Listener_Thread().start()
        audio_manager = Audio_Manager()
        audio_manager.start()
        # scheduler.every(2).seconds.do(log)
        scheduler.enter(5, 0, log)
        scheduler.run(blocking=True)
        return

    class Audio_Manager(threading.Thread):
        def __init__(self, running=False, samplerate=16000, channels=1, device_info=None):
            threading.Thread.__init__(self)
            self._running = running
            self._samplerate = samplerate
            self._channels = channels
            self._queue = queue.Queue()
            self._device_info = device_info
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
                                channels=channels, callback=self.callback, blocksize=800,latency='low'):
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
                    # print('touch energy rate {}'.format(touch_energy_rate))
                    # print(total_energy)
                    if touch_energy_rate > 0.15 and energy < 1000:
                        # print('touch energy rate {}  energy {}'.format(touch_energy_rate, energy))
                        continous = True
                        # print('touched')
                        status_manager.touch_update()
                    else:
                        if continous:
                            continous = False
                            print('*' * 60)
                    before_window = window

    def press(key):
        global status_manager
        status_manager.press_update(key)

    def release(key):
        global status_manager
        status_manager.press_update(key)

    class Listener_Thread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            with Listener(on_press=press, on_release=release) as listener:
                listener.join()

    class Status_Manager():
        min_touch_key_time = 0.05
        max_touch_key_time = 1.3
        min_key_touch_time = 0.4

        def __init__(self):
            global lock
            global status
            print(Status_Manager.min_touch_key_time)
            self._status = status
            # self._keyboard_controller = Controller()
            self._last_touch_time = 0
            self._last_key_time = 0
            self._lock = lock
            # self._keyboard = Controller()
            return

        def press_update(self, key):
            current_key_time = time.time()
            with self._lock:
                time_diff = current_key_time - self._last_touch_time
                # print('press time diff {}'.format(time_diff))
                if self._status == 1 and time_diff > Status_Manager.min_touch_key_time and time_diff < Status_Manager.max_touch_key_time:
                    key_str = str(key)[1:-1]
                    if len(key_str) == 1:
                        large_key = chr(ord(key_str) - 32)
                        print("large key {}".format(large_key))
                        # self._keyboard.press(large_key)
                        # self._keyboard.release(large_key)
                self._status = 0
                self._last_key_time = current_key_time
            return

        def touch_update(self):
            current_touch_time = time.time()
            with self._lock:
                time_diff = current_touch_time - self._last_key_time
                # print('touch time_diff {}'.format(time_diff))
                if self._status == 0 and time_diff > Status_Manager.min_key_touch_time:
                    self._status = 1
                self._last_touch_time = current_touch_time
            return

    start()


if __name__ == '__main__':
    lock = Lock()
    listen_process = Process(target=listen, args=(lock, status))
    listen_process.start()
    main()
# Status_Manager()
