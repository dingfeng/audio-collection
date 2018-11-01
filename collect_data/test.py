# -*- coding: UTF-8 -*-
# filename: test date: 2018/11/1 18:06  
# author: FD 
import matplotlib.pyplot as plt
import numpy as np

x=range(1,10)
y=[2*v for v in x]
print(x, y)
plt.plot(x, y)
while True:
    pos=plt.ginput(100000)
    print(pos)
