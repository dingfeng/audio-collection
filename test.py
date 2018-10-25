# -*- coding: UTF-8 -*-
# filename: test date: 2018/10/21 21:12  
# author: FD 
import threading


class PlotThreading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("hello world")

if __name__ == '__main__':
    thread=PlotThreading()
    thread.start()