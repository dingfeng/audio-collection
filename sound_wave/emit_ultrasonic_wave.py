# -*- coding: UTF-8 -*-
# filename: emit_ultrasonic_wave date: 2018/11/7 17:44  
# author: FD 
import numpy as np
from common.common import *


def write_sound_to_file():
    y = np.zeros(44100).reshape(44100,1)
    write_to_sound_file('ultrasonic.wav', y, 44100)


write_sound_to_file();
