# -*- coding: UTF-8 -*-
# filename: excutor date: 2018/11/10 23:22  
# author: FD
import time
import sched
from pynput.keyboard import Listener, Controller, KeyCode, Key

controller = Controller()

key_mapping = {}

def press(key):
    print('press key {}'.format(key))
    key_str = str(key)[1:-1]
    if len(key_str) == 1:
        # large_key = chr(ord(key_str) - 32)
        # controller.press(large_key)
        # controller.release(large_key)
        print("press")
        actions = key_mapping.get(key_str)
        if actions is None:
            return
        for action in actions:
            controller.press(action)
        for i in range(len(actions)):
            controller.release(actions[len(actions) - 1 - i])


def release(key):
    print('release key {}'.format(key))


def trim(s):
    if len(s) == 0:
        return s
    elif s[0] == ' ' or s[0] == '\n':
        return (trim(s[1:]))
    elif s[-1] == ' ' or s[-1] == '\n':
        return (trim(s[:-1]))
    return s


def load_key_binding():
    global key_mapping
    str_to_symbol = {'shift': Key.shift, 'ctrl': Key.ctrl, 'alt': Key.alt, 'page_up': Key.page_up,
                     'page_down': Key.page_down, 'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3,
                     'f4': Key.f4, 'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8, 'f9': Key.f9}
    with open('./touch_key_binding.txt', 'r') as file:
        for line in file.readlines():
            line = trim(line)
            str_array = line.split('=')
            key = str_array[0]
            action_series = str_array[1]
            actions = action_series.split('+')
            key_mapping[key] = []
            for action in actions:
                action = trim(action)
                if action.__len__() == 1:
                    key_mapping[key].append(action)
                else:
                    key_action = str_to_symbol.get(action)
                    if (key_action is None):
                        raise Exception('wrong key {}'.format(action))
                    key_mapping[key].append(key_action)

    return


if __name__ == '__main__':
    load_key_binding()
    with Listener(on_press=press, on_release=release) as   listener:
        listener.join()
        # Status_Manager()
