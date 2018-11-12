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
        actions = key_mapping.get(key_str)
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
                elif action == 'shift':
                    key_mapping[key].append(Key.shift)
                elif action == 'ctrl':
                    key_mapping[key].append(Key.ctrl)
                else:
                    raise Exception('wrong key {}'.format(action))
    return


if __name__ == '__main__':
    load_key_binding()
    with Listener(on_press=press, on_release=release) as listener:
        listener.join()
# Status_Manager()
