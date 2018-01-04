# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import numpy

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

'''
data_file = "C:\\Users\\peter\\Dropbox\\Development\\IPython\\sampleText.txt"
pullData = open(data_file,"r").read()
dataArray = pullData.split('\n')
xar = []
yar = []
for eachLine in dataArray:
    if len(eachLine)>1:
        x,y = eachLine.split(',')
        xar.append(int(x))
        yar.append(int(y))
'''

ser = serial.Serial('COM8', 115200, timeout=1)

proximities = []
def animate(i):
    proximity = int(ser.readline().strip().decode()[:-1])
    if i == 0:
        proximities.clear()
    proximities.append(proximity)
    ax1.clear()
    ax1.plot(range(i+1), proximities)
    print("Average: {}".format(numpy.mean(proximities)))

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
