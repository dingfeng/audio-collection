# -*- coding: UTF-8 -*-
# filename: excutor date: 2018/11/10 23:22  
# author: FD
import time
import sched
from pynput.keyboard import Listener, Controller

if __name__ == '__main__':
    controller = Controller()


    def press(key):
        print('press key {}'.format(key))
        key_str = str(key)[1:-1]
        if len(key_str) == 1:
            large_key = chr(ord(key_str) - 32)
            controller.press(large_key)
            controller.release(large_key)

    def release(key):
        print('release key {}'.format(key))


    with Listener(on_press=press,on_release=release) as listener:
        listener.join()
# Status_Manager()
