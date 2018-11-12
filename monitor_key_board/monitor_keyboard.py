# -*- coding: UTF-8 -*-
# filename: monitor_keyboard date: 2018/11/8 14:57  
# author: FD 
from  pynput.keyboard import Key, Controller
from pynput.keyboard import Listener
from collections import namedtuple
import time

# time.sleep(5)

keyboard = Controller()


# Press and release space
# keyboard.press(Key.space)
# keyboard.release(Key.space)

def press(key):
    # keyboard.press(Key.backspace)
    # keyboard.press(Key.backspace)
    key_str=str(key)[1:-1]
    print(len(key_str) == 1 and chr(ord(key_str)-32))
    # if (key != Key.backspace):
    #     keyboard.press(Key.backspace)
    #     keyboard.release(Key.backspace)
    return


def realease(key):
    # print('release {}'.format(key))
    return


with Listener(on_press=press, on_release=realease) as listener:
    listener.join()


    # Type a lower case A; this will work even if no key on the
    # physical keyboard is labelled 'A'
    # keyboard.press('a')
    # keyboard.release('a')

    # Type two upper case As
    # keyboard.press('A')
    # keyboard.release('A')
    # with keyboard.pressed(Key.shift):
    #     keyboard.press('a')
    #     keyboard.release('a')

    # Type 'Hello World' using the shortcut type method
    # keyboard.type('Hello World')
